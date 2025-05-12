# stock-check

Check the stock of items from a URL.

## Pre-reqs

- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html)
- [rye](https://rye.astral.sh/)

## Build

Sync rye and run sam build with rye's requirements.lock.

```bash
rye run sam-build
```

## Run Locally

```bash
sam local invoke --event resources/event1.json
```

## Deploy

```bash
# First time
sam deploy --guided

# All other times (Once samconfig.toml has your saved answers from a guided deploy.)
sam deploy
```
