from flask import Flask, request, jsonify, render_template
import numpy as np
#import pickle
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    Gender = request.form.get('gender')
    if(Gender=='Female'):
        Gender=0
    else:
        Gender=1
    MStatus = request.form.get('mstatus')
    if(MStatus=='Single'):
        MStatus=0
    else:
        MStatus=1
    Appincome = request.form.get('appincome')
    Coincome = request.form.get('coincome')
    LoanAmount = request.form.get('amount')
    LoanDuration = request.form.get('duration')              
   
    
    ####################### END OF AUTOAI DEPLOYMENT API #######################

    return render_template('index.html', prediction_text='Loan Risk Prediction is $ {}'.format(response_scoring.json()))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080)
    app.run()
