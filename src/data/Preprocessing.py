#DATA UPLOAD AND PATH FINDER: 
import tarfile
import pandas as pd
import numpy as np
import re
import os
import gzip



def extract_tar_files(data_path):
    '''
        List the .tar files in the data path and extract them in the corresponding subfolder
        Args:
            data_path: path where the tar files are located
        Returns:
            Creates subfolders and extracts the tar files in the specific subfolders
    '''
    tar_files = [file for file in os.listdir(data_path) if file.endswith('.gz')]

    for tar_file in tar_files:
        tar_file_path = os.path.join(data_path, tar_file)

        extraction_folder_name = os.path.basename(tar_file_path).split('.', 1)[0]
        folder_path = os.path.join(data_path, extraction_folder_name)
        os.makedirs(folder_path, exist_ok=True)

        with tarfile.open(tar_file_path, 'r') as tar:
            tar.extractall(path=folder_path)

def txt_to_tsv(path, filename):
    '''
        Transform a .txt file enconted as utf8 into a .tsv file in dataframe format. The file is read line by line,
        and a dictionary is created for the different keys and values every time there is a end-of-line and saved 
        into the .tsv file. The "nan" are replaced by empty space ('') to be better recognized when creating the dataframe.
        Args:
            path: path where the file to be transformed is located
            filename: name of the file
        Returns:
            Creates a .tsv located in the same path provided in args.
    '''
    main_path = os.path.join(path, filename)
    if not os.path.exists(main_path + '.tsv'):
        with gzip.open(main_path + '.txt.gz', 'rt', encoding="utf8") as file_txt:
            with open(main_path + '.tsv', 'w', encoding="utf8") as file_tsv:
                first = True
                obj = {}
                for line in file_txt:
                    if line == '\n':
                        if first:
                            file_tsv.write("\t".join(obj.keys()) + "\n")
                            first=False
                        file_tsv.write("\t".join(obj.values()) + "\n")
                        obj = {}
                        continue

                    line = re.sub(r'\bnan\b', '', line)
                    key, value = line.strip().split(":", 1)
                    obj[key] = value
                
                if obj: file_tsv.write("\t".join(obj.values()) + "\n")

def filter_by_ratings(df, df_ratings, min_ratings, colname, idcolname1, idcolname2=None):
    ''' 
    Filters users based on number of ratings.
    Args:
        df (pd.DataFrame): dataframe with users.
        df_ratings: TODo
        min_ratings (int): minimum number of ratings a user should have to not be removed
        colname: name of the column that will set the threshold for filtring out
        idcolname1: name of the column (in df) that will do the comparison between dfs looking for an isin function
        idcolname2: name of the column (in df_ratings) that will do the comparison between dfs looking for an isin function
    Returns:
        pd.DataFrame: dataframe with users filtered
    '''
    if idcolname2 is None:
        idcolname2 = idcolname1
    # filter the df accoring to the threshold
    filtered_df = df[df[colname]>min_ratings]
    # take the common column to both dfs and apply an isin
    filtered_df2 = df_ratings[df_ratings[idcolname2].isin(filtered_df[idcolname1].values)]
    return filtered_df, filtered_df2

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

def unify_location(loc):
    '''
        Unify country names for countries that are split in multiple states/regions
        Args:
            loc: country name in location column in any of the dataframes
        Returns:
            loc: original country name or corrected country names based on conditions
    '''
    if (loc.startswith('United States') or loc.startswith('Utah') or loc.startswith('New York') or loc.startswith('Virgin Islands') or loc.startswith('Illinois')):
        return 'United States'
    elif loc.startswith('Canada'):
        return 'Canada'
    elif loc.startswith('United Kingdom') or loc.startswith('Wales') or loc.startswith('England') or loc.startswith('Scotland') or loc.startswith('Northern Ireland'):
        return 'United Kingdom'
    else: 
        return loc


def filter_countries(df, df_brew, min_styles=3):
    ''' Filters countries that do not have at least min_styles styles per trimester.
    Args:
        df: Unified_ratings dataframe coming from main_preprocessing
        df: Unified_breweries dataframe coming from main_preprocessing
        min_styles (int) min umber of styles
    '''
    filtered_df = df[['macro_style','Trimester', 'country_brewery']]

    sty_country = filtered_df.groupby(['country_brewery', 'Trimester'], as_index=False).nunique()

    select_countries = sty_country.groupby('country_brewery', as_index=False).min()
    keep_countries = select_countries[select_countries['macro_style'] >= min_styles]
    valid_countries = keep_countries.country_brewery.values
    filtered_countries = df[filtered_df['country_brewery'].isin(valid_countries)]
    filtered_breweries = df_brew[df_brew['country_brewery'].isin(valid_countries)]
    return filtered_countries, filtered_breweries


def remove_countries(df):
    ''' Removes countries with wrongly parsed names
    '''
    countries = df.country_brewery.unique()
    invalid_countries = countries.apply(lambda x: x.contains('</a>'))
    df = df[~df.country_brewery.isin(invalid_countries)]
    return df