import os
import sys
import pickle as pkl

repo_path = '/root/ADA2023/ada-2023-project-adacadabra2023/ada-2023-project-adacadabra2023' # CHANGE
sys.path.append(repo_path)

# from src.data.Data import load_data

dpath = os.path.join(repo_path, 'Data', 'Unified_ratings.pkl')
with open(dpath, 'rb') as f:
    df = pkl.load(f)
print(df.shape)

df.columns

filtered_df = df[['style','Season', 'country_brewery']]
filtered_df

sty_country = filtered_df.groupby(['country_brewery', 'Season'], as_index=False).nunique()
sty_country

select_countries = sty_country.groupby('country_brewery', as_index=False).min()
keep_countries = select_countries[select_countries['style'] >= 3]
valid_countries = keep_countries.country_brewery.values


filtered_countries = filtered_df[filtered_df['country_brewery'].isin(valid_countries)]


top_4_beerstyles = filtered_countries.groupby(['country_brewery', 'Season'])['style'].value_counts().groupby(['country_brewery', 'Season']).head(3).reset_index(name='ratings')

top_4_beerstyles.groupby(['country_brewery', 'Season'], as_index= False).agg(lambda x: x.tolist())


