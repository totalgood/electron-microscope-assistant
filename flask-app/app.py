'''
to run app, 1st Build Docker image
$ docker build -t keras_flask_app .

# then run it!
$ docker run -it --rm -p 5000:5000 keras_flask_app
'''

import os
import sys

from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil


from PIL import Image
from io import BytesIO


# Declare a flask app
app = Flask(__name__)

    
def model_predict(img, model):
    
    # Preprocessing the image
    img = img.resize((299, 299))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x, mode='tf')
    
    # make prediction
    preds = model.predict(x)
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    
    if request.method == 'POST':
        
        
        # Get the image file from post request
        img = base64_to_pil(request.json)
        
        
        # Make prediction
        preds = model_predict(img, model)

        # define labels
        #class_names = ['Biological', 'Fibres', 'Films_Coated_Surface', 'MEMS_devices_and_electrodes', 'Nanowires', 'Particles', 'Patterned_surface', 'Porous_Sponge', 'Powder', 'Tips']
        
        # sort in reverse order and return top index
        top_1 = preds.argsort()[0][::-1][0] 
        best_match = class_names[top_1]
       
    
        # Serialize the result, you can add additional fields
        #return jsonify(result=best_match, probability=preds)
        return jsonify(result=best_match)
        
    

    return None


if __name__ == '__main__':
    
    # Load trained model
    MODEL_PATH = 'models/transfer_test.hdf5'
    model = load_model(MODEL_PATH)
    
    # define labels
    class_names = ['Biological', 'Fibres', 'Films_Coated_Surface', 'MEMS_devices_and_electrodes', 'Nanowires', 'Particles', 'Patterned_surface', 'Porous_Sponge', 'Powder', 'Tips']
        
    
    print('Model loaded. Check http://127.0.0.1:5000/')
    
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
