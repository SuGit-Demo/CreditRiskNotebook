from flask import Flask, request, jsonify, render_template
from flask_db2 import DB2 #for DB2 connection
import numpy as np
import pickle
import requests

app = Flask(__name__)
import login #call login.py
model = pickle.load(open('creditrisk.h5','rb'))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    ############################
    dsn_hostname = "98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud"# e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
    dsn_uid = "vjd81886"# e.g. "abc12345"
    dsn_pwd = "OicRrtEgVpnkIaxU"# e.g. "7dBZ3wWt9XN6$o0J"
    
    dsn_driver = "{IBM DB2 ODBC DRIVER}"
    dsn_database = "bludb"            # e.g. "BLUDB"
    dsn_port = "30875"                # e.g. "50000" 
    dsn_protocol = "TCPIP"            # i.e. "TCPIP"
    dsn_security = "SSL"
    
    dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd, dsn_security)
    
    try:
        conn = ibm_db.connect(dsn, "", "")
        print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)        
    except:
        print ("no connection:", ibm_db.conn_errormsg())

    #query_str = f"select * from VJD81886.CUSTOMER where COLUMN_0 = '{input_fruit}'"
    query_str = f"select * from VJD81886.CUSTOMER where Username = '{username}' and Password = '{password}'"
    selectQuery = query_str
    
    #Execute the statement
    selectStmt = ibm_db.exec_immediate(conn, selectQuery)
    
    #Fetch the Dictionary (for the first row only) - replace ... with your code
    output = ibm_db.fetch_tuple(selectStmt)    
    
    #isTrue = login.checkLogin(username,password)    
    
    if output:
        return render_template('index.html')
    else:
        return redirect(url_for('home'))

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
