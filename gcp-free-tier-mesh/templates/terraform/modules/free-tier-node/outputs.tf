output "project_id" {
  value = var.project_id
}

output "vpc_id" {
  value = google_compute_network.vpc_network.id
}

output "vpc_self_link" {
  value = google_compute_network.vpc_network.self_link
}

output "subnet_cidr" {
  value = google_compute_subnetwork.subnet.ip_cidr_range
}

output "instance_name" {
  value = google_compute_instance.vm_instance.name
}

output "zone" {
  value = google_compute_instance.vm_instance.zone
}

output "public_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].access_config[0].nat_ip
}

output "private_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].network_ip
}

output "ssh_command" {
  value = "gcloud compute ssh ${google_compute_instance.vm_instance.name} --zone=${google_compute_instance.vm_instance.zone} --project=${var.project_id}"
}
