terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# ==============================================================================
# Project-scoped Google Providers (5 Always Free Projects)
# Set credentials_files["<key>"] to a service account JSON path per project,
# or leave empty to use Application Default Credentials (ADC) / shared SA.
# ==============================================================================
provider "google" {
  alias                 = "btczoa"
  project               = var.nodes["btczoa"].project_id
  region                = var.region
  zone                  = var.zone
  user_project_override = true
  billing_project       = var.nodes["btczoa"].project_id
  credentials           = try(var.credentials_files["btczoa"], "") != "" ? var.credentials_files["btczoa"] : null
  access_token          = try(var.access_tokens["btczoa"], "") != "" ? var.access_tokens["btczoa"] : null
}

provider "google" {
  alias                 = "fxzoa2020"
  project               = var.nodes["fxzoa2020"].project_id
  region                = var.region
  zone                  = var.zone
  user_project_override = true
  billing_project       = var.nodes["fxzoa2020"].project_id
  credentials           = try(var.credentials_files["fxzoa2020"], "") != "" ? var.credentials_files["fxzoa2020"] : null
  access_token          = try(var.access_tokens["fxzoa2020"], "") != "" ? var.access_tokens["fxzoa2020"] : null
}

provider "google" {
  alias                 = "nanbingjun"
  project               = var.nodes["nanbingjun"].project_id
  region                = var.region
  zone                  = var.zone
  user_project_override = true
  billing_project       = var.nodes["nanbingjun"].project_id
  credentials           = try(var.credentials_files["nanbingjun"], "") != "" ? var.credentials_files["nanbingjun"] : null
  access_token          = try(var.access_tokens["nanbingjun"], "") != "" ? var.access_tokens["nanbingjun"] : null
}

provider "google" {
  alias                 = "nanheishun"
  project               = var.nodes["nanheishun"].project_id
  region                = var.region
  zone                  = var.zone
  user_project_override = true
  billing_project       = var.nodes["nanheishun"].project_id
  credentials           = try(var.credentials_files["nanheishun"], "") != "" ? var.credentials_files["nanheishun"] : null
  access_token          = try(var.access_tokens["nanheishun"], "") != "" ? var.access_tokens["nanheishun"] : null
}

provider "google" {
  alias                 = "nanzhiyan"
  project               = var.nodes["nanzhiyan"].project_id
  region                = var.region
  zone                  = var.zone
  user_project_override = true
  billing_project       = var.nodes["nanzhiyan"].project_id
  credentials           = try(var.credentials_files["nanzhiyan"], "") != "" ? var.credentials_files["nanzhiyan"] : null
  access_token          = try(var.access_tokens["nanzhiyan"], "") != "" ? var.access_tokens["nanzhiyan"] : null
}
