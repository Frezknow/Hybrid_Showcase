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
from flaskext.mysql import MySQL
import os
import time
import json
#from google.colab import drive
from tensorflow.keras.models import load_model
#drive.mount('/content/gdrive')
PEOPLE_FOLDER = os.path.join('static','people_photo')

app = Flask(__name__, template_folder='/content/static')
cors = CORS(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'test'
app.config['MYSQL_DATABASE_DB'] = 'dev'
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
mysql.init_app(app)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'
#run_with_ngrok(app)
dir = "10_food_classes_10_percent"

train_dir = dir+"/train"
test_dir = dir+"/test"
import tensorflow as tf


IMG_SIZE = (224, 224)
BATCH_SIZE = 32
train_data_10_percent = tf.keras.preprocessing.image_dataset_from_directory(directory=train_dir, 
                                                                            image_size=IMG_SIZE,                                                                           label_mode="categorical",
                                                                            batch_size=BATCH_SIZE)
transfer_model = load_model("./transferModel1", compile = True)
#transfer_model.load_weights('my_model_weights.h5')
Bootstrap(app)
"""
Routes
"""
@app.route('/predict', methods = ['GET', 'POST'])
@cross_origin()
#Load model 
def home():
  #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Shovon.jpg')
  #return render_template('Webp.html',user_image =ful)
  #connection = create_connection("127.0.0.1","root","test")
  _build_cors_preflight_response()
  prediction = "HII"
  if request.method == 'POST'  or request.method == 'OPTIONS':
    uploaded_file = request.files['img']
    if uploaded_file.filename != '':
      ms = round(time.time() * 1000)
      image_path = os.path.join('static',str(ms))
      uploaded_file.save(image_path)
      # Predict with pre saved model here
      from keras.preprocessing import image
      import numpy as np
      img_width, img_height = 224, 224
      img = image.load_img(image_path, target_size = (img_width, img_height))
      img = image.img_to_array(img)
      img = np.expand_dims(img, axis = 0)
      pre = transfer_model.predict(img)
      prediction = np.argmax(pre, axis = 1)
      prediction = train_data_10_percent.class_names[prediction[0]]
      try:
       conn = mysql.connect()
       cursor = conn.cursor()
       cursor.execute("INSERT INTO predictions(prediction,img) VALUES (%s, %s)",(prediction,image_path)) 
       conn.commit()
       return json.dumps({"prediction":prediction,"Img":image_path})
      except Exception as e:
       print(e)
       return
  # return response 
  return 
def _build_cors_preflight_response():
  response = make_response()
  response.headers.add("Access-Control-Allow-Origin","*")
  response.headers.add("Access-Control-Allow-Headers","*")
  response.headers.add("Access-Control-Allow-Methods","*")
  return response
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5052)