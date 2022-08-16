from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
import numpy as np
from pickle import load

app=Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
@cross_origin()
def index():
    try:
        age=float(request.form['age'])
        wrkcls=float(request.form['wrkcls'])
        fnlwgt=float(request.form['fnlwgt'])
        education_num=float(request.form['education_num'])
        marital_status=float(request.form['marital_status'])
        occupation=float(request.form['occupation'])
        relationship=float(request.form['relationship'])
        race=float(request.form['race'])
        sex=float(request.form['sex'])
        cap_gain=float(request.form['cap_gain'])
        cap_loss=float(request.form['cap_loss'])
        hourspweek=float(request.form['hourspweek'])
        native_count=float(request.form['native_count'])
        return render_template('results.html',prediction=prediction)
    except Exception as e:
        print('The Exception message is: ',e)
        return 'Something Went Wrong. Go back and try again.'


if __name__=="__main__":
    app.run(debug=True)