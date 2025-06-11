resource "aws_secretsmanager_secret" "admin_user" {
  name = "_ADMIN_USER"
}

resource "aws_secretsmanager_secret" "admin_pass" {
  name = "_ADMIN_PASS"
}

resource "aws_secretsmanager_secret" "redis_pass" {
  name = "_REDIS_PASS"
}

resource "aws_secretsmanager_secret" "secret_key" {
  name = "_SECRET_KEY"
}

resource "aws_secretsmanager_secret" "b64_aes_key" {
  name = "_B64_AES_KEY"
}

resource "aws_secretsmanager_secret_version" "admin_user" {
  secret_id     = aws_secretsmanager_secret.admin_user.id
  secret_string = var.admin_user
}

resource "aws_secretsmanager_secret_version" "admin_pass" {
  secret_id     = aws_secretsmanager_secret.admin_pass.id
  secret_string = var.admin_pass
}

resource "aws_secretsmanager_secret_version" "redis_pass" {
  secret_id     = aws_secretsmanager_secret.redis_pass.id
  secret_string = var.redis_pass
}

resource "aws_secretsmanager_secret_version" "secret_key" {
  secret_id     = aws_secretsmanager_secret.secret_key.id
  secret_string = var.secret_key
}

resource "aws_secretsmanager_secret_version" "b64_aes_key" {
  secret_id     = aws_secretsmanager_secret.b64_aes_key.id
  secret_string = var.b64_aes_key
}