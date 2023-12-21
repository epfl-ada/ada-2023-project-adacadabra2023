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
    elif loc.startswith('United Kingdom'):
        return 'United Kingdom'
    else: 
        return loc
        