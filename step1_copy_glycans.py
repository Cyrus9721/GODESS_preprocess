import numpy as np
import pandas as pd
import shutil
from shutil import copyfile
from tqdm import tqdm
import os

source_list = ['Experimental_1D/', 'Theoretical_NewGlycans_MaxLength20/']
out_dir = 'dataset/Godess_carbon/'

prev_source_list = []
prev_file_name = []

new_file_name = []

i = 1
for s in source_list:
    s_files_names = os.listdir(s)

    for f in s_files_names:
        s_files_path = os.path.join(s, f)

        temp_glycan_all_files = os.listdir(s_files_path)

#         if 'PDB.pdb' in temp_glycan_all_files:
#             pass
#         else:
#             print(s_files_path, 'is missing PDB file')

#         if 'c_tsv_hyb.txt' in temp_glycan_all_files:
#             pass
#         else:
#             print(s_files_path, 'is missing c_tsv_hyb.txt')

        if ('PDB.pdb' in temp_glycan_all_files) and ('c_tsv_hyb.txt' in temp_glycan_all_files):

            new_dir_name = os.path.join(out_dir, str(i))

            os.makedirs(new_dir_name)

            old_pdb_path = os.path.join(s_files_path, 'PDB.pdb')

            old_label_path = os.path.join(s_files_path, 'c_tsv_hyb.txt')

            new_pdb_path = os.path.join(new_dir_name, 'PDB.pdb')

            new_label_path = os.path.join(new_dir_name, 'c_tsv_hyb.txt')

            copyfile(old_pdb_path, new_pdb_path)

            copyfile(old_label_path, new_label_path)

            prev_source_list.append(s)
            prev_file_name.append(f)
            new_file_name.append(i)


            i += 1



