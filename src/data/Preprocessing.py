#DATA UPLOAD AND PATH FINDER: 
import tarfile
import pandas as pd
import numpy as np
import re
import os
import gzip
import pyarrow as pa
import pyarrow.parquet as pq


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

def conversion(val, conv_type):
    '''
    Converts int64 and float64 to int and float
    '''
    if conv_type == pa.int64(): 
        val = int(val)
    elif conv_type == pa.float64():
        val = float(val)
    
    return(val)

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

""" def txt_to_parquet(path, filename):
    '''
        This function takes as input the path where the .txt file is located as well as the filename and will create a 
        compress parquet file in the same folder where the .txt file is saved. 
        
        The .txt file is read line by line and a dictionary is created to which the different values for each key are appended as 
        the file is read. The "nan" are replaced by empty space ('') to be better recognized when creating a dataframe.
    '''
     # Define fields and schema for the parquet file
    fields =[
        ('beer_name', pa.string()),
        ('beer_name', pa.string()),
        ('beer_id', pa.int64()),
        ('brewery_name', pa.string()),
        ('brewery_id', pa.int64()),
        ('style', pa.string()),
        ('abv', pa.float64()),
        ('date', pa.int64()),
        ('user_name', pa.string()),
        ('user_id', pa.int64()),
        ('appearance', pa.int64()),
        ('aroma', pa.int64()),
        ('palate', pa.int64()),
        ('taste', pa.int64()),
        ('overall', pa.int64()),
        ('rating', pa.float64()),
        ('text', pa.string())
     ]
    schema = pa.schema(fields)

    # Load the path and define the chunksizes for file generation
    main_path = os.path.join(path, filename)
    chunksize = 100
    chunk_counter = 0


    if not os.path.exists(main_path + '.parquet'):
        with gzip.open(main_path + '.txt.gz', 'rt', encoding="utf8") as file_txt:
            obj = {key: [] for key, _ in fields}
            with pq.ParquetWriter(main_path + '.parquet', schema=schema, compression='brotli') as file_parquet:
                for line in file_txt:
                    if line == '\n':
                        chunk_counter+=1
                        if chunk_counter >= chunksize:
                            table = pa.Table.from_pydict(obj, schema=schema)
                            file_parquet.write_table(table)
                            obj = {key: [] for key, _ in fields}
                            chunk_counter=0
                        continue  

                    line = re.sub(r'\bnan\b', '', line)
                    key, value = line.strip().split(":", 1)
                    if value == '':
                        obj[key].append(None)
                    elif isinstance(obj['user_id'], str) == True:
                        obj['user_id'] = obj['user_id'].split('.')[1]
                        conv_type = schema.types[schema.names.index(key)]
                        obj[key].append(conversion(value, conv_type))
                    else:
                        conv_type = schema.types[schema.names.index(key)]
                        obj[key].append(conversion(value, conv_type))

                if len(obj[list(obj.keys())[0]]):
                    table = pa.Table.from_pydict(obj, schema=schema)
                    file_parquet.write_table(table)

            file_parquet.close() """

