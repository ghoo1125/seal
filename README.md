# Avbuddy

# Environment Setup

## Clone Avbuddy
```
$git clone https://github.com/ghoo1125/avbuddy 
```

## Create python3 virtual environment
```
$cd avbuddy
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
$(venv) uvicorn src.main.python.avbuddy:app --port 8080 --reload
```

Then you can see the result by typing localhost:8080 at your browser.

# Developemnt

## Generate requirements.txt after adding new pacakge
```
pip freeze > requirements.txt
```
