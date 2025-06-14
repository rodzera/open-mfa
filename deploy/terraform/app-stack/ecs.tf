resource "aws_ecs_cluster" "open_mfa_cluster" {
  name = "open-mfa-cluster"
}

resource "aws_ecs_service" "open_mfa" {
  name            = "open-mfa-service"
  cluster         = aws_ecs_cluster.open_mfa_cluster.id
  task_definition = aws_ecs_task_definition.open_mfa.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  deployment_controller {
    type = "ECS"
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.open_mfa_sg.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn
    container_name   = "open-mfa"
    container_port   = 8080
  }

  depends_on = [aws_lb_listener.https]
}

resource "aws_ecs_task_definition" "open_mfa" {
  family                   = "open-mfa-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = "open-mfa"
      image = data.terraform_remote_state.base.outputs.ecr_repository_url
      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
        }
      ],
      secrets = [
        {
          name      = "_ADMIN_USER"
          valueFrom = data.terraform_remote_state.base.outputs.admin_user_arn
        },
        {
          name      = "_ADMIN_PASS"
          valueFrom = data.terraform_remote_state.base.outputs.admin_pass_arn
        },
        {
          name      = "_REDIS_PASS"
          valueFrom = data.terraform_remote_state.base.outputs.redis_pass_arn
        },
        {
          name      = "_SECRET_KEY"
          valueFrom = data.terraform_remote_state.base.outputs.secret_key_arn
        },
        {
          name      = "_B64_AES_KEY"
          valueFrom = data.terraform_remote_state.base.outputs.b64_aes_key_arn
        },
      ],
      environment = [
        {
          name  = "_REDIS_HOST"
          value = "localhost"
        }
      ],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/open-mfa",
          awslogs-region        = "us-east-2",
          awslogs-stream-prefix = "open-mfa"
        }
      }
    },
    {
      name  = "redis"
      image = "redis:7.4.1-alpine"
      portMappings = [
        {
          containerPort = 6379
          hostPort      = 6379
        }
      ],
      secrets = [
        {
          name      = "REDIS_PASS"
          valueFrom = data.terraform_remote_state.base.outputs.redis_pass_arn
        }
      ],
      command = [
        "sh", "-c", "redis-server --requirepass \"$REDIS_PASS\""
      ],
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = "/ecs/open-mfa",
          awslogs-region        = "us-east-2",
          awslogs-stream-prefix = "redis"
        }
      }
    },
  ])
}