variable "project_id" {
  description = "project_id"
  default = "chmurki-329715"
}

variable "server_private_ip" {
  description = "private IP for the server"
  default = "10.0.42.42"
}

provider "google" {
    project = var.project_id
    region  = "europe-west3"
}

# Create networks
resource "google_compute_network" "main_network2" {
    name = "main2"   
}

resource "google_compute_subnetwork" "main_subnetwork2" {
    # gcloud compute networks subnets list  | grep servers
    name          = "servers2"
    ip_cidr_range = "10.0.0.0/16"
    network       = google_compute_network.main_network2.self_link
}


# Configure Firewall
resource "google_compute_firewall" "firewall2" {
    name    = "my-firewall-rules2"
    network = google_compute_network.main_network2.self_link
    priority = 1000

    allow {
        protocol = "tcp"
        ports    = ["80", "443"]
    }

    allow {
        protocol = "udp"
        ports    = ["80", "443"]
    }

    source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "firewall-ssh2" {
    name    = "allow-ssh-firewall-rule"
    network = google_compute_network.main_network2.self_link
    priority = 1000

    allow {
        protocol = "tcp"
        ports    = ["22"]
    }

    source_ranges = ["79.110.199.238", "156.17.151.30"]
}

# Create IP addresses
resource "google_compute_address" "public_ip2" {
    name         = "public-server-ip2"
    address_type = "EXTERNAL"
}

resource "google_compute_address" "private_ip2" {
    name         = "private-server-ip2"
    address_type = "INTERNAL"
    subnetwork   = google_compute_subnetwork.main_subnetwork2.self_link  # self link vs id ??
    address      = var.server_private_ip
}

# Create VM instance
resource "google_compute_instance" "main_server2" {
    name         = "myserver2"
    machine_type = "f1-micro"
    zone         = "europe-west3-a"
    tags         =  ["allow-http", "http-server", "https-server"]

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"
        }
    }

    network_interface {
        network = google_compute_network.main_network2.self_link
        subnetwork = google_compute_subnetwork.main_subnetwork2.self_link
        network_ip = google_compute_address.private_ip2.address

        access_config {
            nat_ip = google_compute_address.public_ip2.address
        }
    }
}

# Create Database
resource "google_sql_database_instance" "database" {
    # mysql -h 34.107.42.84 -u databaseuser -p 
    name                = "database-instance-public-ip"
    database_version    = "MYSQL_8_0"
    deletion_protection = false

    settings {
        tier      = "db-f1-micro"
        disk_size = 10
        
        ip_configuration {

            authorized_networks {
              name = "myserver"
              value = google_compute_address.public_ip2.address
            }
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
}

output "server_instance_name" {
  value = google_compute_instance.main_server2.name
}

output "server_ip_public_address" {
  value = google_compute_address.public_ip2.address
}

output "server_ip_private_address" {
  value = google_compute_address.private_ip2.address
}

output "main_subnetwork_id" {
  value = google_compute_subnetwork.main_subnetwork2.id
}

output "main_subnetwork_self_link" {
  value = google_compute_subnetwork.main_subnetwork2.self_link
}

