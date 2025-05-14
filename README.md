# 📦 stock-check

> Check the stock of items from a URL.

## ✨ Features

- ✅ Serverless - Runs in AWS serverless infrastructure.
- ✅ Site Checks - Check a remote site for a match.
- ✅ Scheduled - Run the checks on a schedule.
- ✅ Logging - Each execution is logged.
- ✅ Alerting - Get AWS SNS alerts when there is a match.

## 🛠 Installation

### Pre-reqs

- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html)
- [rye](https://rye.astral.sh/)

### Build

Sync rye and run sam build with rye's requirements.lock. (By default, sam will lock for requirements.txt, unless told otherwise via the `--manifest` flag.)

```bash
rye run sam-build
```

## 🚀 Usage

### Run Locally

```bash
sam local invoke --event resources/event1.json
```

### Deploy to AWS

```bash
# First time
sam deploy --guided

# All other times (Once samconfig.toml has your saved answers from a guided deploy.)
sam deploy
```

## ⚙️ Configuration

The configurable key values used as events:

- `url`: The remote URL to HTTP GET.
- `headers`: Any headers to send. The example event has a user agent configured to avoid some sites that block scripted signatures.
- `match`: The string to check for in the text of the returned HTTP GET request.
- `match_description`: Used in log messages and SNS alerts to describe the item searched for.

The events can be changed in two places:

- resources/ : Events for local invoke testing.
- template.yaml : The events that will be deployed as schedules to your AWS account.

## 🐞 Known Issues

- ❗ When run via `sam local invoke`, there is no SNS topic to publish to for alerting on a match. This will throw an exception.
