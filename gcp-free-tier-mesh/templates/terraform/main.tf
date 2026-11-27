locals {
  spoke_cidrs = [
    var.nodes["fxzoa2020"].cidr,
    var.nodes["nanbingjun"].cidr,
    var.nodes["nanheishun"].cidr,
    var.nodes["nanzhiyan"].cidr,
  ]
  hub_cidr = var.nodes["btczoa"].cidr
}

# ==============================================================================
# VM #0: btczoa (Redis Server Hub)
# ==============================================================================
module "node_btczoa" {
  source = "./modules/free-tier-node"
  providers = {
    google = google.btczoa
  }

  project_id            = var.nodes["btczoa"].project_id
  region                = var.region
  zone                  = var.zone
  instance_name         = var.nodes["btczoa"].instance_name
  boot_disk_size_gb     = var.boot_disk_size_gb
  vpc_network_name      = var.vpc_network_name
  subnet_name           = var.subnet_name
  subnet_ip_cidr_range  = var.nodes["btczoa"].cidr
  peered_cidrs          = local.spoke_cidrs
  instance_tags         = ["allow-ssh", "redis-server"]
  enable_redis_firewall = true
  ssh_user              = var.ssh_user
  ssh_public_key        = var.ssh_public_key
  billing_account_id    = var.nodes["btczoa"].billing_account_id
  budget_alert_email    = var.nodes["btczoa"].budget_alert_email
}

# ==============================================================================
# VM #1: fxzoa2020 (Monitoring & Slack Alert)
# ==============================================================================
module "node_fxzoa2020" {
  source = "./modules/free-tier-node"
  providers = {
    google = google.fxzoa2020
  }

  project_id           = var.nodes["fxzoa2020"].project_id
  region               = var.region
  zone                 = var.zone
  instance_name        = var.nodes["fxzoa2020"].instance_name
  boot_disk_size_gb    = var.boot_disk_size_gb
  vpc_network_name     = var.vpc_network_name
  subnet_name          = var.subnet_name
  subnet_ip_cidr_range = var.nodes["fxzoa2020"].cidr
  peered_cidrs         = [local.hub_cidr]
  instance_tags        = ["allow-ssh", "coin-trader"]
  ssh_user             = var.ssh_user
  ssh_public_key       = var.ssh_public_key
  billing_account_id   = var.nodes["fxzoa2020"].billing_account_id
  budget_alert_email   = var.nodes["fxzoa2020"].budget_alert_email
}

# ==============================================================================
# VM #2: nanbingjun (BTC DCA & Grid Bots)
# ==============================================================================
module "node_nanbingjun" {
  source = "./modules/free-tier-node"
  providers = {
    google = google.nanbingjun
  }

  project_id           = var.nodes["nanbingjun"].project_id
  region               = var.region
  zone                 = var.zone
  instance_name        = var.nodes["nanbingjun"].instance_name
  boot_disk_size_gb    = var.boot_disk_size_gb
  vpc_network_name     = var.vpc_network_name
  subnet_name          = var.subnet_name
  subnet_ip_cidr_range = var.nodes["nanbingjun"].cidr
  peered_cidrs         = [local.hub_cidr]
  instance_tags        = ["allow-ssh", "coin-trader"]
  ssh_user             = var.ssh_user
  ssh_public_key       = var.ssh_public_key
  billing_account_id   = var.nodes["nanbingjun"].billing_account_id
  budget_alert_email   = var.nodes["nanbingjun"].budget_alert_email
}

# ==============================================================================
# VM #3: nanheishun (Multi DCA & Surge Dip Bots)
# ==============================================================================
module "node_nanheishun" {
  source = "./modules/free-tier-node"
  providers = {
    google = google.nanheishun
  }

  project_id           = var.nodes["nanheishun"].project_id
  region               = var.region
  zone                 = var.zone
  instance_name        = var.nodes["nanheishun"].instance_name
  boot_disk_size_gb    = var.boot_disk_size_gb
  vpc_network_name     = var.vpc_network_name
  subnet_name          = var.subnet_name
  subnet_ip_cidr_range = var.nodes["nanheishun"].cidr
  peered_cidrs         = [local.hub_cidr]
  instance_tags        = ["allow-ssh", "coin-trader"]
  ssh_user             = var.ssh_user
  ssh_public_key       = var.ssh_public_key
  billing_account_id   = var.nodes["nanheishun"].billing_account_id
  budget_alert_email   = var.nodes["nanheishun"].budget_alert_email
}

# ==============================================================================
# VM #4: nanzhiyan (Top20 Tracker & Reserve)
# ==============================================================================
module "node_nanzhiyan" {
  source = "./modules/free-tier-node"
  providers = {
    google = google.nanzhiyan
  }

  project_id           = var.nodes["nanzhiyan"].project_id
  region               = var.region
  zone                 = var.zone
  instance_name        = var.nodes["nanzhiyan"].instance_name
  boot_disk_size_gb    = var.boot_disk_size_gb
  vpc_network_name     = var.vpc_network_name
  subnet_name          = var.subnet_name
  subnet_ip_cidr_range = var.nodes["nanzhiyan"].cidr
  peered_cidrs         = [local.hub_cidr]
  instance_tags        = ["allow-ssh", "coin-trader"]
  ssh_user             = var.ssh_user
  ssh_public_key       = var.ssh_public_key
  billing_account_id   = var.nodes["nanzhiyan"].billing_account_id
  budget_alert_email   = var.nodes["nanzhiyan"].budget_alert_email
}

# ==============================================================================
# Star-Topology VPC Network Peering (Hub: btczoa <-> Spokes: 4 Projects)
# Note: Hub-side peerings are chained with depends_on to avoid GCP API
# "operation in progress on the local or peer network" race conditions.
# ==============================================================================

# Pair 1: btczoa <-> nanbingjun
resource "google_compute_network_peering" "btczoa_to_nanbingjun" {
  provider     = google.btczoa
  name         = "peer-btczoa-to-nanbingjun"
  network      = module.node_btczoa.vpc_self_link
  peer_network = module.node_nanbingjun.vpc_self_link
}

resource "google_compute_network_peering" "nanbingjun_to_btczoa" {
  provider     = google.nanbingjun
  name         = "peer-nanbingjun-to-btczoa"
  network      = module.node_nanbingjun.vpc_self_link
  peer_network = module.node_btczoa.vpc_self_link

  depends_on = [google_compute_network_peering.btczoa_to_nanbingjun]
}

# Pair 2: btczoa <-> nanheishun
resource "google_compute_network_peering" "btczoa_to_nanheishun" {
  provider     = google.btczoa
  name         = "peer-btczoa-to-nanheishun"
  network      = module.node_btczoa.vpc_self_link
  peer_network = module.node_nanheishun.vpc_self_link

  depends_on = [google_compute_network_peering.nanbingjun_to_btczoa]
}

resource "google_compute_network_peering" "nanheishun_to_btczoa" {
  provider     = google.nanheishun
  name         = "peer-nanheishun-to-btczoa"
  network      = module.node_nanheishun.vpc_self_link
  peer_network = module.node_btczoa.vpc_self_link

  depends_on = [google_compute_network_peering.btczoa_to_nanheishun]
}

# Pair 3: btczoa <-> nanzhiyan
resource "google_compute_network_peering" "btczoa_to_nanzhiyan" {
  provider     = google.btczoa
  name         = "peer-btczoa-to-nanzhiyan"
  network      = module.node_btczoa.vpc_self_link
  peer_network = module.node_nanzhiyan.vpc_self_link

  depends_on = [google_compute_network_peering.nanheishun_to_btczoa]
}

resource "google_compute_network_peering" "nanzhiyan_to_btczoa" {
  provider     = google.nanzhiyan
  name         = "peer-nanzhiyan-to-btczoa"
  network      = module.node_nanzhiyan.vpc_self_link
  peer_network = module.node_btczoa.vpc_self_link

  depends_on = [google_compute_network_peering.btczoa_to_nanzhiyan]
}

# Pair 4: btczoa <-> fxzoa2020
resource "google_compute_network_peering" "btczoa_to_fxzoa2020" {
  provider     = google.btczoa
  name         = "peer-btczoa-to-fxzoa2020"
  network      = module.node_btczoa.vpc_self_link
  peer_network = module.node_fxzoa2020.vpc_self_link

  depends_on = [google_compute_network_peering.nanzhiyan_to_btczoa]
}

resource "google_compute_network_peering" "fxzoa2020_to_btczoa" {
  provider     = google.fxzoa2020
  name         = "peer-fxzoa2020-to-btczoa"
  network      = module.node_fxzoa2020.vpc_self_link
  peer_network = module.node_btczoa.vpc_self_link

  depends_on = [google_compute_network_peering.btczoa_to_fxzoa2020]
}
