variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Region for Always Free tier (us-central1, us-west1, or us-east1)"
  type        = string
  default     = "us-central1"

  validation {
    condition     = contains(["us-central1", "us-west1", "us-east1"], var.region)
    error_message = "The region must be one of Always Free supported regions: us-central1, us-west1, or us-east1."
  }
}

variable "zone" {
  description = "Zone within the selected Always Free region"
  type        = string
  default     = "us-central1-a"
}

variable "instance_name" {
  description = "Name of the compute instance"
  type        = string
}

variable "boot_disk_size_gb" {
  description = "Boot disk size in GB (Always Free allows up to 30 GB standard persistent disk)"
  type        = number
  default     = 30

  validation {
    condition     = var.boot_disk_size_gb <= 30
    error_message = "Disk size must not exceed 30 GB to stay within the Always Free tier."
  }
}

variable "vpc_network_name" {
  description = "Name of the VPC network"
  type        = string
  default     = "coin-vpc"
}

variable "subnet_name" {
  description = "Name of the subnetwork"
  type        = string
  default     = "coin-subnet"
}

variable "subnet_ip_cidr_range" {
  description = "IP CIDR range for the subnetwork"
  type        = string
}

variable "peered_cidrs" {
  description = "List of peered VPC subnet CIDRs allowed for internal/SSH/Redis communication"
  type        = list(string)
  default     = []
}

variable "instance_tags" {
  description = "Network tags attached to the GCE instance"
  type        = list(string)
  default     = ["allow-ssh"]
}

variable "enable_redis_firewall" {
  description = "Whether to create inbound Redis (6379) firewall rule from peered_cidrs"
  type        = bool
  default     = false
}

variable "ssh_user" {
  description = "Default SSH username"
  type        = string
  default     = "ppbb"
}

variable "ssh_public_key" {
  description = "Public SSH key string. Leave empty if using OS Login or gcloud compute ssh."
  type        = string
  default     = ""
}

variable "billing_account_id" {
  description = "Billing Account ID. Set to empty string to skip budget configuration."
  type        = string
  default     = ""
}

variable "budget_alert_email" {
  description = "Email address for billing budget threshold alerts"
  type        = string
  default     = ""
}

variable "gcp_services" {
  description = "List of GCP APIs to enable for Always Free environment"
  type        = list(string)
  default = [
    "cloudresourcemanager.googleapis.com",
    "serviceusage.googleapis.com",
    "compute.googleapis.com",
    "iam.googleapis.com",
    "oslogin.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    "billingbudgets.googleapis.com"
  ]
}
