from tensorflow.keras.preprocessing import image
import numpy as np
img_width, img_height = 224, 224
#pip install flask-ngrok
#pip install flask-bootstrap
#pip install flask-cors
from flask import Flask, render_template, url_for, request, redirect, jsonify, make_response
from flask_ngrok import run_with_ngrok
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
import os
#from google.colab import drive
from tensorflow.keras.models import load_model
#drive.mount('/content/gdrive')
PEOPLE_FOLDER = os.path.join('static','people_photo')

app = Flask(__name__, template_folder='/content/static')
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'
run_with_ngrok(app)
dir = "10_food_classes_10_percent"

train_dir = dir+"/train"
test_dir = dir+"/test"
import tensorflow as tf

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
train_data_10_percent = tf.keras.preprocessing.image_dataset_from_directory(directory=train_dir, 
                                                                            image_size=IMG_SIZE,
                                                                            label_mode="categorical",
                                                                            batch_size=BATCH_SIZE)
transfer_model = load_model("./transferModel1", compile = True)
#transfer_model.load_weights('my_model_weights.h5')
#Bootstrap(app)
"""
Routes
"""
@app.route('/predict', methods = ['GET', 'POST'])
@cross_origin()
#Load model 
def home():
  #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Shovon.jpg')
  #return render_template('Webp.html',user_image =ful)
  _build_cors_preflight_response()
  prediction = "HII"
  if request.method == 'POST':
    uploaded_file = request.files['img']
    if uploaded_file.filename != '':
      image_path = os.path.join('static')
      uploaded_file.save(uploaded_file.filename)
      # Predict with pre saved model here
      from keras.preprocessing import image
      import numpy as np
      img_width, img_height = 224, 224
      img = image.load_img(uploaded_file.filename, target_size = (img_width, img_height))
      img = image.img_to_array(img)
      img = np.expand_dims(img, axis = 0)
      pre = transfer_model.predict(img)
      prediction = np.argmax(pre, axis = 1)
      prediction = train_data_10_percent.class_names[prediction[0]]
      
   # return response 
  return prediction
def _build_cors_preflight_response():
  response = make_response()
  response.headers.add("Access-Control-Allow-Origin","*")
  response.headers.add("Access-Control-Allow-Headers","*")
  response.headers.add("Access-Control-Allow-Methods","*")
  return response
if __name__ == '__main__':
  app.run()