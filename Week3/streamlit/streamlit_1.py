import streamlit as st
import numpy as np
import pandas as pd
import time

st.title('Example - 1 - Streamlit Basics')

# write normal text
st.subheader('Write text and Data frame')
st.write('text')
# write a data frame
st.write(pd.DataFrame({'first':[1,2,3], 'second':[10,20,30]}))
# magic commands
df = pd.DataFrame({'first':[1,2,3], 'second':[10,20,30]})
df

# Add graph/ chart
st.subheader('Graph')
data = pd.DataFrame(np.random.randn(20,3), columns=['a', 'b', 'c'])
st.line_chart(data=data)

# Plot a map
st.subheader('Map')
map_data = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
st.map(map_data)

# Interactivity
# checkbox
st.subheader('Interactivty')
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['A', 'B', 'C'])
    st.line_chart(chart_data)

# selectbox
option = st.selectbox('which number do you like?', df['first'])
'You selected:', option

# sidebar
st.sidebar.subheader('Sidebar')
option = st.sidebar.selectbox('Which number do you like?', df['first'])
st.sidebar.markdown(f'You selected: {option}')

# slider
st.subheader('Slider')
x = st.slider('x')
st.write(x, 'squared is ', x * x)

st.subheader('Progress')
# Show progress
latest_itteration =st.empty()
bar = st.progress(0)

for i in range(100):
    latest_itteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.1)


