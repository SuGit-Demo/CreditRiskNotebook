from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import requests

app = Flask(__name__)
import login #call login.py
model = pickle.load(open('creditrisk.h5','rb'))

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
   
    ##Test model prediction with static data. Reshape to change to 2D array 
    testdata = np.reshape([
    Gender,
    MStatus, #Married. Change to 0 to get No Risk. Chane to 1 to get Risk
    None,
    None,
    None,
    Appincome,
    Coincome,
    LoanAmount,
    LoanDuration,
    None,
    None,
    None
    ],(1, -1))

    pred_result = model.predict(testdata)

    if(pred_result[0]==0):
        txt = 'No Risk Loan'
    else:
        txt = 'Risky Loan'
    print(txt)
    

    return render_template('index.html', prediction_text='Loan Risk Prediction is $ {}'.format(txt))

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080)
    app.run()
