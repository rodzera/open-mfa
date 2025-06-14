output "alb_dns_name" {
  value = aws_alb.open_mfa_load_balancer.dns_name
}