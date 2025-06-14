# open-mfa
[![Python 3.12](https://img.shields.io/badge/python-3.12-success.svg)](https://www.python.org/downloads/release/python-3121/)
[![codecov](https://codecov.io/gh/rodzera/open-mfa/graph/badge.svg?token=98ORTRBHN5)](https://codecov.io/gh/rodzera/open-mfa)
[![GH Actions Badge](https://github.com/rodzera/open-mfa/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/rodzera/open-mfa/actions/workflows/main.yml) 

Open-MFA is a demo project that implements an authentication server supporting OTP (One-Time Password), HOTP (HMAC-Based One-Time Password) and TOTP (Time-Based One-Time Password) algorithms. 

## Project Overview

* The authentication server creates a unique Flask session ID for each user. All OTP codes generated for a user are linked to their unique session ID and stored into a Redis database. Both sessions and OTP codes have a 60-minutes expiration. 
* For properly validating HOTP and TOTP codes, URIs should be converted into QR Code using tools like [2FA-QR](https://stefansundin.github.io/2fa-qr). These QR codes can then be scanned with any authenticator app, such as [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2), which supports OTP algorithms generation.
* In a real-world authentication server, the Identity and Access Management (IAM) would be much more robust and complex, however for demo purposes, this application has been deliberately simplified.

## OTP Algorithms

* OTP algorithms use hash functions (like HMAC-SHA1) that receive two inputs: a **seed** and a **moving factor**.
* The seed is a static and non-guessable secret that may be shared with the client in HOTP and TOTP implementations, but must always be securely stored by the authentication server. 
* The moving factor is a dynamic value that must be distinct for each OTP code generation. This value, combined with the seed, produces different OTP codes for each authentication request.
* Different OTP implementations exist due to variations in how the moving factor is generated and whether the HMAC secret is shared with the client.
* While there are RFCs for HOTP ([RFC 4226](https://datatracker.ietf.org/doc/html/rfc4226)) and TOTP ([RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238)), there is no specific RFC for a simplified OTP implementation. However, such implementation may be the most common on the world wide web today, often found in scenarios like email verification or temporary login codes. Despite their widespread use, any simplified OTP implementation **should** still follow the security guidelines outlined in the HOTP and TOTP specs.

### General and common best practices for all algorithms

* All implementations **must** use HTTPS to secure communication between the authentication server and the client.
* The authentication server **must** randomly generate OTP HMAC secrets at the hardware level, or using a cryptographically strong pseudorandom generators.
* The authentication server **must** securely store OTP HMAC secrets in a controlled access database.
* The authentication server **must** deny replay attacks by rejecting any already-used OTP code.
* The authentication server or infrastructure **must** throttle (rate limit) brute-force attacks.
* While the HOTP and TOTP specifications recommend using HMAC-SHA1 method, modern and safer methods like HMAC-SHA256 are preferable.

## Running this project

### Requirements

* Install [Docker](https://docs.docker.com/engine/install/) engine for development and staging deployment.
* Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) and [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) for production deployment.

### Development

Inside `/deploy/docker-compose` directory:
* Rename the `.env.example` file to `.env` and replace the variables with real values.
* Run `chmod +x ./dev/setup.sh` and `sudo ./dev/setup.sh` to install and configure mkcert and hosts file.
* Run `make dev-up` to start the stack.
* The application will be available at: `https://open-mfa.local`

### Staging

Inside `/deploy/docker-compose` directory:
* Rename the `.env.example` file to `.env` and replace the variables with real values.
* Run `make staging-up` to start the stack.
* The application will be available at: `https://${DNS_DOMAIN}`

### Production

* Create an AWS `IAM user` for terraform operations with `AdministratorAccess` policy attached.
* Configure an `AWS CLI profile` using the IAM user credentials.
* Set up `core-stack` module variables file based on `terraform.tfvars.example`.
* Initialize the terraform modules in the following order:
  1. **Bootstrap** - Initializes the S3 remote state backend. This must be created first to store the entire stack's state and cannot be destroyed.
  2. **Core Stack** - Deploys ECR, Route53 hosted zone and application secrets. These are the critical infra components required by CI/CD and the application, and cannot be destroyed.
  3. **App Stack** - Deploys ECS, VPC, ELB, CloudWatch and WAF. This is the application stack that can be destroyed and redeployed at any time.

## Project Stack

This project is a case study demonstrating the use of the following technologies:

- Architecture:
  - RESTful API design.
  - Clean architecture.
  - Layered architecture.
  - Domain-driven design (DDD).
- Backend:
  - [Flask](https://flask.palletsprojects.com/en/stable/) - Web framework.
  - [PyOTP](https://github.com/pyauth/pyotp) - Library for OTP algorithms implementation.
  - [Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) - Library for REST API data validation.
  - [Redis](https://hub.docker.com/_/redis) - Database for OTP storage.
  - [Python Logging](https://docs.python.org/3.12/library/logging) - Configurable runtime logging.
  - [Pytest](https://docs.pytest.org/en/7.4.x/) and [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) - Unit, integration, and property-based testing.
  - [Flasgger](https://github.com/flasgger/flasgger) - Swagger UI and OpenAPI documentation.
- DevOps:
  - [Codecov](https://about.codecov.io/product/documentation/) - Code coverage reports.
  - [Docker](https://docs.docker.com/) - Services containerization.
  - [GitHub Actions](https://docs.github.com/en/actions) - CI/CD pipelines for testing and deployment.
  - [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) - Public container image registry.
  - [AWS Elastic Container Registry](https://docs.aws.amazon.com/ecr/) - Private container image registry.
  - [Docker Compose](https://docs.docker.com/compose/) - Multi-service orchestration.
    - **Development deployment:**
      - [Werkzeug](https://werkzeug.palletsprojects.com/en/stable/) WSGI server.
      - [Nginx](https://nginx.org/en/docs/) and [mkcert](https://github.com/FiloSottile/mkcert) for HTTPS and reverse proxy.
    - **Staging deployment:**
      - [Gunicorn](https://gunicorn.org/) WSGI production-grade server.
      - [Nginx-proxy](https://hub.docker.com/r/nginxproxy/nginx-proxy) and [letsencrypt](https://hub.docker.com/r/nginxproxy/acme-companion) for HTTPS, reverse proxy and rate-limit.
  - [AWS](https://docs.aws.amazon.com/) and [Terraform](https://developer.hashicorp.com/terraform/docs) - Infrastructure as Code (IaC) for **production deployment**.
    - [S3](https://docs.aws.amazon.com/s3/) - Remote terraform state backend storage.
    - [ECS Fargate](https://docs.aws.amazon.com/ecs/) - Serverless container deployment.
    - [ELB](https://docs.aws.amazon.com/elasticloadbalancing/) - Application Load Balancing.
    - [Route 53](https://docs.aws.amazon.com/route53/) - DNS management and routing.
    - [Cloudwatch](https://docs.aws.amazon.com/cloudwatch/) - Observability for ECS services.
    - [AWS WAF](https://docs.aws.amazon.com/waf/) - Web Application Firewall for rate limiting.
