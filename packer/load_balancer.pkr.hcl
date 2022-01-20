variable "project_id" {
  type    = string
  default = "chmurki-329715"
}

variable "credentials" {
  type    = string
  default = "/Users/febrin/sa-private-key.json"
}

locals {
  timestamp           = regex_replace(timestamp(), "[- TZ:]", "")
  source_image_family = "debian-11"
}

source "googlecompute" "load-balancer" {
  account_file        = var.credentials
  disk_size           = 10
  image_description   = "Load balancer image"
  image_family        = "load-balancer-image"
  image_name          = "load-balancer-${local.timestamp}"
  machine_type        = "f1-micro"
  project_id          = var.project_id
  source_image_family = local.source_image_family
  ssh_username        = "packer"
  region              = "us-central1"
  zone                = "us-central1-a"
}

build {
  sources = ["source.googlecompute.load-balancer"]

  provisioner "ansible" {
    user          = "packer"
    playbook_file = "../ansible/load_balancer.yml"
  }

  provisioner "shell" {
    inline = ["sudo rm /home/packer/.ssh/authorized_keys"]
  }

}