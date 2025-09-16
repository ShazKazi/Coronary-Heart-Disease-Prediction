import pandas as pd 
import numpy as np
import pickle

st=pd.read_csv("Dataset\Heart_disease_statlog.csv")
st=st.drop(['ca','thal'],axis=1)

cl=pd.read_csv('Dataset\heart_cleveland_upload.csv')
cl=cl.drop(['ca','thal'],axis=1)

hn=pd.read_csv('Dataset\heart.csv')
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
columns=['sex','cp','restecg','exang','slope']
for i in columns:
    hn[i]=le.fit_transform(hn[i])

ds=pd.concat([st,cl,hn],axis=0)

x=ds.iloc[:,:-1].values
y=ds.iloc[:,-1].values

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=0)

from catboost import CatBoostClassifier
cb=CatBoostClassifier(iterations=472,depth=9,learning_rate=0.2528024333109265,l2_leaf_reg=8.237257695919375,
                      bagging_temperature=0.24256095707516284,random_seed=42,early_stopping_rounds=50,auto_class_weights='Balanced')

cb.fit(x_train,y_train)

# with open("catboost_model.pkl","wb") as f:
#     pickle.dump(cb,f)

y_pred=cb.predict(x_test)

from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,y_pred))