from keras.preprocessing import image
import numpy as np
img_width, img_height = 224, 224
!pip install flask-ngrok
!pip install flask-bootstrap
!pip install flask-cors
from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response
from flask_ngrok import run_with_ngrok
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
import os
from google.colab import drive
from tensorflow.keras.models import load_model
drive.mount('/content/gdrive')
PEOPLE_FOLDER = os.path.join('static','people_photo')

app = Flask(__name__, template_folder='/content/static')
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'
