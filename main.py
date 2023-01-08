import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import seaborn as sns
from textblob import TextBlob
import re 
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

st.write("""
# Aplikasi Analisis Sentimen
""")

st.sidebar.header('Data Input')

# Collects user input features into dataframe
uploaded_file = st.sidebar.file_uploader("Upload data", type=["csv","xlsx"])
if uploaded_file is not None:
    inputan = pd.read_excel(uploaded_file)
else:
    def input_user():
        tweet = st.sidebar('tweet')
        data = {'tweet': tweet,}

        features = pd.DataFrame(data, index=[0])
        return features
    

# Combines user input features with entire penguins dataset
# This will be useful for the encoding phase

inputan['vector'] = inputan['Content'].astype(str)

vec = CountVectorizer().fit(inputan['vector'])
vec_transform = vec.transform(inputan['vector'])
print(vec_transform)
x_test = vec_transform.toarray()




# Displays the user input features
st.subheader('Data Input')

if uploaded_file is not None:
    st.write(inputan[['Author','Content']])
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(inputan)

# Reads in saved classification model
load_model = pickle.load(open('model_bayes.pkl', 'rb'))

inputan['sentimen'] = load_model.predict(x_test)
# Apply model to make predictions
if st.button("Klasifikasi"):
  st.subheader('Hasil klasifikasi')
  inputan['sentimen'] = load_model.predict(x_test)
  st.write(inputan[['Author','Content','sentimen']])
  st.write(inputan['sentimen'].value_counts())
  

def convert_inputan(inputan):
# IMPORTANT: Cache the conversion to prevent computation on every rerun
    return inputan.to_csv().encode('utf-8')

csv = convert_inputan(inputan)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='sentiment.csv',
    mime='text/csv',
        )


st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

if st.button("visualisasi"):
  st.subheader('Hasil Visualisasi')
  data = inputan['sentimen'].value_counts()

  plt.figure(figsize=(10, 6))
  plt.bar(['Positive', 'Netral', 'Negative'], data, color=['royalblue','green', 'orange'])
  plt.xlabel('Jenis Sentimen', size=14)
  plt.ylabel('Frekuensi', size=14)

  st.pyplot()
