from flask import Flask

import fastbook
fastbook.setup_book()

#hide
from fastbook import *
from fastai.vision.all import *
from utils import *
from downloadFromGoogleDrive import GoogleDriveDownloader

from flask import request, redirect, render_template

import os, sys
app = Flask(__name__)

GOOGLE_DRIVE_MODEL_FILE_ID = '1Z3SvYdGNR_k7yrtGWgU73r2W_tMVL3XE'
# to get this click on share with people and copy link 
# Model location : https://drive.google.com/file/d/1Z3SvYdGNR_k7yrtGWgU73r2W_tMVL3XE/view?usp=sharing


app.config["IMAGE_UPLOADS"] = "img"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
model = None

@app.route("/")
def upload_image():
    # return "hello world"
    return render_template("index.html")


@app.route("/classify", methods=["POST"])
def classify():
    if request.files:
        image = request.files["image"]
        filename = image.filename
      
        img_path = os.path.join(app.config["IMAGE_UPLOADS"], filename)
        image.save(img_path)
        print(f"Image saved @ : {img_path}")
        res = model.predict(img_path)
        Prediction_Result = {}
        Prediction_Result["label"] = res[0]
        probabilities = ["%.4f" % float(e) for e in list(res[2])]
        labels = model.dls.vocab
        Prediction_Result["result"] = list(zip(labels, probabilities))
        return Prediction_Result

if __name__ == "__main__":
    if not os.path.exists(app.config["IMAGE_UPLOADS"]):
        sys.path.mkdir(app.config["IMAGE_UPLOADS"])

    path = Path()
    modelLocation = path/"lesson1.pkl"
    googleDrive = GoogleDriveDownloader(GOOGLE_DRIVE_MODEL_FILE_ID, str(modelLocation))
    
    if not modelLocation.exists():
        googleDrive.download_file_from_google_drive()
    
    model = load_learner(modelLocation)
    app.run()
