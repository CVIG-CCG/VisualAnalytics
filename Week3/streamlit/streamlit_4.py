import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go

st.title('Example - 4 -  Simple Visual Analytics - Iris Classification')

df = pd.read_csv('./Data/iris.csv')

if st.checkbox('Show Dataframe'):
    st.write(df)

st.subheader('Scatter Plot')
species = st.multiselect('Show iris per variety?', df['class'].unique())
col1 = st.selectbox('Which feature on x?', df.columns[0:4])
col2 = st.selectbox('Which feature on y?', df.columns[0:4])

new_df = df[(df['class'].isin(species))]
st.write(new_df)

fig = px.scatter(new_df, x= col1, y=col2, color='class')
st.plotly_chart(fig)

st.subheader('Histogram')
feature = st.selectbox('Which feature?', df.columns[0:4])
new_df2 = df[(df['class'].isin(species))][feature]
fig2 = px.histogram(new_df, x=feature, color='class', marginal='rug')
st.plotly_chart(fig2)

st.subheader('Machine Learning Models')
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC

features = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
labels = df['class'].values
st.write(features)
st.write(labels)

X_train, X_test, y_train,y_test = train_test_split(features, labels, train_size=0.7, random_state=1)

alg = ['Decision Tree', 'Support Vector Machine']
classifier = st.selectbox('Which algorithm?', alg)
if classifier == 'Decision Tree':
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    acc = dtc.score(X_test, y_test)
    st.write('Accuracy:', acc)
    pred_dtc = dtc.predict(X_test)
    cm_dtc = confusion_matrix(y_test, pred_dtc)
    st.write('Confusion Matrix: ', cm_dtc)

elif classifier == 'Support Vector Machine':
    svm = SVC()
    svm.fit(X_train, y_train)
    acc = svm.score(X_test, y_test)
    st.write('Accuracy:', acc)
    pred_svm = svm.predict(X_test)
    cm = confusion_matrix(y_test, pred_svm)
    st.write('Confusion Matrix: ', cm)
