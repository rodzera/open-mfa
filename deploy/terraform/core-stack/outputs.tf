# base stack

output "route53_domain" {
  value = trim(aws_route53_zone.main.name, ".")
}

output "route53_zone_id" {
  value = aws_route53_zone.main.id
}

output "route53_zone_ns" {
  value = aws_route53_zone.main.name_servers
}

output "ecr_repository_url" {
  value = aws_ecr_repository.open_mfa_ecr.repository_url
}

# secrets arns

output "admin_user_arn" {
  value = aws_secretsmanager_secret.admin_user.arn
}

output "admin_pass_arn" {
  value = aws_secretsmanager_secret.admin_pass.arn
}

output "redis_pass_arn" {
  value = aws_secretsmanager_secret.redis_pass.arn
}

output "secret_key_arn" {
  value = aws_secretsmanager_secret.secret_key.arn
}

output "b64_aes_key_arn" {
  value = aws_secretsmanager_secret.b64_aes_key.arn
}