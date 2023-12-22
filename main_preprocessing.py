import argparse
import os, shutil
import pandas as pd
import numpy as np
import pickle as pkl


import src.data.Preprocessing as pproc 
import src.data.HerdingFunctions as hf


def filter_by_value(df1, df2, min_value, colname, idcolname):
    ''' 
        Filter a dataframe with a threhold and based on filtering results, use an column of that
        dataframe to filter a second dataframe
        Args:
            df1 (pd.DataFrame): dataframe 1.
            df2 (pd.DataFrame): dataframe 2.
            min_value (int): threshold for filtering
            colname: name of the column in df1 that will be filtered by the threshold
            idcolname1: name of the column that will do the comparison between dfs for filtering df2
        Returns:
            pd.DataFrames: filtered dataframes 1 and 2
    '''
    filtered_df = df1[df1[colname]>=min_value]
    filtered_df2 = df2[df2.set_index([idcolname]).index.isin(filtered_df.set_index([idcolname]).index)]
    return filtered_df, filtered_df2

def main(args):
    ''' 
    Pre-process the raw data, transform .txt files to .parquet and unified
    the pre-process files into pickle files
    '''
    # Define the path for the files
    RB_path = os.path.join(args.dpath, 'RateBeer')
    BA_path = os.path.join(args.dpath, 'BeerAdvocate')
    MB_path = os.path.join(args.dpath, 'matched_beer_data')


    if not args.no_extract:
        # Extract the .tar files
        print('Extracting files...')
        pproc.extract_tar_files(args.dpath)
            
        #Transform .txt files to tsv
        print('Transforming ratings.txt to tsv...')
        pproc.txt_to_tsv(RB_path, 'ratings')
        pproc.txt_to_tsv(BA_path, 'ratings')
    
    # Loading data
    print('Loading datasets and filtering ...')
    MB_beers = pd.read_csv(MB_path + '/beers.csv', header=1)
    MB_breweries = pd.read_csv(MB_path + '/breweries.csv', header=1)
    MB_users = pd.read_csv(MB_path + '/users.csv', header=1)
    
    RB_beers = pd.read_csv(RB_path + '/beers.csv')
    RB_breweries = pd.read_csv(RB_path + '/breweries.csv')
    RB_users = pd.read_csv(RB_path + '/users.csv')
    RB_ratings = pd.read_csv(RB_path + '/ratings.tsv', sep='\t')

    BA_beers = pd.read_csv(BA_path + '/beers.csv')
    BA_breweries = pd.read_csv(BA_path + '/breweries.csv')
    BA_users = pd.read_csv(BA_path + '/users.csv')
    BA_ratings = pd.read_csv(BA_path + '/ratings.tsv', sep='\t')
    BA_ratings.user_id = BA_ratings.user_id.apply(lambda x: x.replace(' ', ''))
    
    # Load the dictionary for the macro_styles
    beer_dict = {
    'American Pale Ale': 'Pale Ale',
    'American Blonde Ale': 'Pale Ale',
    'Golden Ale/Blond Ale': 'Pale Ale',
    'Bitter': 'Pale Ale',
    'Pale Ale': 'Pale Ale',
    'American Pale Ale (APA)': 'Pale Ale',
    'English Pale Ale': 'Pale Ale',
    'English Bitter': 'Pale Ale',
    'Premium Bitter/ESB': 'Pale Ale',
    'English India Pale Ale (IPA)': 'Pale Ale',
    'Extra Special / Strong Bitter (ESB)': 'Pale Ale',
    'Saison / Farmhouse Ale': 'Pale Ale',
    'English Pale Mild Ale': 'Pale Ale',
    'Saison': 'Pale Ale',
    'Belgian Pale Ale': 'Pale Ale',
    'Belgian Strong Pale Ale': 'Strong Pale Ale',
    'Tripel': 'Strong Pale Ale',
    'Abbey Tripel': 'Strong Pale Ale',
    'American IPA': 'IPA',
    'Black IPA': 'IPA',
    'India Pale Ale (IPA)': 'IPA',
    'American Double / Imperial IPA': 'IPA',
    'Imperial IPA': 'IPA',
    'New England IPA (NEIPA)': 'IPA',
    'Session IPA': 'IPA',
    'Belgian IPA': 'IPA',
    'Abbey Dubbel': 'Brown/Dark Ale',
    'Dubbel': 'Brown/Dark Ale',
    'Belgian Dark Ale': 'Brown/Dark Ale',
    'American Brown Ale': 'Brown/Dark Ale',
    'Brown Ale': 'Brown/Dark Ale',
    'English Dark Mild Ale': 'Brown/Dark Ale',
    'American Black Ale': 'Brown/Dark Ale',
    'English Brown Ale': 'Brown/Dark Ale',
    'Belgian Strong Dark Ale': 'Strong Brown/Dark Ale',
    'Abt/Quadrupel': 'Strong Brown/Dark Ale',
    'Barley Wine': 'Strong Brown/Dark Ale',
    'English Barleywine': 'Strong Brown/Dark Ale',
    'American Barleywine': 'Strong Brown/Dark Ale',
    'Quadrupel (Quad)': 'Strong Brown/Dark Ale',
    'Amber Ale': 'Amber Ale',
    'American Amber Ale': 'Amber Ale',
    'Irish Red Ale': 'Amber Ale',
    'American Amber / Red Ale': 'Amber Ale',
    'Red Ale': 'Amber Ale',
    'Belgian Ale': 'Ale',
    'Irish Ale': 'Ale',
    'Old Ale': 'Ale',
    'Mild Ale': 'Ale',
    'Traditional Ale': 'Ale',
    'Scotch Ale / Wee Heavy': 'Ale',
    'Scotch Ale': 'Ale',
    'Scottish Ale': 'Ale',
    'Belgian Strong Ale': 'Strong Ale',
    'American Strong Ale': 'Strong Ale',
    'English Strong Ale': 'Strong Ale',
    'Winter Warmer': 'Strong Ale',
    'Stout': 'Stout',
    'American Stout': 'Stout',
    'Dry Stout': 'Stout',
    'American Double / Imperial Stout': 'Stout',
    'English Stout': 'Stout',
    'Imperial Stout': 'Stout',
    'Irish Dry Stout': 'Stout',
    'Foreign / Export Stout': 'Stout',
    'Oatmeal Stout': 'Stout',
    'Russian Imperial Stout': 'Stout',
    'Milk / Sweet Stout': 'Stout',
    'Foreign Stout': 'Stout',
    'Sweet Stout': 'Stout',
    'Porter': 'Porter',
    'American Porter': 'Porter',
    'Baltic Porter': 'Porter',
    'Imperial Porter': 'Porter',
    'English Porter': 'Porter',
    'American Dark Wheat Ale': 'Wheat Beer',
    'Berliner Weissbier': 'Wheat Beer',
    'Dunkelweizen': 'Wheat Beer',
    'German Hefeweizen': 'Wheat Beer',
    'Hefeweizen': 'Wheat Beer',
    'Wheat Ale': 'Wheat Beer',
    'Weizen Bock': 'Wheat Beer',
    'Roggenbier': 'Wheat Beer',
    'Weizenbock': 'Wheat Beer',
    'Witbier': 'Wheat Beer',
    'German Kristallweizen': 'Wheat Beer',
    'Berliner Weisse': 'Wheat Beer',
    'Kristalweizen': 'Wheat Beer',
    'Wheatwine': 'Wheat Beer',
    'Dunkelweizen': 'Wheat Beer',
    'American Pale Wheat Ale': 'Wheat Beer',
    'Flanders Oud Bruin': 'Wild/Sour Beer',
    'Flanders Red Ale': 'Wild/Sour Beer',
    'Gose': 'Wild/Sour Beer',
    'Lambic - Fruit': 'Wild/Sour Beer',
    'American Wild Ale': 'Wild/Sour Beer',
    'Lambic - Unblended': 'Wild/Sour Beer',
    'Lambic Style - Faro': 'Wild/Sour Beer',
    'Lambic Style - Fruit': 'Wild/Sour Beer',
    'Lambic Style - Gueuze': 'Wild/Sour Beer',
    'Lambic Style - Unblended': 'Wild/Sour Beer',
    'Sour Red/Brown': 'Wild/Sour Beer',
    'Sour/Wild Ale': 'Wild/Sour Beer',
    'Faro': 'Wild/Sour Beer',
    'Gueuze': 'Wild/Sour Beer',
    'Grodziskie/Gose/Lichtenhainer': 'Wild/Sour Beer',
    'American Adjunct Lager': 'Pilsner & Pale Lager',
    'American Pale Lager': 'Pilsner & Pale Lager',
    'Pilsener': 'Pilsner & Pale Lager',
    'Dortmunder / Export Lager': 'Pilsner & Pale Lager',
    'European Pale Lager': 'Pilsner & Pale Lager',
    'German Pilsener': 'Pilsner & Pale Lager',
    'Pale Lager': 'Pilsner & Pale Lager',
    'Munich Helles Lager': 'Pilsner & Pale Lager',
    'Pilsener (German and Czech)': 'Pilsner & Pale Lager',
    'Czech Pilsener': 'Pilsner & Pale Lager',
    'Czech Pilsner (Světlý)': 'Pilsner & Pale Lager',
    'India Style Lager': 'Pilsner & Pale Lager',
    'Imperial Pils/Strong Pale Lager': 'Pilsner & Pale Lager',
    'Kellerbier / Zwickelbier': 'Pilsner & Pale Lager',
    'Euro Pale Lager': 'Pilsner & Pale Lager',
    'Zwickel/Keller/Landbier': 'Pilsner & Pale Lager',
    'Euro Strong Lager': 'Pilsner & Pale Lager',
    'American Double / Imperial Pilsner': 'Pilsner & Pale Lager',
    'Light Lager': 'Pilsner & Pale Lager',
    'Radler/Shandy': 'Pilsner & Pale Lager',
    'Japanese Rice Lager': 'Pilsner & Pale Lager',
    'Premium Lager': 'Pilsner & Pale Lager',
    'Dortmunder/Helles': 'Pilsner & Pale Lager',
    'Doppelbock': 'Bock',
    'Eisbock': 'Bock',
    'Heller Bock': 'Bock',
    'Maibock / Helles Bock': 'Bock',
    'Bock': 'Bock',
    'Amber Lager/Vienna': 'Dark Lager',
    'Munich Dunkel Lager': 'Dark Lager',
    'Schwarzbier': 'Dark Lager',
    'Vienna Lager': 'Dark Lager',
    'American Amber / Red Lager': 'Dark Lager',
    'Dunkel/Tmavý': 'Dark Lager',
    'Dunkler Bock': 'Dark Lager',
    'Euro Dark Lager': 'Dark Lager',
    'Schwarzbier': 'Dark Lager',
    'Polotmavý': 'Dark Lager',
    'Märzen / Oktoberfest': 'Dark Lager',
    'Oktoberfest/Märzen': 'Dark Lager',
    'Rauchbier': 'Smoked',
    'Smoked': 'Smoked',
    'Smoked Beer': 'Smoked',
    'Cream Ale': 'Hybrid Beer',
    'Kölsch': 'Hybrid Beer',
    'California Common': 'Hybrid Beer',
    'California Common / Steam Beer': 'Hybrid Beer',
    'Braggot': 'Hybrid Beer',
    'Bière de Garde': 'Hybrid Beer',
    'Black & Tan': 'Hybrid Beer',
    'Altbier': 'Hybrid Beer',
    'Rye Beer': 'Hybrid Beer',
    'Chile Beer': 'Herbs/Vegetables',
    'Cider': 'Herbs/Vegetables',
    'Fruit / Vegetable Beer': 'Herbs/Vegetables',
    'Fruit Beer': 'Herbs/Vegetables',
    'Herbed / Spiced Beer': 'Herbs/Vegetables',
    'Mead': 'Herbs/Vegetables',
    'Spice/Herb/Vegetable': 'Herbs/Vegetables',
    'Specialty Grain': 'Herbs/Vegetables',
    'Sahti': 'Herbs/Vegetables',
    'Sahti/Gotlandsdricke/Koduõlu': 'Herbs/Vegetables',
    'Scottish Gruit / Ancient Herbed Ale': 'Herbs/Vegetables',
    'Pumpkin Ale': 'Herbs/Vegetables',
    'Perry': 'Herbs/Vegetables',
    'Happoshu': 'Low Alcohol',
    'Low Alcohol': 'Low Alcohol',
    'Low Alcohol Beer': 'Low Alcohol',
    'Kvass': 'Low Alcohol',
    'American Malt Liquor': 'Cocktails',
    'Bière de Champagne / Bière Brut': 'Cocktails',
    'Malt Liquor': 'Cocktails',
    'Saké - Daiginjo': 'Cocktails',
    'Saké - Futsu-shu': 'Cocktails',
    'Saké - Genshu': 'Cocktails',
    'Saké - Ginjo': 'Cocktails',
    'Saké - Honjozo': 'Cocktails',
    'Saké - Infused': 'Cocktails',
    'Saké - Junmai': 'Cocktails',
    'Saké - Koshu': 'Cocktails',
    'Saké - Namasaké': 'Cocktails',
    'Saké - Nigori': 'Cocktails',
    'Saké - Taru': 'Cocktails',
    'Saké - Tokubetsu': 'Cocktails'
    }
   
    print('Done loading!')

    # # Remove extracted folders
    # print('Removing extracted folders...')
    # shutil.rmtree(RB_path)
    # shutil.rmtree(BA_path)
    # shutil.rmtree(MB_path)
   
    # Merge breweries
    # Creation of the df with ALL the breweries with a unique brewery ID (chosen to be the one from RB)
    print('Merging breweries...')
    unified_breweries = RB_breweries
    unified_breweries = unified_breweries.rename(columns={'nbr_beers':'nbr_beers_rb'})

    BA_brew = BA_breweries.add_suffix('_ba')

    MB_breweries_subset = MB_breweries[['id', 'id.1', 'location', 'location.1', 'nbr_beers', 'nbr_beers.1', 'name', 'name.1']]
    MB_breweries_subset = MB_breweries_subset.add_suffix('_ba')
    MB_breweries_subset.columns = MB_breweries_subset.columns.str.replace('.1_ba' , '_rb')

    merged_df = pd.merge(BA_brew, MB_breweries_subset, on=['id_ba', 'name_ba', 'location_ba', 'nbr_beers_ba'], how='left')
    available_numbers_brew = np.setxor1d(np.arange(1,3*len(BA_brew)), unified_breweries.id.unique())
    merged_df['new_ba_brew_id'] = available_numbers_brew[:len(BA_brew)]

    merged_df['id'] = merged_df['id_rb'].combine_first(merged_df['new_ba_brew_id'])
    merged_df['location'] = merged_df['location_rb'].combine_first(merged_df['location_ba'])
    merged_df['name'] = merged_df['name_rb'].combine_first(merged_df['name_ba'])

    unified_breweries = unified_breweries.merge(merged_df[['name', 'id', 'location', 'nbr_beers_ba']], on=['id', 'name', 'location'], how='outer')
    unified_breweries['nbr_beers_rb'].fillna(0, inplace=True)
    unified_breweries['nbr_beers_ba'].fillna(0, inplace=True)
    unified_breweries['total_nbr_beers'] = unified_breweries[["nbr_beers_rb", "nbr_beers_ba"]].max(axis=1)

    # Duplicated in the BA database
    unified_breweries['nbr_ba'] = unified_breweries.groupby('id')['nbr_beers_ba'].transform('mean')
    unified_breweries = unified_breweries.drop_duplicates('id')
    unified_breweries = unified_breweries.drop('nbr_beers_ba', axis=1)
    unified_breweries = unified_breweries.rename(columns={'nbr_ba':'nbr_beers_ba', 'id':'brewery_id', 'location':'country_brewery'})


    # Merge beers
    # Creation of the df with ALL the beers (that have at least one rating) with a unique beer ID (randomly chosen to be the one from RB)
    print('Merging beers...')
    unified_beers = RB_beers[['beer_id', 'beer_name', 'nbr_ratings', 'style', 'brewery_id', 'brewery_name']]
    unified_beers = unified_beers.rename(columns={'nbr_ratings':'nbr_ratings_rb'})

    BA_beers_subset = BA_beers[['beer_id', 'beer_name', 'nbr_ratings', 'style', 'brewery_id', 'brewery_name']]
    BA_beers_subset.columns += '_ba'

    MB_beers_subset = MB_beers[['beer_id', 'beer_id.1', 'beer_name', 'beer_name.1', 'style', 'style.1', 'brewery_id', 'brewery_id.1', 'brewery_name', 'brewery_name.1']]
    MB_beers_subset.columns += '_ba'
    MB_beers_subset.columns = MB_beers_subset.columns.str.replace('.1_ba' , '_rb')

    merged_df_beers = pd.merge(BA_beers_subset, MB_beers_subset, on=['beer_id_ba', 'beer_name_ba', 'style_ba', 'brewery_id_ba', 'brewery_name_ba'], how='left')
    available_numbers = np.setxor1d(np.arange(1,3*len(BA_beers_subset)), unified_beers.beer_id.unique())
    merged_df_beers['new_ba_id'] = available_numbers[:len(BA_beers_subset)]
    merged_df_beers['brewery_name'] = merged_df_beers['brewery_name_rb'].combine_first(merged_df_beers['brewery_name_ba'])
    equivalences_dict_brew_id = dict(zip(unified_breweries['name'], unified_breweries['brewery_id']))
    merged_df_beers['brewery_id'] = merged_df_beers['brewery_name'].map(equivalences_dict_brew_id)
    merged_df_beers['style'] = merged_df_beers['style_rb'].combine_first(merged_df_beers['style_ba'])
    merged_df_beers['beer_id'] = merged_df_beers['beer_id_rb'].combine_first(merged_df_beers['new_ba_id'])
    merged_df_beers['beer_name'] = merged_df_beers['beer_name_rb'].combine_first(merged_df_beers['beer_name_ba'])

    unified_beers = unified_beers.merge(merged_df_beers[['nbr_ratings_ba', 'style', 'brewery_id', 'brewery_name', 'beer_id', 'beer_name']], on=['beer_id', 'beer_name', 'brewery_id', 'brewery_name','style'], how='outer')
    unified_beers['nbr_ratings_rb'].fillna(0, inplace=True)
    unified_beers['nbr_ratings_ba'].fillna(0, inplace=True)
    unified_beers['total_nbr_ratings'] = unified_beers['nbr_ratings_rb'] + unified_beers['nbr_ratings_ba']
    unified_beers['macro_style'] = unified_beers['style'].map(beer_dict)
    
    # Merge users
    # Creation of the df with ALL the users with a unique user ID (randomly chosen to be the one from RB)
    print('Merging users...')
    unified_users = RB_users[['nbr_ratings', 'user_id', 'user_name', 'location']]
    unified_users = unified_users.rename(columns={'nbr_ratings':'nbr_ratings_rb'})

    BA_users_subset = BA_users[['nbr_ratings', 'user_id', 'user_name', 'location']]
    BA_users_subset = BA_users_subset.add_suffix('_ba')

    MB_users_subset = MB_users[['location', 'location.1', 'nbr_ratings', 'nbr_ratings.1', 'user_id', 'user_id.1', 'user_name', 'user_name.1']]
    MB_users_subset = MB_users_subset.add_suffix('_ba')
    MB_users_subset.columns = MB_users_subset.columns.str.replace('.1_ba' , '_rb')

    merged_df_users = pd.merge(BA_users_subset, MB_users_subset, on=['user_id_ba', 'user_name_ba', 'location_ba', 'nbr_ratings_ba'], how='left')
    available_numbers = np.setxor1d(np.arange(1,3*len(BA_users_subset)), unified_users.user_id.unique())
    merged_df_users['new_ba_id'] = available_numbers[:len(BA_users_subset)]

    merged_df_users['user_name'] = merged_df_users['user_name_rb'].combine_first(merged_df_users['user_name_ba'])
    merged_df_users['location'] = merged_df_users['location_rb'].combine_first(merged_df_users['location_ba'])
    merged_df_users['user_id'] = merged_df_users['user_id_rb'].combine_first(merged_df_users['new_ba_id'])

    unified_users = unified_users.merge(merged_df_users[['nbr_ratings_ba', 'user_name', 'location', 'user_id']], on=['user_id', 'user_name', 'location'], how='outer')
    unified_users['nbr_ratings_rb'].fillna(0, inplace=True)
    unified_users['nbr_ratings_ba'].fillna(0, inplace=True)
    unified_users['total_nbr_ratings'] = unified_users['nbr_ratings_rb'] + unified_users['nbr_ratings_ba']
    unified_users = unified_users.rename(columns={'location':'country_user'})
    unified_users = unified_users[~unified_users['country_user'].isna()] #Remove users without a location
   
    # Merge ratings
    # Creation of the df with ALL the ratings with a unique user ID (randomly chosen to be the one from RB)
    print('Merging ratings...')
    unified_ratings = RB_ratings[['beer_name', 'beer_id', 'brewery_name', 'brewery_id', 'style', 'date', 'rating', 'user_id', 'text', 'abv']]
    unified_ratings.loc[:, 'Procedence']  = 'RB'

    BA_subset = BA_ratings[['beer_name', 'beer_id', 'brewery_name', 'brewery_id', 'style', 'date', 'rating', 'user_id', 'text', 'abv']]
    BA_subset = BA_subset.add_suffix('_ba')

    equivalences_brew_id = dict(zip(merged_df['id_ba'], merged_df['id']))
    BA_subset['brewery_id'] = BA_subset['brewery_id_ba'].map(equivalences_brew_id)

    BA_subset['brewery_name_ba'] = BA_subset['brewery_name_ba'].str.strip()
    equivalences_brew_name = dict(zip(merged_df['name_ba'].str.strip(), merged_df['name']))
    BA_subset['brewery_name'] = BA_subset['brewery_name_ba'].map(equivalences_brew_name)

    equivalences_beer_id = dict(zip(merged_df_beers['beer_id_ba'], merged_df_beers['beer_id']))
    BA_subset['beer_id'] = BA_subset['beer_id_ba'].map(equivalences_beer_id)

    equivalences_user_id = dict(zip(merged_df_users['user_id_ba'].str.strip(), merged_df_users['user_id']))
    BA_subset['user_id_ba'] = BA_subset['user_id_ba'].str.strip()
    BA_subset['user_id'] = BA_subset['user_id_ba'].map(equivalences_user_id)

    BA_subset['beer_name_ba'] = BA_subset['beer_name_ba'].str.strip()
    equivalences_beer_name = dict(zip(merged_df_beers['beer_name_ba'].str.strip(), merged_df_beers['beer_name']))
    BA_subset['beer_name'] = BA_subset['beer_name_ba'].map(equivalences_beer_name)

    BA_subset['style_ba'] = BA_subset['style_ba'].str.strip()
    equivalences_style = dict(zip(merged_df_beers['style_ba'].str.strip(), merged_df_beers['style']))
    BA_subset['style'] = BA_subset['style_ba'].map(equivalences_style)

    BA_subset = BA_subset.drop(['beer_name_ba', 'beer_id_ba', 'brewery_id_ba', 'brewery_name_ba', 'style_ba', 'user_id_ba'], axis=1)
    BA_subset.columns = BA_subset.columns.str.replace('_ba' , '')
    BA_subset.loc[:, 'Procedence']  = 'BA'

    unified_ratings = pd.concat([unified_ratings, BA_subset], ignore_index=True)

    equivalences_country = dict(zip(unified_users['user_id'], unified_users['country_user']))
    unified_ratings['country_user'] = unified_ratings['user_id'].map(equivalences_country)

    equivalences_brew_country = dict(zip(unified_breweries['brewery_id'], unified_breweries['country_brewery']))
    unified_ratings['country_brewery'] = unified_ratings['brewery_id'].map(equivalences_brew_country)
    unified_ratings['style'] = unified_ratings['style'].str.strip()
    unified_ratings['macro_style'] = unified_ratings['style'].str.strip().map(beer_dict)
    unified_ratings = unified_ratings[~unified_ratings['country_user'].isna()] #Remove ratings of users without a location
    
    #Unify locations
    unified_ratings['country_brewery'] = unified_ratings['country_brewery'].apply(pproc.unify_location)
    unified_ratings['country_user'] = unified_ratings['country_user'].apply(pproc.unify_location)
    unified_breweries['country_brewery'] = unified_breweries['country_brewery'].apply(pproc.unify_location)
    unified_users['country_user'] = unified_users['country_user'].apply(pproc.unify_location)
    
    # Correct herding effect
    # Adding a time column in an interpretable format and a 'year' column.
    print('Correcting for herding...')
    unified_ratings = hf.correct_time(unified_ratings, season=True).copy(deep=True)
    unified_ratings['z_score'] = unified_ratings.groupby(['Procedence', 'year'])['rating'].transform(lambda x:(x-x.mean())/x.std())
    unified_ratings_BA = unified_ratings[unified_ratings.Procedence == 'BA']
    unified_ratings_RB = unified_ratings[unified_ratings.Procedence == 'RB']
    unified_ratings_BA = hf.he_correction(unified_ratings_BA)
    unified_ratings_RB = hf.he_correction(unified_ratings_RB)

    print('Concatenating data...')
    unified_ratings = pd.concat([unified_ratings_BA, unified_ratings_RB], ignore_index=True)

    # Save unified beers as pickle file
    print('Saving merging beers as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_beers_raw.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(unified_beers, f)
    print('Raw unified beers shape: ', unified_beers.shape)
    
    # Save unified users as pickle file
    print('Saving merging users as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_users_raw.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(unified_users, f)
    print('Raw unified users shape: ', unified_users.shape)
    
    # Save unified breweries as pickle file
    print('Saving merging breweries as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_breweries_raw.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(unified_breweries, f)
    print('Raw unified breweries shape: ', unified_breweries.shape)
    
    # Save unified & herding corrected ratings as pickle file
    print('Saving corrected ratings as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_ratings_raw.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(unified_ratings, f)
    print('Raw herding-corrected unified ratings shape: ', unified_ratings.shape)
    
    ##Filtering
    print('Filtering data...')
    # To have users with a minimum number of ratings
    df_users_filt, df_ratings_filt_users = pproc.filter_by_value(unified_users, unified_ratings, args.min_user_rating, 'total_nbr_ratings', 'user_id')
    
    # Remove breweries with 0 beers
    df_breweries_filt, df_ratings_filt_breweries = pproc.filter_by_value(unified_breweries, df_ratings_filt_users, args.min_brewery_produced, 'total_nbr_beers', 'brewery_id')

    
    # Filter to have only locations with at least 30 breweries
    brewery_per_location_counts = df_breweries_filt.groupby('country_brewery').size().reset_index().rename(columns={0:'brewery_per_location'})
    _ , df_ratings_filt_countries = pproc.filter_by_ratings(brewery_per_location_counts, df_ratings_filt_breweries, 30, 'brewery_per_location', 'country_brewery')
        
    # Filters countries that do not have at least min_styles styles per trimester.
    df_ratings_filt_final, df_breweries_filt_final = pproc.filter_countries(df_ratings_filt_countries, df_breweries_filt, args.min_styles_season)
    
    # Save unified beers as pickle file
    print('Saving filtered beers as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_beers.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(unified_beers, f)
    print('Final filtered unified beers shape: ', unified_beers.shape)
    
    # Save unified users as pickle file
    print('Saving filtered users as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_users.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(df_users_filt, f)
    print('Final filtered unified users shape: ', df_users_filt.shape)
    
    # Save unified breweries as pickle file
    print('Saving filtered breweries as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_breweries.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(df_breweries_filt_final, f)
    print('Final filtered unified breweries shape: ', df_breweries_filt_final.shape)
    
    # Save unified & herding corrected ratings as pickle file
    print('Saving filtered ratings as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_ratings.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(df_ratings_filt_final, f)
    print('Final filtered ratings shape: ', df_ratings_filt_final.shape)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dpath', type=str, default= 'Data')
    parser.add_argument('--no-extract', action='store_true')
    parser.add_argument('-rt', '--min-user-rating', type=int, default=20)
    parser.add_argument('-rw', '--min-beer-review', type=int, default=15)
    parser.add_argument('-bp', '--min-brewery-produced', type=int, default=1)
    parser.add_argument('-fc', '--min-styles-season', type=int, default=3)

    args = parser.parse_args()
    main(args)