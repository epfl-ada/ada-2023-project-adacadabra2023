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
            
            
def text_to_tsv(path, filename):
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
