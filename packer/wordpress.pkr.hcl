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

source "googlecompute" "wordpress" {
  account_file        = var.credentials
  disk_size           = 10
  image_description   = "Wordpress image"
  image_family        = "wordpress-image"
  image_name          = "wordpress-${local.timestamp}"
  machine_type        = "f1-micro"
  project_id          = var.project_id
  source_image_family = local.source_image_family
  ssh_username        = "packer"
  region              = "us-central1"
  zone                = "us-central1-a"
}

build {
  sources = ["source.googlecompute.wordpress"]

  provisioner "ansible" {
    user          = "packer"
    playbook_file = "../ansible/wordpress.yml"
  }

  provisioner "shell" {
    inline = ["sudo rm /home/packer/.ssh/authorized_keys"]
  }

}