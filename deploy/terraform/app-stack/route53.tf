resource "aws_route53_record" "open_mfa" {
  zone_id = data.terraform_remote_state.base.outputs.route53_zone_id
  name    = "app"
  type    = "A"
  alias {
    name                   = aws_alb.open_mfa_load_balancer.dns_name
    zone_id                = aws_alb.open_mfa_load_balancer.zone_id
    evaluate_target_health = true
  }
}

resource "aws_acm_certificate" "open_mfa_cert" {
  domain_name       = "app.${data.terraform_remote_state.base.outputs.route53_domain}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "open_mfa_cert_validation" {
  for_each = {
    for option in aws_acm_certificate.open_mfa_cert.domain_validation_options : option.domain_name => option
  }

  name    = each.value.resource_record_name
  type    = each.value.resource_record_type
  zone_id = data.terraform_remote_state.base.outputs.route53_zone_id
  records = [each.value.resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "open_mfa_cert_validation" {
  certificate_arn         = aws_acm_certificate.open_mfa_cert.arn
  validation_record_fqdns = [for record in aws_route53_record.open_mfa_cert_validation : record.fqdn]
}