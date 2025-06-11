terraform {
  backend "s3" {
    bucket  = "open-mfa-tf-state"
    key     = "base.tfstate"
    region  = "us-east-2"
    encrypt = true
  }
}