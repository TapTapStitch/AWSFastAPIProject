provider "aws" {
  region = var.region
  default_tags {
    tags = {
      app = var.app_name
    }
  }
}

module "network" {
  source   = "./network"
  app_name = var.app_name
  region   = var.region
}

module "ecs" {
  source             = "./ecs"
  app_name           = var.app_name
  region             = var.region
  image              = var.image
  aws_access_key_id  = var.aws_access_key_id
  aws_secret_access_key = var.aws_secret_access_key
  jwt_secret         = var.jwt_secret
  client_id          = var.client_id
  client_secret      = var.client_secret
  table_name         = var.table_name
  vpc_id             = module.network.vpc.id
  public_subnet_ids  = [for s in module.network.public_subnets : s.id]
  private_subnet_ids = [for s in module.network.private_subnets : s.id]
  depends_on         = [module.network]
}


# Outputs
output "alb_dns_name" {
  value = module.ecs.alb_dns_name
}
