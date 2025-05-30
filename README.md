# open-mfa
[![Python 3.12](https://img.shields.io/badge/python-3.12-success.svg)](https://www.python.org/downloads/release/python-3121/)
[![codecov](https://codecov.io/gh/rodzera/open-mfa/graph/badge.svg?token=98ORTRBHN5)](https://codecov.io/gh/rodzera/open-mfa)
[![Build and Publish Docker Image](https://github.com/rodzera/open-mfa/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/rodzera/open-mfa/actions/workflows/main.yml) 

Open-MFA is a demo project that implements an authentication server supporting OTP (One-Time Password), HOTP (HMAC-Based One-Time Password) and TOTP (Time-Based One-Time Password) algorithms. 

## Project Overview

* The authentication server creates a unique Flask session ID for each user. All OTP codes generated for a user are linked to their unique session ID and stored into a Redis database. Both sessions and OTP codes have a 60-minutes expiration. 
* For properly validating HOTP and TOTP codes, URIs should be transformed into QR Code using tools like [2FA-QR](https://stefansundin.github.io/2fa-qr). These QR codes can then be scanned with any authenticator app, such as [Google Authenticator](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2), which supports OTP algorithms generation.
* In a real-world authentication server, the Identity and Access Management (IAM) would be much more robust and complex, however for demo purposes, this application has been deliberately simplified.

## OTP Algorithms

* OTP algorithms use hash functions (like HMAC-SHA1) that receives two inputs: a **seed** and a **moving factor**.
* The seed is a static and non-guessable secret that may be shared with the client in HOTP and TOTP implementations, but must always be securely stored by the authentication server. 
* The moving factor is a dynamic value that must be distinct for each OTP code generation. This value, combined with the seed, produces different OTP codes for each authentication request.
* Different OTP implementations exist due to variations in how the moving factor is generated and whether the HMAC secret is shared with the client.
* While there are RFCs for HOTP ([RFC 4226](https://datatracker.ietf.org/doc/html/rfc4226)) and TOTP ([RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238)), there is no specific RFC for a "pure" OTP implementation. However, such implementations may be the most common on the world wide web today, often found in scenarios like email verification or temporary login codes. Despite their widespread use, any "pure" OTP implementation **should** still follow the security guidelines outlined in the HOTP and TOTP specs.

### General and common best practices for all algorithms

* All implementations **must** use HTTPS to secure communication between the authentication server and the client.
* The authentication server **must** randomly generate OTP HMAC secrets at the hardware level, or using a cryptographically strong pseudorandom generators.
* The authentication server **must** securely store OTP HMAC secrets in a controlled access database.
* The authentication server **must** throttle (rate limit) brute-force attacks.
* The authentication server **must** deny replay attacks by rejecting any already-used OTP code.
* While the HOTP and TOTP specifications recommend using HMAC-SHA1 method, modern and safer methods like HMAC-SHA256 are preferable.

## Running this project

To run the project stack locally with docker compose, follow these steps within the `/deploy` directory:
* Install [docker](https://docs.docker.com/engine/install/) engine.
* Rename the `template.env` file to `.env` and fill the variables with real values.
* Run `chmod +x ./dev/setup.sh` and `sudo ./dev/setup.sh` to install and configure mkcert and hosts file.
* Run `make dev-up` to start the stack.
* The application will be available at: https://app.open-mfa.local

Optionally, you can build a local docker image within the `/src/docker` directory:
* Run `make` command.

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
    - **Development:**
      - [Werkzeug](https://werkzeug.palletsprojects.com/en/stable/) server.
      - [Nginx](https://nginx.org/) and [mkcert](https://github.com/FiloSottile/mkcert) for HTTPS and reverse proxy.
    - **Production:**
      - [Gunicorn](https://gunicorn.org/) server.
