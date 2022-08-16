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
        sibsp=float(request.form['sibsp'])
        parch=float(request.form['parch'])
        fare=float(request.form['fare'])
        pclass=float(request.form['pclass'])
        sex=float(request.form['sex'])
        a1=np.array([0.0,0.0,0.0])
        a2=np.array([0.0,0.0])
        a1[int(pclass)-1]=1.0
        a2[int(sex)-1]=1.0
        a3=np.append(a1,a2)
        final_arr=np.append([age,sibsp,parch,fare],a3)
        model=load(open("dtree.pkl",'rb'))
        prediction=model.predict([final_arr])
        if(prediction[0]==0):
            prediction=" not Survive"
        else:
            prediction="Survive"
        return render_template('results.html',prediction=prediction)
    except Exception as e:
        print('The Exception message is: ',e)
        return 'Something Went Wrong. Go back and try again.'


if __name__=="__main__":
    app.run(debug=True)