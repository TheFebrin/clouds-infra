variable "project_id" {
  description = "project_id"
  default = "chmurki-329715"
}

provider "google" {
    project = var.project_id
    region  = "europe-west3"
}

module "setup_backend_servers" {
    source = "./servers/"

    vm_type = "micro"
    vm_number = 3
}

module "setup_load_balancer" {
    source = "./load_balancer/"

    network = module.setup_backend_servers.network
    subnetwork = module.setup_backend_servers.subnetwork
}