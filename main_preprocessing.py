import argparse
import os, shutil
import pandas as pd
import numpy as np
import pickle as pkl

import tarfile

import src.data.Preprocessing as pproc 
import src.data.HerdingFunctions as hf


def main(args):
    ''' 
    Pre-process the raw data, transform .txt files to .parquet and unified
    the pre-process files into pickle files
    '''
    # Define the path for the files
    RB_path = os.path.join(args.dpath, 'RateBeer')
    BA_path = os.path.join(args.dpath, 'BeerAdvocate')
    MB_path = os.path.join(args.dpath, 'matched_beer_data')

    # Extract the .tar files
    print('Extracting files...')
    pproc.extract_tar_files(args.dpath)
        
    #Transform .txt files to tsv
    print('Transforming ratings.txt to tsv...')
    pproc.txt_to_tsv(RB_path, 'ratings')
    pproc.txt_to_tsv(BA_path, 'ratings')
    
    # Loading data
    print('Loading datasets...')
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

    # Remove space in front of user for BA web
    BA_ratings.user_id = BA_ratings.user_id.apply(lambda x: x.replace(' ', ''))

    # Remove extracted folders
    print('Removing extracted folders...')
    shutil.rmtree(RB_path)
    shutil.rmtree(BA_path)
    shutil.rmtree(MB_path)
   
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
    unified_breweries = unified_breweries.rename(columns={'nbr_ba':'nbr_beers_ba'})

    # Save unified breweries as pickle file
    print('Saving merging breweries as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_breweries.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(unified_breweries, f)
    print('Final unified breweries shape: ', unified_breweries.shape)

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
    equivalences_dict_brew_id = dict(zip(unified_breweries['name'], unified_breweries['id']))
    merged_df_beers['brewery_id'] = merged_df_beers['brewery_name'].map(equivalences_dict_brew_id)
    merged_df_beers['style'] = merged_df_beers['style_rb'].combine_first(merged_df_beers['style_ba'])
    merged_df_beers['beer_id'] = merged_df_beers['beer_id_rb'].combine_first(merged_df_beers['new_ba_id'])
    merged_df_beers['beer_name'] = merged_df_beers['beer_name_rb'].combine_first(merged_df_beers['beer_name_ba'])

    unified_beers = unified_beers.merge(merged_df_beers[['nbr_ratings_ba', 'style', 'brewery_id', 'brewery_name', 'beer_id', 'beer_name']], on=['beer_id', 'beer_name', 'brewery_id', 'brewery_name','style'], how='outer')
    unified_beers['nbr_ratings_rb'].fillna(0, inplace=True)
    unified_beers['nbr_ratings_ba'].fillna(0, inplace=True)
    unified_beers['total_nbr_ratings'] = unified_beers['nbr_ratings_rb'] + unified_beers['nbr_ratings_ba']
    
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

    # Save unified users as pickle file
    print('Saving merging users as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_users.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(unified_users, f)
    print('Final unified users shape: ', unified_users.shape)
    
    # Merge ratings
    # Creation of the df with ALL the ratings with a unique user ID (randomly chosen to be the one from RB)
    print('Merging ratings...')
    unified_ratings = RB_ratings[['beer_name', 'beer_id', 'brewery_name', 'brewery_id', 'style', 'date', 'rating', 'user_id', 'text']]
    unified_ratings.loc[:, 'Procedence']  = 'RB'

    BA_subset = BA_ratings[['beer_name', 'beer_id', 'brewery_name', 'brewery_id', 'style', 'date', 'rating', 'user_id', 'text']]
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

    equivalences_country = dict(zip(unified_users['user_id'], unified_users['location']))
    unified_ratings['country_user'] = unified_ratings['user_id'].map(equivalences_country)

    equivalences_brew_country = dict(zip(unified_breweries['id'], unified_breweries['location']))
    unified_ratings['country_brewery'] = unified_ratings['brewery_id'].map(equivalences_brew_country)
    
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
    
    # Save unified & herding corrected ratings as pickle file
    print('Saving corrected ratings as pickle file...')
    save_path = os.path.join(args.dpath, 'unified_ratings.pkl')
    with open(save_path, 'wb') as f:
        pkl.dump(unified_ratings, f)
    print('Final herding-corrected unified ratings shape: ', unified_ratings.shape)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dpath', type=str, default= 'Data')
    args = parser.parse_args()
    main(args)