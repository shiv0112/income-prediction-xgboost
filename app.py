from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
import numpy as np
import pandas as pd
from pickle import load

app=Flask(__name__)

def preprocess(df):
    train_set = pd.read_csv('train_data.csv')
    train_set['workclass']=np.where(train_set['workclass']==' Without-pay',' Never-worked',train_set['workclass'])
    train_set['workclass']=np.where(train_set['workclass']==' ?',train_set['workclass'].mode(),train_set['workclass'])
    train_set['occupation']=np.where(train_set['occupation']==' ?',train_set['occupation'].mode(),train_set['occupation'])    
    col_labels = ['age', 'workclass', 'fnlwgt', 'education_num','marital_status', 'occupation','relationship', 'race', 'sex', 'capital_gain','capital_loss', 'hours_per_week', 'native_country']
    scaler=load(open('scaler.pkl','rb'))
    df=pd.DataFrame(df,columns=col_labels)
    fq = train_set.groupby('workclass').size()/len(train_set)
    df['workclass']=df['workclass'].map(fq)
    fq=train_set.groupby('marital_status').size()/len(train_set)
    df['marital_status']=df['marital_status'].map(fq)
    fq=train_set.groupby('occupation').size()/len(train_set)
    df['occupation']=df['occupation'].map(fq)
    fq=train_set.groupby('relationship').size()/len(train_set)
    df['relationship']=df['relationship'].map(fq)
    fq=train_set.groupby('race').size()/len(train_set)
    df['race']=df['race'].map(fq)
    df['sex']=np.where(df['sex']==' Male',0,1)
    df['native_country']=np.where(df['native_country']==' United-States',1,0)
    df=scaler.transform(df)
    df=pd.DataFrame(df,columns=col_labels)
    return(df)

@app.route('/',methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
@cross_origin()
def index():
    try:
        age=float(request.form['age'])
        wrkcls=str(request.form['wrkcls'])
        fnlwgt=float(request.form['fnlwgt'])
        education_num=str(request.form['education_num'])
        marital_status=str(request.form['marital_status'])
        occupation=str(request.form['occupation'])
        relationship=str(request.form['relationship'])
        race=str(request.form['race'])
        sex=str(request.form['sex'])
        cap_gain=float(request.form['cap_gain'])
        cap_loss=float(request.form['cap_loss'])
        hourspweek=float(request.form['hourspweek'])
        native_count=str(request.form['native_count'])
        final_arr=np.array([[age, wrkcls, fnlwgt, education_num, marital_status, occupation,relationship, race, sex, cap_gain, cap_loss,hourspweek, native_count]])
        model=load(open('model.pkl','rb'))
        prediction=model.predict(preprocess(final_arr))
        if prediction[0]==0:
            prediction="less than $50K."
        else:
            prediction="more than $50K."
        return render_template('results.html',prediction=prediction)
    except Exception as e:
        print('The Exception message is: ',e)
        return 'Something went Wrong. Go back and try again.'


if __name__=="__main__":
    app.run(debug=True)