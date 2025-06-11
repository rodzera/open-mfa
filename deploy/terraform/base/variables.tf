variable "route53_domain" {
  description = "Route 53 hosted domain name"
  type        = string
}

# secrets

variable "admin_user" {
  description = "Value for Flask super admin username"
  type        = string
  sensitive   = true
}

variable "admin_pass" {
  description = "Value for Flask super admin password"
  type        = string
  sensitive   = true
}

variable "redis_pass" {
  description = "Value for redis database password"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Value for Flask secret key"
  type        = string
  sensitive   = true
}

variable "b64_aes_key" {
  description = "Value for b64 AES key"
  type        = string
  sensitive   = true
}