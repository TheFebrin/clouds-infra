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

source "googlecompute" "nginx-http" {
  account_file        = var.credentials
  disk_size           = 10
  image_description   = "Nginx http server image"
  image_family        = "nginx-image"
  image_name          = "nginx-http-${local.timestamp}"
  machine_type        = "f1-micro"
  project_id          = var.project_id
  source_image_family = local.source_image_family
  ssh_username        = "packer"
  region              = "us-central1"
  zone                = "us-central1-a"
}

build {
  sources = ["source.googlecompute.nginx-http"]

  provisioner "ansible" {
    user          = "packer"
    playbook_file = "../ansible/nginx_http_servers.yml"
  }

  provisioner "shell" {
    inline = ["sudo rm /home/packer/.ssh/authorized_keys"]
  }

}