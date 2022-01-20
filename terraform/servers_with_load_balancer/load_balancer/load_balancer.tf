variable "network" {
  description = "google_compute_network"
}

variable "subnetwork" {
  description = "google_compute_subnetwork"
}

resource "google_compute_address" "load_balancer_public_ip" {
    name         = "load-balancer-public-ip"
    address_type = "EXTERNAL"
}

resource "google_compute_address" "load_balancer_private_ip" {
    name         = "load-balancer-private-ip"
    address_type = "INTERNAL"
    subnetwork   = var.subnetwork.self_link
    address      = "10.0.1.255"
}

resource "google_compute_firewall" "firewall_ssh_load_balancer" {
    name    = "firewall-ssh-load-balancer"
    network = var.network.self_link
    priority = 1000

    allow {
        protocol = "tcp"
        ports    = ["22"]
    }

    source_ranges = ["79.110.199.238", "156.17.151.30"]
}

# Create load balancer
resource "google_compute_instance" "load_balancer" {
    name         = "load-balancer"
    machine_type = "f1-micro"
    zone         = "europe-west3-a"

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"  # TODO load prepared image
        }
    }

    network_interface {
        network = var.network.self_link
        subnetwork = var.subnetwork.self_link

        network_ip = google_compute_address.load_balancer_private_ip.address

        access_config {
            nat_ip = google_compute_address.load_balancer_public_ip.address
        }
    }

}