#! /usr/bin/bash

### Automation script to setup a FAST AI supported flask app
git init
python3 -m venv env
source env/bin/activate
echo "setting up files"
touch app.py utils.py .gitignore README.md requirements.txt
echo "installing Flask"
python3 -m pip3 install Flask
echo "installing fastcore"
pip3 install -Uqq fastcore==1.0.9 
echo "installing fastai"
pip3 install -Uqq fastai==1.0.42 
echo "installing fastbook"
pip3 install -Uqq fastbook

echo '''from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()''' > "app.py"

# python3 -m pip freeze > requirements.txt

python3 app.py