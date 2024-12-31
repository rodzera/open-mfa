# open-mfa
[![Python 3.12](https://img.shields.io/badge/python-3.12.x-success.svg)](https://www.python.org/downloads/release/python-3121/)
[![Test and Build](https://github.com/rodzera/open-mfa/actions/workflows/test_and_build.yml/badge.svg?branch=master)](https://github.com/rodzera/open-mfa/actions/workflows/test_and_build.yml) 
[![codecov](https://codecov.io/gh/rodzera/open-mfa/graph/badge.svg?token=98ORTRBHN5)](https://codecov.io/gh/rodzera/open-mfa)

Open-MFA is a demo project that implements an authentication server supporting OTP (One-Time Password), HOTP (HMAC-Based One-Time Password) and TOTP (Time-Based One-Time Password) algorithms. 

## Project Overview

* The authentication server creates a unique session ID for each user, storing it in both a Flask session and a Redis database with 60-minutes expiration. All OTP codes generated for a user are linked to their unique session ID.
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

To run the open-mfa stack locally with docker compose, follow these steps within the `docker-compose` directory:
* Install [docker](https://docs.docker.com/engine/install/) engine
* Rename the `template.env` file to `.env` and fill the variables with real values
* Run: `docker compose up`
* Application will be available at: http://0.0.0.0:8080

Optionally, you can build a local docker image within the `src` directory:
* Run `make` command

## Project Stack

This project was built with the following tech stack:

- [Flask](https://flask.palletsprojects.com/en/stable/) web server. 
- OTP services implemented with [PyOTP](https://github.com/pyauth/pyotp).
- RESTful APIs with [marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) validation.
- [Redis](https://hub.docker.com/_/redis) database support.
- Runtime [logging](https://docs.python.org/3.12/library/logging).
- Unittests with [Pytest](https://docs.pytest.org/en/7.4.x/).
- [Swagger](https://github.com/flasgger/flasgger) documentation.
- [Docker Hub](https://docs.docker.com/docker-hub/) deployment.
- CI/CD pipelines with [GitHub Actions](https://docs.github.com/en/actions).
- Production-ready [Docker Compose](https://docs.docker.com/compose/) setup with [Gunicorn](https://gunicorn.org/).
