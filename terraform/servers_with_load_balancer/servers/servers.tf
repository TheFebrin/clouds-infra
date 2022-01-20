variable "vm_type" {
  description = "VM type, can be (micro, small, medium)."
}

variable "vm_number" {
  description = "How many VM to create."
}

locals {
  vm_type_map = {
    micro   = "f1-micro"
    small   = "f1-small"
    medium  = "f1-medium"
  }
}

# Create networks
resource "google_compute_network" "servers_network" {
    name = "servers-network-new"   
    auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "servers_subnetwork" {
    # gcloud compute networks subnets list  | grep servers_network
    name          = "servers-subnetwork"
    ip_cidr_range = "10.0.0.0/16"
    network       = google_compute_network.servers_network.self_link
}

# IPs
resource "google_compute_address" "servers_private_ips" {
    count = var.vm_number

    name         = "private-server-ip-${count.index}"
    address_type = "INTERNAL"
    subnetwork   = google_compute_subnetwork.servers_subnetwork.self_link
    address      = "10.0.1.${count.index}"
}

# Configure Firewall
resource "google_compute_firewall" "servers_firewall" {
    name    = "servers-firewall"
    network = google_compute_network.servers_network.self_link
    priority = 1000

    allow {
        protocol = "tcp"
        ports    = ["22"]
    }

    source_ranges = ["79.110.199.238", "156.17.151.30"]
}

resource "google_compute_firewall" "servers_firewall_2" {
    name    = "servers-firewall-2"
    network = google_compute_network.servers_network.self_link
    priority = 1000

    allow {
        protocol = "tcp"
        ports    = ["80"]
    }

    source_ranges = ["0.0.0.0/0"]
}

# Create VM instance
resource "google_compute_instance" "backend_servers" {
    count = var.vm_number

    name         = "server-${count.index}"
    machine_type = local.vm_type_map[var.vm_type]
    zone         = "europe-west3-a"    

    tags         =  ["http-server", "https-server"]

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"
        }
    }

    network_interface {
        network = google_compute_network.servers_network.self_link
        subnetwork = google_compute_subnetwork.servers_subnetwork.self_link

        network_ip = google_compute_address.servers_private_ips[count.index].address
    }

    metadata_startup_script = file("servers/script.bash")
}


output "network" {
  value = google_compute_network.servers_network
}

output "subnetwork" {
  value = google_compute_subnetwork.servers_subnetwork
}