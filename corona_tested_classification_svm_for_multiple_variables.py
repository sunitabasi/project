# -*- coding: utf-8 -*-
"""corona tested classification svm for multiple variables

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GeMW-a8gRMXBmhf1sQcTmQjKAVUNXi9z
"""

#Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Data Preprocessing
from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, MinMaxScaler

#Models ML
from sklearn.svm import SVC
#Metrics
from sklearn.metrics import confusion_matrix,accuracy_score
# from sklearn.metrics import mean_squared_error,r2_score
# from sklearn.metrics import roc_curve, auc

data = pd.read_csv('corona_tested.csv')
data.head()

row,col = data.shape
print("No of row = ",row)
print("No of col = ",col)

# There is not NaN or null values in columns
data.info()   # incase of huge data we have to drop lowest value

data = data.dropna()

data.shape



data['Cough_symptoms'] = data['Cough_symptoms'].astype('bool').astype('int')
data['Fever'] = data['Fever'].astype('bool').astype('int')
data['Sore_throat'] = data['Sore_throat'].astype('bool').astype('int')
data['Shortness_of_breath'] = data['Shortness_of_breath'].astype('bool').astype('int')
data['Headache'] = data['Headache'].astype('bool').astype('int')
# data['Age_60_above'] = data['Age_60_above'].astype('bool')
# data['Sex'] = data['Sex'].astype.('bool')
# data['Known_contact'] = data['Known_contact'].astype('bool')

data.info()

#data.describe()
data

print(len(data[data['Corona'] == 'other']))
print(len(data[data['Corona'] == 'positive']))
print(len(data[data['Corona']=='negative']))

data = data[data['Corona'] != 'other']
data

data= data.iloc[:,2:]
data

# from sklearn.preprocessing import OrdinalEncoder
# ord_enc = OrdinalEncoder()
# data['Sex'] = ord_enc.fit_transform(data[["Sex"]]).astype('int')
# data['Known_contact'] = ord_enc.fit_transform(data[["Known_contact"]]).astype('int')
# data['Age_60_above'] = ord_enc.fit_transform(data[["Age_60_above"]]).astype('int')
# data['Corona'] = ord_enc.fit_transform(data[["Corona"]]).astype('int')

# we have to use ordinalencoder to convert categorical value
#alternatively
from sklearn.preprocessing import OrdinalEncoder
ord_enc = OrdinalEncoder()
list = ['Sex','Known_contact','Age_60_above','Corona']
for columns in list:
  data[columns]= ord_enc.fit_transform(data[[columns]]).astype('int')

data

# print(len(data[data['TenYearCHD'] == 1]))
# print(len(data[data['TenYearCHD'] == 0]))

df1 = data[data['Corona'] == 1]
print(len(df1))
df2 = data[data['Corona'] == 0].iloc[0:557]
data = pd.concat([df1,df2])
print(len(df2))

data = data.sample(frac = 1)
data

data.columns

#data1 = data.iloc[: ,:-1]

data.corr()

plt.figure(figsize=(16,9))
corr = data.corr()
sns.heatmap(corr, annot=True, cmap='Set3')
plt.show()

# training and normalization of data
X = data[['Cough_symptoms', 'Fever', 'Sore_throat', 'Shortness_of_breath','Headache', 'Age_60_above', 'Sex', 'Known_contact']]
Y = data['Corona']

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.20, random_state=1)

# SScaler = StandardScaler()
# X_train = SScaler.fit_transform(X_train)
# X_test = SScaler.fit_transform(X_test)

# def roc_curve(Y_test, Y_score):
#     from sklearn.metrics import roc_curve, auc
#     fpr, tpr, thresholds = roc_curve(Y_test, Y_score)
#     score = metrics.auc(fpr, tpr)

#     fig = px.area(
#         #fpr = False Positive Rate; tpr= True Positive Rate
#         x=fpr, y=tpr,
#         title=f'ROC Curve (AUC={auc(fpr, tpr):.4f})',
#         labels=dict(x='False Positive Rate', y='True Positive Rate'),
#         width=700, height=500
#     )

#     fig.add_shape(
#         type='line', line=dict(dash='dash'),
#         x0=0, x1=1, y0=0, y1=1
#     )

#     fig.update_yaxes(scaleanchor="x", scaleratio=1)
#     fig.update_xaxes(constrain='domain')
#     fig.show()

from sklearn.svm import SVC
svc= SVC()
svc.fit(X_train,Y_train)

#from sklearn.liner_model

X_test

Y_pred = svc.predict(X_test)
Y_pred

#pd.DataFrame({'Results':list(Y_pred)})

svc_accuracy= round(accuracy_score(Y_test,Y_pred), 4)*100 # Accuracy
svc_accuracy

d = X_test.iloc[0:1]
d

Y_test.iloc[0:1]

Y_pred = svc.predict(X_test.iloc[0:1])
Y_pred

# Pregnancies = float(input("Enter Pregnancies = "))
# Glucose = float(input("Enter Glucose = "))
# BloodPressure = float(input("Enter BloodPressure = "))
# SkinThickness = float(input("Enter SkinThickness = "))
# Insulin = float(input("Enter Insulin = "))
# BMI = float(input("Enter BMI = "))
# DiabetesPedigreeFunction = float(input("Enter DiabetesPedigreeFunction = "))
# Age = float(input("Enter Age = "))

# new_data = {'Pregnancies':[Pregnancies],
#             'Glucose':[Glucose],
#             'BloodPressure':[BloodPressure],
#             'SkinThickness':[SkinThickness],
#             'Insulin':[Insulin],
#             'BMI':[BMI],
#             'DiabetesPedigreeFunction':[DiabetesPedigreeFunction],
#             'Age':[Age]}
# d = pd.DataFrame(new_data)



Y_score = svc.predict(d)
print(Y_score)

Y_pred = svc.predict(X_test)
Y_pred

# def impressions(model,accuracy):
# print('Mean squared error: ', round(mean_squared_error(Y_test,Y_pred),3))
cm=confusion_matrix(Y_test,Y_pred)

class_label = [0, 1]

df_cm = pd.DataFrame(cm, index=class_label,columns=class_label)
sns.heatmap(df_cm,annot=True,cmap='Set2',linewidths=2,fmt='d')
plt.title("Confusion Matrix",fontsize=15)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

cm=confusion_matrix(Y_test,Y_pred)
cm

from sklearn.metrics import classification_report, confusion_matrix
ytest = np.array(Y_test)
print(classification_report(ytest,svc.predict(X_test)))

len(X_test)

Y_pred

Y_test



from sklearn.linear_model import LogisticRegression
log_regression = LogisticRegression()
log_regression.fit(X_train,Y_train)
Y_pred = log_regression.predict(X_test)

lg_accuracy = round(accuracy_score(Y_test,Y_pred),4)*100 #accuracy
lg_accuracy



cm=confusion_matrix(Y_test,Y_pred)

class_label = [0, 1]

df_cm = pd.DataFrame(cm, index=class_label,columns=class_label)
sns.heatmap(df_cm,annot=True,cmap='Set2',linewidths=2,fmt='d')
plt.title("Confusion Matrix",fontsize=15)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

