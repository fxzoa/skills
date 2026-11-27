# ==============================================================================
# GCP API Services Enablement
# ==============================================================================
resource "google_project_service" "enabled_apis" {
  for_each = toset(var.gcp_services)

  project = var.project_id
  service = each.key

  disable_on_destroy         = false
  disable_dependent_services = false
}

# ==============================================================================
# Network Configuration
# ==============================================================================
resource "google_compute_network" "vpc_network" {
  name                    = var.vpc_network_name
  project                 = var.project_id
  auto_create_subnetworks = false
  description             = "Dedicated VPC network for Always Free tier environment"

  depends_on = [
    google_project_service.enabled_apis
  ]
}

resource "google_compute_subnetwork" "subnet" {
  name                     = var.subnet_name
  project                  = var.project_id
  ip_cidr_range            = var.subnet_ip_cidr_range
  region                   = var.region
  network                  = google_compute_network.vpc_network.id
  private_ip_google_access = true
}

# Firewall: Allow SSH (Port 22)
resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh-ingress"
  project = var.project_id
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-ssh"]
  description   = "Allow incoming SSH traffic"
}

# Firewall: Allow ICMP (Ping)
resource "google_compute_firewall" "allow_icmp" {
  name    = "allow-icmp-ingress"
  project = var.project_id
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "icmp"
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-ssh"]
  description   = "Allow incoming ICMP ping"
}

# Firewall: Allow Internal & Peered VPC Traffic (CIDR-based across VPC peering)
resource "google_compute_firewall" "allow_internal" {
  name        = "allow-internal"
  project     = var.project_id
  network     = google_compute_network.vpc_network.name
  description = "Allow internal traffic across local and peered VPC subnets"

  allow {
    protocol = "icmp"
  }
  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }
  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  source_ranges = concat([var.subnet_ip_cidr_range], var.peered_cidrs)
  priority      = 65534
}

# Firewall: Allow Inbound Redis (Port 6379) from peered Bot VPC CIDRs
# Note: Network tags do not work across VPC peering; CIDR source_ranges are required.
resource "google_compute_firewall" "allow_redis_from_peered" {
  count       = var.enable_redis_firewall && length(var.peered_cidrs) > 0 ? 1 : 0
  name        = "allow-redis-from-peered-vpcs"
  project     = var.project_id
  network     = google_compute_network.vpc_network.name
  description = "Allow inbound Redis traffic (Port 6379) from peered Bot VPCs"

  allow {
    protocol = "tcp"
    ports    = ["6379"]
  }

  source_ranges = var.peered_cidrs
  target_tags   = ["redis-server"]
  priority      = 1000
}

# ==============================================================================
# Always Free GCE Instance Configuration
# ==============================================================================
data "google_compute_image" "ubuntu" {
  family  = "ubuntu-2204-lts"
  project = "ubuntu-os-cloud"
}

resource "google_compute_instance" "vm_instance" {
  name         = var.instance_name
  project      = var.project_id
  machine_type = "e2-micro"
  zone         = var.zone

  tags = var.instance_tags

  boot_disk {
    auto_delete = true
    initialize_params {
      image = data.google_compute_image.ubuntu.self_link
      type  = "pd-standard"
      size  = var.boot_disk_size_gb
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.subnet.self_link

    access_config {
      network_tier = "STANDARD"
    }
  }

  metadata = merge(
    {
      enable-oslogin = "TRUE"
    },
    var.ssh_public_key != "" ? {
      ssh-keys = "${var.ssh_user}:${var.ssh_public_key}"
    } : {}
  )

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
  }

  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }

  lifecycle {
    prevent_destroy = false
  }
}

# ==============================================================================
# Billing Budget Alert Configuration
# ==============================================================================
resource "google_monitoring_notification_channel" "billing_alert_email" {
  count        = var.billing_account_id != "" && var.budget_alert_email != "" ? 1 : 0
  project      = var.project_id
  display_name = "Billing Alert Notification Channel"
  type         = "email"

  labels = {
    email_address = var.budget_alert_email
  }

  depends_on = [
    google_project_service.enabled_apis
  ]
}

resource "google_billing_budget" "budget_one_dollar" {
  count           = var.billing_account_id != "" && var.budget_alert_email != "" ? 1 : 0
  billing_account = var.billing_account_id
  display_name    = "Always Free Safeguard Budget (${var.project_id})"

  depends_on = [
    google_project_service.enabled_apis
  ]

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = "JPY"
      units         = "150"
      nanos         = 0
    }
  }

  threshold_rules {
    threshold_percent = 1.0
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 0.5
    spend_basis       = "CURRENT_SPEND"
  }

  threshold_rules {
    threshold_percent = 1.0
    spend_basis       = "FORECASTED_SPEND"
  }

  all_updates_rule {
    monitoring_notification_channels = [
      google_monitoring_notification_channel.billing_alert_email[0].id
    ]
    disable_default_iam_recipients = false
  }
}
