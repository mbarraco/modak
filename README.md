# Rate limited email sending module

##  Requirements

We have a Notification system that sends out email notifications of various types (supdatesupdate, daily news, project invitations, etc). We need to protect recipients from getting too many emails, either due to system errors or due to abuse, so let's limit the number of emails sent to them by implementing a rate-limited version of NotificationService.

The system must reject requests that are over the limit.

Some sample notification types and rate limit rules, e.g.:

* Status: not more than 2 per minute for each recipient
* News: not more than 1 per day for each recipient
* Marketing: not more than 3 per hour for each recipient

Etc. these are just samples, the system might have several rate limit rules!# modak


## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Docker and Docker Compose installed

## Installation

Clone the repository to your local machine:

```bash
git clone git@github.com:mbarraco/modak.git
cd modak
```

setup the environment by either
```bash
docker-compose up -d
```
or
```bash
docker compose up -d
```

## Usage

* **Send Emails**: Use the CLI to interactively create and send emails.
* **Create Notification Config**: Define rate limits for email notifications through the CLI.
* **View configuratios**n: List all existing email notification configurations with the CLI.
* **Mail server for testing**: emails sent via the CLI are captured by MailHog, a mock SMTP server.
Access MailHog Web Interface: View and manage test emails at http://127.0.0.1:8025/.


run the cli
```bash
make run-cli
```

### Accessing Mailhog Web interface
[http://127.0.0.1:8025/](http://127.0.0.1:8025/)

## Run tests
```bash
make run-tests
```