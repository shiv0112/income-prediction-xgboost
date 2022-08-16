class feature_eng:
    train_set = pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', header = None)
    col_labels = ['age', 'workclass', 'fnlwgt', 'education','education_num','marital_status', 'occupation','relationship', 'race', 'sex', 'capital_gain','capital_loss', 'hours_per_week', 'native_country', 'wage_class']
    train_set.columns = col_labels
    def preprocessing(df):
    df['workclass']=np.where(df['workclass']==' Without-pay',' Never-worked',df['workclass'])
    df['workclass']=np.where(df['workclass']==' ?',df['workclass'].mode(),df['workclass'])
    fq = train_set.groupby('workclass').size()/len(train_set)
    df["workclass"]=df["workclass"].map(fq)
    df.drop('education',axis=1,inplace=True)
    fq=train_set.groupby('marital_status').size()/len(train_set)
    df['marital_status']=df['marital_status'].map(fq)
    df['occupation']=np.where(df['occupation']==' ?',train_set['occupation'].mode(),df['occupation'])
    fq=train_set.groupby('occupation').size()/len(train_set)
    df['occupation']=df['occupation'].map(fq)
    fq=train_set.groupby('relationship').size()/len(train_set)
    df['relationship']=df['relationship'].map(fq)
    fq=train_set.groupby('race').size()/len(train_set)
    df['race']=df['race'].map(fq)
    df['sex']=np.where(df['sex']==' Male',0,1)
    df['native_country']=np.where(df['native_country']==' United-States',1,0)
    X_test=df.drop('wage_class',axis=1)
    y_test=df['wage_class']
    X_col=X_test.columns
    X_test=scaler.transform(X_test)
    X_test=pd.DataFrame(X_test,columns=X_col)
    return(X_test,y_test)