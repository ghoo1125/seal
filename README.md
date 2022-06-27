# seal
Line Bot with Messaging API and FastAPI server deployed on Heroku

# Environment Setup

## Clone seal
```
$git clone https://github.com/ghoo1125/seal
```

## Create python3 virtual environment
```
$cd seal
$python3 -m venv .venv
$source .venv/bin/activate # or use vscode to select correct venv
```

## Install required packages
```
$(venv) pip install --upgrade pip
$(venv) pip install -r requirements.txt
```

# Run Server in Local
```
$(venv) uvicorn src.server:app --port 8080 --reload
```
Then you can see the result by typing localhost:8080 at your browser.

## Hook with line server with ngrok:
```
$(venv) ngrok http 8080
```
Then goto Line Messaging API page to update the webhook with ngrok forwarding url.

## Run local mongodb server with docker (deprecated)
```
$docker-compose -f docker/docker-compose.yaml up -d
```

# Developemnt

## Generate requirements.txt after adding new pacakge
```
pip freeze > requirements.txt
```

# CI/CD

Once PR is merged into master branch, it will trigger github actions and deployed to heroku after tests are all passed. The application is served on dynamic port decided by heroku default 443 for HTTPS.