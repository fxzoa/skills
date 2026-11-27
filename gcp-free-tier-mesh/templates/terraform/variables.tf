variable "region" {
  description = "Region for Always Free tier (all 5 projects must be in the same region for free/low-cost VPC peering)"
  type        = string
  default     = "us-central1"

  validation {
    condition     = contains(["us-central1", "us-west1", "us-east1"], var.region)
    error_message = "The region must be one of Always Free supported regions: us-central1, us-west1, or us-east1."
  }
}

variable "zone" {
  description = "Zone within the selected Always Free region (same zone = $0.00 cross-project internal egress)"
  type        = string
  default     = "us-central1-a"
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
  description = "Name of the VPC network in each project"
  type        = string
  default     = "coin-vpc"
}

variable "subnet_name" {
  description = "Name of the subnetwork in each project"
  type        = string
  default     = "coin-subnet"
}

variable "ssh_user" {
  description = "Default SSH username"
  type        = string
  default     = "ppbb"
}

variable "ssh_public_key" {
  description = "Public SSH key string (e.g., 'ssh-ed25519 AAAAC3... user@host'). Leave empty if using OS Login or gcloud compute ssh."
  type        = string
  default     = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDFWprqy/USq0UqTk6YSYRpMfJq6UFJPn5iuNZivxbRi nanbingjun@gmail.com"
}

variable "credentials_files" {
  description = "Optional map of service account JSON key paths per node key (btczoa, fxzoa2020, nanbingjun, nanheishun, nanzhiyan)"
  type        = map(string)
  default     = {}
}

variable "access_tokens" {
  description = "Optional map of short-lived OAuth2 access tokens per node key (e.g. from gcloud auth print-access-token --account=...)"
  type        = map(string)
  default     = {}
  sensitive   = true
}

variable "nodes" {
  description = "Configuration map for the 5 Always Free GCP project nodes"
  type = map(object({
    project_id         = string
    instance_name      = string
    cidr               = string
    role               = string
    billing_account_id = optional(string, "")
    budget_alert_email = optional(string, "")
  }))
  default = {
    btczoa = {
      project_id    = "btczoa-project"
      instance_name = "vm-btczoa-redis"
      cidr          = "10.0.0.0/24"
      role          = "VM #0: Redis Server Hub"
    }
    fxzoa2020 = {
      project_id    = "fxzoa2020-project"
      instance_name = "vm-fxzoa2020"
      cidr          = "10.10.0.0/24"
      role          = "VM #1: price-monitor + slack-alert-sender"
    }
    nanbingjun = {
      project_id         = "nanbingjun-project"
      instance_name      = "vm-nanbingjun"
      cidr               = "10.20.0.0/24"
      role               = "VM #2: btc-dca-bot + btc-grid-bot"
      billing_account_id = "015435-AC9BBD-C349B6"
      budget_alert_email = "nanbingjun@gmail.com"
    }
    nanheishun = {
      project_id    = "nanheishun-project"
      instance_name = "vm-nanheishun"
      cidr          = "10.30.0.0/24"
      role          = "VM #3: multi-dca-bot + surge-dip-bot"
    }
    nanzhiyan = {
      project_id    = "nanzhiyan-project"
      instance_name = "vm-nanzhiyan"
      cidr          = "10.40.0.0/24"
      role          = "VM #4: top20-tracker-worker + reserve"
    }
  }
}
