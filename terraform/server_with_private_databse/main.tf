variable "project_id" {
  description = "project_id"
  default = "chmurki-329715"
}

variable "server_private_ip" {
  description = "private IP for the server"
  default = "10.0.21.37"
}

provider "google" {
    project = var.project_id
    region  = "europe-west3"
}

# Create networks
resource "google_compute_network" "main_network" {
    name = "main"   
}

resource "google_compute_subnetwork" "main_subnetwork" {
    # gcloud compute networks subnets list  | grep servers
    name          = "servers"
    ip_cidr_range = "10.0.0.0/16"
    network       = google_compute_network.main_network.self_link
}


# Configure Firewall
resource "google_compute_firewall" "firewall" {
    name    = "my-firewall-rules"
    network = google_compute_network.main_network.self_link
    priority = 2137

    allow {
        protocol = "tcp"
        ports    = ["80", "443"]
    }

    allow {
        protocol = "udp"
        ports    = ["80", "443"]
    }

    source_ranges = ["0.0.0.0/0"]
    target_tags = ["allow-http"]
}

# Allow ssh
resource "google_compute_firewall" "firewall-ssh" {
    name    = "ssh-firewall-rule"
    network = google_compute_network.main_network.self_link
    priority = 1000

    allow {
        protocol = "tcp"
        ports    = ["22"]
    }
    
    source_ranges = ["79.110.199.238", "156.17.151.30"]
}

# SSH access
# module "firewall_rules" {
#   source       = "terraform-google-modules/network/google//modules/firewall-rules"
#   project_id   = var.project_id
#   network_name = google_compute_network.main_network.self_link

#   rules = [{
#     name                    = "allow-ssh-ingress"
#     description             = null
#     direction               = "INGRESS"
#     priority                = null
#     ranges                  = ["79.110.199.238"]
#     source_tags             = null
#     source_service_accounts = null
#     target_tags             = null
#     target_service_accounts = null
#     allow = [{
#       protocol = "tcp"
#       ports    = ["22"]
#     }]
#     deny = []
#     log_config = {
#       metadata = "INCLUDE_ALL_METADATA"
#     }
#   }]
# }


# Create IP addresses
resource "google_compute_address" "public_ip" {
    name         = "public-server-ip"
    address_type = "EXTERNAL"
}

# resource "google_compute_address" "public_ip2" {
#     name         = "public-server-ip2"
#     address_type = "EXTERNAL"
# }

resource "google_compute_address" "private_ip" {
    name         = "private-server-ip"
    address_type = "INTERNAL"
    subnetwork   = google_compute_subnetwork.main_subnetwork.self_link  # self link vs id ??
    address      = var.server_private_ip
}

resource "google_compute_global_address" "private_ip_address_database" {
    project       = var.project_id
    provider      = google-beta
    name          = "private-ip-address-database"
    purpose       = "VPC_PEERING"
    address_type  = "INTERNAL"
    prefix_length = 16
    network       = google_compute_network.main_network.self_link
}

resource "google_service_networking_connection" "private_vpc_connection" {
  provider                = google-beta

  network                 = google_compute_network.main_network.self_link
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address_database.name]
}

# Create VM instance
resource "google_compute_instance" "main_server" {
    name         = "myserver"
    machine_type = "f1-micro"
    zone         = "europe-west3-a"
    tags         =  ["allow-http", "http-server", "https-server"]

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"
        }
    }

    network_interface {
        network = google_compute_network.main_network.self_link
        subnetwork = google_compute_subnetwork.main_subnetwork.self_link
        network_ip = google_compute_address.private_ip.address

        access_config {
            nat_ip = google_compute_address.public_ip.address
        }
    }
}

# resource "google_compute_instance" "test-ssh" {
#     name         = "test-ssh"
#     machine_type = "f1-micro"
#     zone         = "europe-west3-a"
#     tags         =  ["ssh-enabled"]
    
#     depends_on = [google_service_networking_connection.private_vpc_connection]

#     boot_disk {
#         initialize_params {
#             image = "debian-cloud/debian-11"
#         }
#     }

#     metadata = {
#       "enable-oslogin" = "TRUE"
#     }

#     network_interface {
#         network = google_compute_network.main_network.self_link
#         access_config {}
#     }
# }

# Create Database
resource "google_sql_database_instance" "database" {
    # mysql -h 10.70.0.9 -u databaseuser -p 
    name                = "database-instance-private-ip-2"
    database_version    = "MYSQL_8_0"
    deletion_protection = false

    depends_on = [google_service_networking_connection.private_vpc_connection]

    settings {
        tier      = "db-f1-micro"
        disk_size = 10
        
        ip_configuration {
            ipv4_enabled    = false
            private_network = google_compute_network.main_network.self_link

            # authorized_networks {
            #   name = "myserver"
              # value = var.server_private_ip
              # value = "10.0.0.1/32"
            # }
        }
    }
}

resource "google_sql_database" "users" {
    instance  = google_sql_database_instance.database.name
    name      = "users-database"
}

resource "google_sql_user" "database_user" {
    instance  = google_sql_database_instance.database.name
    name      = "databaseuser"
    password  = "databaseuser"
    # host      = google_compute_instance.main_server.name
}

output "server_instance_name" {
  value = google_compute_instance.main_server.name
}

output "server_ip_public_address" {
  value = google_compute_address.public_ip.address
}

output "server_ip_private_address" {
  value = google_compute_address.private_ip.address
}

output "main_subnetwork_id" {
  value = google_compute_subnetwork.main_subnetwork.id
}

output "main_subnetwork_self_link" {
  value = google_compute_subnetwork.main_subnetwork.self_link
}

