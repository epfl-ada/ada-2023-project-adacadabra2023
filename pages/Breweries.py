# Libraries
import streamlit as st
import pandas as pd
import pickle as pkl
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# Config
st.set_page_config(page_title='Beers Travel Guide', page_icon=':beer:')

# Title
st.title('🏭 What about the breweries?')

st.write(
    """
    The reason for this analysis
    """
)
data_exploration, locorind, best_breweries = st.tabs(['Data exploration', 'Local or Industrial?', 'Best breweries to visit'])

# Load datasets
data_path = os.path.join('/Users/loureiro/Documents/Courses/CS-401_ADA/project_v4_branch/Data', 'Unified_ratings_wo_text.pkl')
with open(data_path, 'rb') as f:
    ratings = pkl.load(f)
data_path = os.path.join('/Users/loureiro/Documents/Courses/CS-401_ADA/project_v4_branch/Data', 'Unified_breweries.pkl')
with open(data_path, 'rb') as f:
    data = pkl.load(f)

with data_exploration:
    st.write(
    """
    Data exploration.....
    """
    )
    
    # Histograms showing the complete distribution of the number of beers per brewery on the left and the number of breweries producing up to 100 beers on the right
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9,2.5), sharex=False, sharey=False, gridspec_kw={'width_ratios':[1,1], 'wspace': 0.3})

    sns.histplot(data=data, x='total_nbr_beers', bins=50, ax=axs[0], color='#4a79a5', edgecolor='#3b6084')
    axs[0].set_xlabel('number of beers', fontsize='11')
    axs[0].set_ylabel('number breweries in log.', fontsize='11')
    axs[0].set_yscale('log')
    axs[0].set_title('All breweries', fontsize='12')
    for label in (axs[0].get_xticklabels() + axs[0].get_yticklabels()):
        label.set_fontsize(9)

    sns.histplot(data=data, x='total_nbr_beers', bins=600, ax=axs[1], color='#cf651d', edgecolor='#a01010')
    axs[1].set_xlim(0,100)
    axs[1].set_xlabel('number of beers', fontsize='11')
    axs[1].set_ylabel('number breweries', fontsize='11')
    axs[1].set_title('Breweries with max. 100 beers', fontsize='12')
    for label in (axs[1].get_xticklabels() + axs[1].get_yticklabels()):
        label.set_fontsize(9)

    #fig.suptitle('Distribution of beers produced by brewery', weight='bold', fontsize='13')

    st.pyplot(fig)

with locorind:
    st.write(
    """
    Explain analysis + plot.....
    """
    )
    #Here we define the threshold for local vs industrial breweries
    # Local breweries < 15
    # Industrial breweries > 15
    data['local_brewery'] = data['total_nbr_beers'].apply(lambda x: True if x < 15 else False)
    
    # Plotting the proportion of local vs industrial breweries per country
    # We filtered out countries having less than 30 breweries for better statistics
    fig, ax = plt.subplots(figsize=(2.1, 6))

    grouped = data.groupby('location').agg({
        'local_brewery': lambda x: x.mean(),
        'name': 'size'
    }).reset_index()
    grouped.sort_values(by='local_brewery', ascending=False, inplace=True)
    grouped['industrial_brewery'] = grouped['local_brewery'] - 1
    grouped = grouped[grouped['name'] > 30]

    plt.rcParams['font.size'] = '6'
    for label in (ax.get_yticklabels()):
        label.set_fontsize(5)

    sns.barplot(data=grouped, y='location', x='local_brewery', color='#058872')
    sns.barplot(data=grouped, y='location', x='industrial_brewery', color='#DAA71A')

    local_patch = mpatches.Patch(color='#058872', label='Local breweries')
    industrial_patch = mpatches.Patch(color='#DAA71A', label='Industrial breweries')
    plt.legend(handles=[local_patch, industrial_patch], bbox_to_anchor=(1.05, 0.98), fontsize='6', ncol=1)
    plt.ylabel('Countries', weight='bold')
    plt.xlabel('Proportion of industrial vs local breweries', weight='bold')
    #plt.legend(labels=["Local breweries","Industrial breweries"], loc='upper left', labelcolor=['#058872', '#DAA71A'], fontsize='small')
    plt.xlim(-1.2,1.2)
    st.pyplot(fig)

with best_breweries:
    option = st.selectbox('Select a country you are interested in visiting?',
        (np.sort(data['location'].unique())))

    df = ratings[ratings['country_brewery']==option].groupby('brewery_name').agg({'z_score':'mean'}).reset_index().sort_values(by='z_score', ascending=False)
    df = df.reset_index()
    df.index += 1
    
    st.write('These are the top rated breweries in that country:')
    st.table(df['brewery_name'].head(10))
    