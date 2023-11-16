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

setup the environment
```bash
docker-compose up -d
```
## Usage
The CLI tool in this project provides an interactive way to send test emails which can be viewed using the MailHog server. To use the CLI, run make run-cli from the terminal. This will prompt you to enter details for the email you wish to send, including the recipient's address, the email subject, and body. After you've inputted these details, the CLI will send the email, which is intercepted by the MailHog server for testing purposes.

To view the sent emails, open a web browser and navigate to the MailHog web interface at http://127.0.0.1:8025/. Here, you'll see an inbox-like interface where all emails captured by MailHog are displayed. This setup is particularly useful for developers and testers who need to verify email functionalities in applications without sending actual emails to real addresses.

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