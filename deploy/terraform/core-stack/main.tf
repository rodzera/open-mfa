terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = "us-east-2"
  profile = "terraform"
  default_tags {
    tags = {
      Project   = "open-mfa"
      ManagedBy = "terraform"
    }
  }
}

resource "aws_route53_zone" "main" {
  name = var.route53_domain
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_ecr_repository" "open_mfa_ecr" {
  name = "open-mfa"
  lifecycle {
    prevent_destroy = true
  }
}