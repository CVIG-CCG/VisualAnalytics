import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

st.title('Example - 3 - Restaurant Tips Analysis')

tips = px.data.tips()
if st.checkbox('Show Data'):
    st.write(tips)

st.subheader('Visualization bar charts')
label = st.selectbox('Which label do you want to visualize ', ['total_bill', 'tip'])
x = st.selectbox('Pick the x variable:', ['sex', 'smoker', 'day', 'time', 'size'])
tips = tips.sort_values('size')
fig = px.bar(tips, x = x, y=label, height=400)
st.plotly_chart(fig)

if st.checkbox('Want to group with respect to another variables?'):
    group1 = st.selectbox('Pick the group variable:', ['smoker', 'day', 'time', 'size', 'sex'])
    fig1 = px.bar(tips, x=x, y=label, color=group1, barmode='group', height=400)
    st.plotly_chart(fig1)

if st.checkbox('Want to group with respect to another variable?'):
    group2 = st.selectbox('Pick the group variable:', ['smoker', 'day', 'time', 'sex'])
    fig2 = px.bar(tips, x = x, y= label, color=group2, barmode='group', facet_col=group2, height=400)
    st.plotly_chart(fig2)

st.subheader('Visualizing distribution')
label1 = st.selectbox('Which label do you want to visualized?', ['total_bill', 'tip'])
fig3 = px.histogram(tips, x= label1, hover_data=tips.columns, marginal='box')
st.plotly_chart(fig3)

if st.checkbox('Want to condition the probability ?'):
    group1_d = st.selectbox('Pick the condition variable: ', ['smoker', 'day', 'time', 'size', 'sex'])
    fig4 = px.histogram(tips, x=label1, color=group1_d, marginal='box', hover_data=tips.columns)
    st.plotly_chart(fig4)

if st.checkbox('Want to condition the probability on a future variable?'):
    group2_d = st.selectbox('Pick the condition variable2: ', ['smoker', 'day', 'time', 'size', 'sex'])
    fig5 = px.histogram(tips, x=label1, color=group1_d, facet_col=group2_d, marginal='box', hover_data=tips.columns)
    st.plotly_chart(fig5)

# Machine Learning
tips.replace({'sex':{'Male':0, 'Female':1}, 'smoker':{'No':0, 'Yes':1}}, inplace=True)
days= pd.get_dummies(tips['day'], drop_first=True)
tips = pd.concat([tips, days], axis=1)
times = pd.get_dummies(tips['time'], drop_first=True)
tips = pd.concat([tips, times], axis=1)
tips.drop(['day', 'time'], inplace=True, axis=1)
st.write(tips.head())

st.subheader('Running Regression')
X = st.multiselect('Pick the covariates: ', ['sex', 'smoker', 'size', 'Thur', 'Sat', 'Sun', 'Lunch'])
X = tips[X]
y = st.selectbox('Select the target', ['tip', 'total_bill'])
y = tips[y]

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

if st.checkbox('Show Score'):
    score = model.score(X_test, y_test)
    st.write(f'Score is: {score}')





