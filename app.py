# Libraries
import os.path

import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px

# Title
st.title('Orange is the new black')

# Data Fetching
path = os.path.join('data/product.csv')

def load_data(path):
    data = pd.read_csv(path)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

df = load_data(path)

# Visualisation #
# chart_select = st.sidebar.selectbox(
#     label = "Select chart type",
#     options = ['Barchart', 'Histogram']
# )

df_nutriscore = df[df.nutriscore_grade != 0] # delete product with nutriscore = 0

st.subheader('Répartition des jus d’orange par Nutriscore')
plot = px.bar(df_nutriscore.nutriscore_grade, labels={
    "nutriscore_grade": "Nutriscore",
    "count": "Nombre de produits",
},
              title="Répartition des jus d'orange par Nutriscore",
              category_orders={"nutriscore_grade":['a','b','c','d','e']})
st.plotly_chart(plot)

# if chart_select == 'Barchart':
#     st.sidebar.subheader("Barchart settings")
#     try:
#         st.subheader('Répartition des jus d’orange par Nutriscore')
#         x_values = st.sidebar.selectbox('X axis', options=df_nutriscore.columns),
#         y_values = st.sidebar.selectbox('Y axis', options=df_nutriscore.columns),
#         plot = px.bar(df_nutriscore, x_values, y_values, labels={
#             "nutriscore_grade": "Nutriscore",
#             "count": "Nombre de produits",
#         },
#                       title="Répartition des jus d'orange par Nutriscore",
#                       category_orders={"nutriscore_grade":['a','b','c','d','e']})
#         st.plotly_chart(plot)
#     except Exception as e:
#         print(e)


st.subheader('Ratio sucre / Kcal')
sucre = go.Histogram(
    x=df['sugars_100g'],
    opacity=0.75,
    name = "Sucre",
    marker=dict(color='rgba(171, 50, 96, 0.6)'))
kcal = go.Histogram(
    x=df['energy-kcal_100g'],
    opacity=0.75,
    name = "Kcal",
    marker=dict(color='rgba(12, 50, 196, 0.6)'))

data = [sucre, kcal]
layout = go.Layout(barmode='overlay',
                   title='Ratio sucre / kilocalorie',
                   xaxis=dict(title='Ratio sucre / kcal'),
                   yaxis=dict( title='Nombres'))
fig = go.Figure(data=data, layout=layout)
st.plotly_chart(fig)

st.subheader('Taux de sucre pour 100gr')

# delete product with sugars_100g = 0
df_sugars = df[df.sugars_100g != 0]

# create 7 bins starting with 0 up to 50
# bins = np.linspace(0, 50, 7)
bins = np.arange(0, 30, 5)
# use pd.cut to create the bins
df['sugars_100g'] = pd.cut(df['sugars_100g'], bins, include_lowest=True)
# pd.cut creates an interval category which is sorted from lowest bin to the greatest bin
df['sugars_100g'].cat.categories
# count the values in each bin. Bins are sorted based on the occurance (from most populated to the least one)
agg = df['sugars_100g'].value_counts()
# sort the values according to the bins (`sort_index`), turn into data frame (`to_frame`) and reset index
agg = agg.sort_index().to_frame().reset_index()
# rename index (containing the bin range to bins)
agg.rename(columns={"index":"bins"}, inplace=True)
# Plotly cannot work with categories index, so we need to turn it into string
agg["bins"] = agg["bins"].astype("str")

#pie chart
fig_2 = px.pie(agg, values='sugars_100g', names='bins', title="Répartition des produits avec taux de sucre entre 0,0001 et 50 grammes")
st.plotly_chart(fig_2)

st.subheader("Exploration jus d'oranges")
pics = {
    "Marques les plus représentées": "img/brands_logo.jpg",
    "Les jus d'oranges BIO": "img/juice_without.jpg",
    "Les jus d'oranges nutriscore A": "img/nutriA.jpg",
    "Les jus d'oranges nutriscore E": "img/E.jpg",
    "Les jus d'oranges vitamine C": "img/C.jpg"
}

pic = st.selectbox("Picture choices", list(pics.keys()), 0)
st.image(pics[pic], use_column_width=True, caption=pics[pic])