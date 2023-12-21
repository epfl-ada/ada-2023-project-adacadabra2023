import sys
import streamlit as st

sys.path.append('.')
from src.web.models import run_query
from src.data.Data import load_data


# Load training data:
df = load_data('Data/web/Train.pkl')
beerstyles = df['1st_Style'].unique()
country = None

trimesters = ['Jan-Apr', 'Apr-Jul','Jul-Oct', 'Oct-Dec']


# load models
model_aut = load_data('web_everything/trees/tree_Autumn.pkl')
model_spr = load_data('web_everything/trees/tree_Spring.pkl')
model_summ = load_data('web_everything/trees/tree_Summer.pkl')
model_wint = load_data('web_everything/trees/tree_Winter.pkl')


# Set Image
st.image('web_everything/figures/map_beer.jpg', width=700)


st.title('What country should you visit next?')

# Selectboxes with beer styles
beer1 = st.selectbox('Select your favourite beerstyle', beerstyles, index=None)
beer2 = st.selectbox('Select your second favourite beerstyle', beerstyles, index=None)
beer3 = st.selectbox('Select your third favourite beerstyle', beerstyles, index=None)

# Selectboxes with the trimester in which you want to travel
trimester = st.selectbox('When would you like to travel?', trimesters, index=None)


# Select the trimester:
if trimester == trimesters[0]:
    country = run_query(model_wint, beer1, beer2, beer3)
elif trimester == trimesters[1]:
    country = run_query(model_spr, beer1, beer2, beer3)
elif trimester == trimesters[2]:
    country = run_query(model_summ, beer1, beer2, beer3)
elif trimester == trimesters[3]:
    country = run_query(model_aut, beer1, beer2, beer3)
    
# st.write(f'The country we recommend you to go is... {country[0]}')

if country is not None:
    st.markdown("""
    <style>
    .big-font {
        font-size:40px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<p class="big-font">The country we recommend you to go is... </p>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center;"><p class="big-font"> {country[0]} </p> </div>',  unsafe_allow_html=True)
