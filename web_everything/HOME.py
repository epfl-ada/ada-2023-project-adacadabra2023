import streamlit as st
#import pandas as pd

# Configure page
st.set_page_config(page_title='Beers Travel Guide', page_icon=':beer_mug:')

# Set Image
st.image('web_everything/figures/beer_intro.png')

# Set Title
st.title('Beers Travel Guide')

# st.sidebar.title("Beers Travel Guide")

st.write(
    """
    According to Wikipedia, __beer__ is one of the oldest alcoholic drinks in the world, the most 
    widely consumed, and the third most popular drink after water and tea. Almost every country in
    the world, crafts this fermented elixir with their unique blend of ingredients, techniques and 
    philosophies. Thus it comes with no surprise that beer acts as a portal, inviting us to traverse
    the diverse cultures, traditions and flavors spanning the globe. 
    
    Beer is a universal beverage that gathers people together everywhere around the world. Beer gives 
    you a reason to make a pause, be it in bars, parks, breweries, homes or vibrant gatherings, where
    people share stories, forge connections and discuss heterogeneous topics. In essence, beer breeds
    communities and communities nurture beer.

    In this blog, we set out a beer travel guide for intrepid explorers that provides unique 
    facets of beer culture around the world. We examine different beer-related features using 
    beer reviews sourced from beer communities called BeerAdvocate and RateBeer, and provide 
    traveling recommendations according to the user's needs.

    Join us is if you want to dive into the world of beers, and learn about each country's brewering
    traditions. Our guide might help you expand your traveling list, or find the perfect destinations
    aligned with your beer preferences. Isn't this what you beer-loving soul is thirsting for?
    """
)

c1, c2 = st.columns(2)
with c1:
    st.info('**EPFL - ADA: [@CS401](https://epfl-ada.github.io/teaching/fall2023/cs401/)**', icon="🎓")
with c2:
    st.info('**GitHub: [@adacadabra2023](https://github.com/epfl-ada/ada-2023-project-adacadabra2023)**', icon="💻")

st.markdown("Developed by __Sandra Hernández__, __Andrea López__, __Antonello Di Bari__, __Sebastián Deslarzes__ and __Cristina Loureiro__")
