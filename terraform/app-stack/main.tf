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

data "terraform_remote_state" "base" {
  backend = "s3"
  config = {
    bucket  = "open-mfa-tf-state"
    key     = "base.tfstate"
    region  = "us-east-2"
    encrypt = true
  }
}