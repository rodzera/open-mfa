resource "aws_wafv2_web_acl" "rate_limit" {
  name  = "rate-limit-acl"
  scope = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "RateLimitRule"
    priority = 1

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 100
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "rateLimit"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "rateLimitACL"
    sampled_requests_enabled   = true
  }
}

resource "aws_wafv2_web_acl_association" "alb_acl" {
  resource_arn = aws_alb.open_mfa_load_balancer.arn
  web_acl_arn  = aws_wafv2_web_acl.rate_limit.arn
}