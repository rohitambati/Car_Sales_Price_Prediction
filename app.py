import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    print("haio")
    features = [x for x in request.form.values()]

    features[0] = float(features[0])
    features[1] = float(features[1])
    features[2] = float(features[2])
    features[3] = float(features[3])
    features[4] = float(features[4])
    features[5] = int(features[5])

    final_features = [np.array(features)]
    prediction = model.predict(final_features)

    output = round(prediction[0]*1000, 2)

    return render_template('index.html', prediction_text='Car resale value could be: $ {}'.format(output))


if __name__ == "__main__":
    app.run()
