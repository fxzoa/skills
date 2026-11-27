output "nodes_summary" {
  description = "Summary of all 5 Always Free VM nodes"
  value = {
    btczoa = {
      role       = var.nodes["btczoa"].role
      project_id = module.node_btczoa.project_id
      cidr       = module.node_btczoa.subnet_cidr
      public_ip  = module.node_btczoa.public_ip
      private_ip = module.node_btczoa.private_ip
      ssh        = module.node_btczoa.ssh_command
    }
    fxzoa2020 = {
      role       = var.nodes["fxzoa2020"].role
      project_id = module.node_fxzoa2020.project_id
      cidr       = module.node_fxzoa2020.subnet_cidr
      public_ip  = module.node_fxzoa2020.public_ip
      private_ip = module.node_fxzoa2020.private_ip
      ssh        = module.node_fxzoa2020.ssh_command
    }
    nanbingjun = {
      role       = var.nodes["nanbingjun"].role
      project_id = module.node_nanbingjun.project_id
      cidr       = module.node_nanbingjun.subnet_cidr
      public_ip  = module.node_nanbingjun.public_ip
      private_ip = module.node_nanbingjun.private_ip
      ssh        = module.node_nanbingjun.ssh_command
    }
    nanheishun = {
      role       = var.nodes["nanheishun"].role
      project_id = module.node_nanheishun.project_id
      cidr       = module.node_nanheishun.subnet_cidr
      public_ip  = module.node_nanheishun.public_ip
      private_ip = module.node_nanheishun.private_ip
      ssh        = module.node_nanheishun.ssh_command
    }
    nanzhiyan = {
      role       = var.nodes["nanzhiyan"].role
      project_id = module.node_nanzhiyan.project_id
      cidr       = module.node_nanzhiyan.subnet_cidr
      public_ip  = module.node_nanzhiyan.public_ip
      private_ip = module.node_nanzhiyan.private_ip
      ssh        = module.node_nanzhiyan.ssh_command
    }
  }
}

output "redis_internal_target" {
  description = "Internal IP of VM #0 (btczoa) to set as REDIS_SSH_TARGET / REDIS_REMOTE_HOST on Bot VMs ($0.00 egress)"
  value       = module.node_btczoa.private_ip
}
