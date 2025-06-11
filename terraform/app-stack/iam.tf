data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ecs_secrets_access" {
  statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = [
      data.terraform_remote_state.base.outputs.admin_user_arn,
      data.terraform_remote_state.base.outputs.admin_pass_arn,
      data.terraform_remote_state.base.outputs.redis_pass_arn,
      data.terraform_remote_state.base.outputs.secret_key_arn,
      data.terraform_remote_state.base.outputs.b64_aes_key_arn
    ]
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "ecs-task-execution-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_policy" "ecs_secrets_access_policy" {
  name   = "ecs-secrets-access-policy"
  policy = data.aws_iam_policy_document.ecs_secrets_access.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_logs" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

resource "aws_iam_role_policy_attachment" "ecs_secrets_policy_attach" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_secrets_access_policy.arn
}