import sys
import streamlit as st

sys.path.append('.')
from src.web.models import run_query
from src.data.Data import load_data


# TODO:
df = load_data('Data/web/Train.pkl')
beerstyles = df['1st_Style'].unique()


trimesters = ['Jan-Apr', 'Apr-Jul','Jul-Oct', 'Oct-Dec']


# load models
model_aut = load_data('web_everything/trees/tree_Autumn.pkl')
model_spr = load_data('web_everything/trees/tree_Spring.pkl')
model_summ = load_data('web_everything/trees/tree_Summer.pkl')
model_wint = load_data('web_everything/trees/tree_Winter.pkl')


st.title('What country should you visit next?')

# Selectboxes with beer styles
beer1 = st.selectbox('Select your favourite beerstyle', beerstyles)
beer2 = st.selectbox('Select your second favourite beerstyle', beerstyles)
beer3 = st.selectbox('Select your third favourite beerstyle', beerstyles)

# Selectboxes with the trimester in which you want to travel
trimester = st.selectbox('When would you like to travel?', trimesters)


# TODO: Call the inference function
if trimester == trimesters[0]:
    country = run_query(model_wint, beer1, beer2, beer3)
elif trimester == trimesters[1]:
    country = run_query(model_spr, beer1, beer2, beer3)
elif trimester == trimesters[2]:
    country = run_query(model_summ, beer1, beer2, beer3)
elif trimester == trimesters[3]:
    country = run_query(model_aut, beer1, beer2, beer3)

st.write(country)