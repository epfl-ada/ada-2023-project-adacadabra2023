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
    '''
    tar_files = [file for file in os.listdir(data_path) if file.endswith('.gz')]

    for tar_file in tar_files:
        tar_file_path = os.path.join(data_path, tar_file)

        extraction_folder_name = os.path.basename(tar_file_path).split('.', 1)[0]
        folder_path = os.path.join(data_path, extraction_folder_name)
        os.makedirs(folder_path, exist_ok=True)

        with tarfile.open(tar_file_path, 'r') as tar:
            tar.extractall(path=folder_path)


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

def unify_location(loc, keep_state=False):
    if not keep_state:
        return 'United States' if loc.startswith('United States') else loc
    else: 
        if loc.startswith('United States'):
            return loc.split(',')[1]
        else: 
            return loc
        
def txt_to_tsv(path, filename):
    '''
        This function takes as input the path where the .txt file is located as well as the filename and will create a .tsv file 
        in the same folder from the data in the .txt file. 
        
        The .txt file is read line by line and a dictionary is created to which the different values for each key are appended as 
        the file is read. The "nan" are replaced by empty space ('') to be better recognized when creating a dataframe.
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



def filter_countries(df, min_styles=3):
    ''' Filters countries that do not have at least min_styles styles per season.
    Args:
        df: Unified_ratings dataframe coming from main_preprocessing
        min_styles (int) min umber of styles
    '''
    filtered_df = df[['style','Trimester', 'country_brewery']]

    sty_country = filtered_df.groupby(['country_brewery', 'Trimester'], as_index=False).nunique()

    select_countries = sty_country.groupby('country_brewery', as_index=False).min()
    keep_countries = select_countries[select_countries['style'] >= min_styles]
    valid_countries = keep_countries.country_brewery.values
    filtered_countries = df[filtered_df['country_brewery'].isin(valid_countries)]
    return filtered_countries


def remove_countries(df):
    ''' Removes countries with wrongly parsed names
    '''
    countries = df.country_brewery.unique()
    invalid_countries = countries.apply(lambda x: x.contains('</a>'))
    df = df[~df.country_brewery.isin(invalid_countries)]
    return df