import streamlit as st
import pandas as pd
import plotly.express as px
from statistics import mode, median
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_elements import elements
st.set_page_config(layout="wide")
 

#pip install streamlit-elements==0.1.*
#https://github.com/okld/streamlit-elements

#pip install streamlit-pills
#https://github.com/jrieke/streamlit-pills

#pip install streamlit-extras
#https://github.com/arnaudmiribel/streamlit-extras


#all graphs we use custom css not streamlit 
theme_plotly = None 

with st.sidebar:
       st.header("DASHBOARD")
# Custom CSS for sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #103F7A;
    }
    [data-testid="stSidebar"] * {
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.title('DATA SCIENCE')
df = pd.read_csv('dataset.csv')


married=st.sidebar.multiselect(
    "married",
     options=df["married"].unique(),
     default=df["married"].unique(),
)
education_level=st.sidebar.multiselect(
    "education_level",
     options=df["education_level"].unique(),
     default=df["education_level"].unique(),
)
employment=st.sidebar.multiselect(
    "employment",
     options=df["employment"].unique(),
     default=df["employment"].unique(),
)

df_selection=df.query(
    "married==@married & education_level==@education_level & employment ==@employment"
)


with st.expander("VIEW EXCEL DATASET"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=[])
        st.dataframe(df_selection[showData],use_container_width=True)

try: 
 max_age = df_selection['age'].max()
 min_age = df_selection['age'].min()
 mode_age = mode(df_selection['age'])
 median_age = median(df_selection['age'])
except:
     st.error("Error")
try:
 a1,a2,a3,a4=st.columns(4)
 a1.metric(label="Min Age", value=min_age)
 a2.metric(label="Max Age", value=max_age)
 a3.metric(label="Mode Age", value=mode_age)
 a4.metric(label="Median Age", value=median_age)     
 style_metric_cards(border_left_color="#103F7A",box_shadow=True,border_color="gray")
except:
     st.error("Error")

b1,b2=st.columns([1, 1]) 

b1.subheader('SIMPLE BAR GRAPH')
age_counts = df_selection['age'].value_counts().sort_index()
fig = px.bar(age_counts, x=age_counts.index, y=age_counts.values, labels={'x': 'Age', 'y': 'Frequency'}, title='Age by Frequency')
b1.plotly_chart(fig,use_container_width=True)
 



try:
 b2.subheader('BOX PLOT')
 fig_box = px.box(df_selection, y='age', title='Age Distribution')
 b2.plotly_chart(fig_box)
except:
     st.error("Error")


 
 
 

 

     