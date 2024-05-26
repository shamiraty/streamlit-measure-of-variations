import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import plotly.figure_factory as ff
from scipy.stats import skew,zscore
st.set_page_config(layout="wide")
import numpy as np
from scipy.stats import skew, norm
import plotly.graph_objects as go
import seaborn as sns

#!pip install streamlit pandas plotly scipy numpy

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
load_df = pd.read_csv('dataset.csv')


married=st.sidebar.multiselect(
    "married",
     options=load_df["married"].unique(),
     default=load_df["married"].unique(),
)
education_level=st.sidebar.multiselect(
    "education_level",
     options=load_df["education_level"].unique(),
     default=load_df["education_level"].unique(),
)
employment=st.sidebar.multiselect(
    "employment",
     options=load_df["employment"].unique(),
     default=load_df["employment"].unique(),
)

df=load_df.query(
    "married==@married & education_level==@education_level & employment ==@employment"
)


std_dev = df['age'].std()
variance = df['age'].var()
quartile_deviation = (df['age'].quantile(0.75) - df['age'].quantile(0.25)) / 2
skewness = skew(df['age'])
max_age = df['age'].max()
min_age = df['age'].min()
std_dev = df['age'].std()
variance = df['age'].var()


col5, col6, col7, col8 = st.columns(4)
with col5:
    st.metric(label="Standard Deviation", value=f"{std_dev:.2f}")
with col6:
    st.metric(label="Variance", value=f"{variance:.2f}")
with col7:
    st.metric(label="Quartile Deviation", value=f"{quartile_deviation:.2f}")
with col8:
    st.metric(label="Skewness", value=f"{skewness:.2f}")
style_metric_cards(border_left_color="#103F7A",box_shadow=True,border_color="gray")

# Kernel Density Estimate (KDE) for PDF
st.subheader('Age Probability Density Function (PDF) NORMAL CURVE')
kde = sns.kdeplot(df['age'], bw_adjust=0.5).get_lines()[0].get_data()
fig_pdf = go.Figure()

# Normal distribution curve
x_values = np.linspace(min_age, max_age, 100)
normal_pdf = norm.pdf(x_values, df['age'].mean(), df['age'].std())

fig_pdf.add_trace(go.Scatter(x=x_values, y=normal_pdf, mode='lines', name='Normal Distribution', line=dict(color='blue')))
 
# Highlight outliers using z-scores
z_scores = zscore(df['age'])
outliers = df[(z_scores < -3) | (z_scores > 3)]
fig_pdf.add_trace(go.Scatter(x=outliers['age'], y=[0]*len(outliers), mode='markers', name='Outliers', marker=dict(color='red', size=10)))

# Add legend entries for z-scores ±3 without vertical lines
fig_pdf.add_trace(go.Scatter(x=[None], y=[None], mode='markers', name='Z-score > +3 or < -3', marker=dict(color='red', size=10)))

b1,b2=st.columns(2)
fig_pdf.update_layout(title='Probability Density Function (PDF) of Age', xaxis_title='Age', yaxis_title='Density', showlegend=True)
st.plotly_chart(fig_pdf,use_container_width=True)



# Highlight outliers
st.subheader('Outliers')
st.dataframe(outliers,use_container_width=True)
st.subheader('Z score Values')
st.dataframe(z_scores,use_container_width=True)