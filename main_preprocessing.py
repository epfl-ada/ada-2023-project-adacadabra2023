import argparse
import os
import pandas as pd

import src.data.Preprocessing as pproc 


def filter_users(users_df, min_ratings):
    ''' Filters users based on number of ratings.
    Args:
        users_df (pd.DataFrame): dataframe with users.
        min_ratings (int): minimum number of ratings a user should have to not be removed
    Returns:
        pd.DataFrame: dataframe with users filtered
    '''
    pass


def main(args):
    ''' Creates pre-processed .csv files from the original files.
    '''
    # Definining the path for the files
    RB_path = os.path.join(args.dpath, 'RateBeer')
    BA_path = os.path.join(args.dpath, 'BeerAdvocate')
    MB_path = os.path.join(args.dpath, 'matched_beer_data')

    # Extraction of the .tar files
    pproc.extract_tar_files(args.dpath)
    
    #Transformation of the .txt files
    pproc.text_to_tsv(RB_path, 'ratings')
    pproc.text_to_tsv(RB_path, 'reviews')

    pproc.text_to_tsv(BA_path, 'ratings')
    pproc.text_to_tsv(BA_path, 'reviews')

    pproc.text_to_tsv(MB_path, 'ratings_ba')
    pproc.text_to_tsv(MB_path, 'ratings_with_text_ba')
    pproc.text_to_tsv(MB_path, 'ratings_rb')
    pproc.text_to_tsv(MB_path, 'ratings_with_text_rb')
    
    
    # Load all data
    MB_beers = pd.read_csv(MB_path + '/beers.csv', header=1)
    MB_breweries = pd.read_csv(MB_path + '/breweries.csv', header=1)
    MB_users = pd.read_csv(MB_path + '/users.csv', header=1)
    MB_users_approx = pd.read_csv(MB_path + '/users_approx.csv', header=1)
    
    MB_ratings = pd.read_csv(MB_path + '/ratings.csv', header=1)
    MB_ratingsBA = pd.read_csv(MB_path + '/ratings_ba.tsv', sep='\t')
    MB_ratingsBA_txt = pd.read_csv(MB_path + '/ratings_with_text_ba.tsv', sep='\t')
    MB_ratingsRB = pd.read_csv(MB_path + '/ratings_rb.tsv', sep='\t')
    MB_ratingsRB_txt = pd.read_csv(MB_path + '/ratings_with_text_rb.tsv', sep='\t')
    
    RB_beers = pd.read_csv(RB_path + '/beers.csv')
    RB_breweries = pd.read_csv(RB_path + '/breweries.csv')
    RB_users = pd.read_csv(RB_path + '/users.csv')
    RB_ratings = pd.read_csv(RB_path + '/ratings.tsv', sep='\t')
    RB_reviews = pd.read_csv(RB_path + '/reviews.tsv', sep='\t')
    
    BA_beers = pd.read_csv(BA_path + '/beers.csv')
    BA_breweries = pd.read_csv(BA_path + '/breweries.csv')
    BA_users = pd.read_csv(BA_path + '/users.csv')
    BA_ratings = pd.read_csv(BA_path + '/ratings.tsv', sep='\t')
    BA_reviews = pd.read_csv(BA_path + '/reviews.tsv', sep='\t')
    
    # TODO: Filter dataframes individually
    MB_users = filter_users(MB_users, args.min_user_rating)
    RB_users = filter_users(RB_users, args.min_user_rating)
    BA_users = filter_users(BA_users, args.min_user_rating)
    # filter_beers()
    # filter...
    
    # TODO: Copy Andrea's merge
    
    # TODO: Apply herding 
    
    
    


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dpath', type=str, default= 'Data')
    parser.add_argument('-r', '--min-user-rating', type=int, default=10) # TODO: Get correct number (change default)
    args = parser.parse_args()
    main(args)