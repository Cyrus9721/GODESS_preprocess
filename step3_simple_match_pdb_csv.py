import numpy as np
import pandas as pd
import shutil
from shutil import copyfile
from tqdm import tqdm
import os

pd.set_option('display.max_rows', 1000+1)


pdb_dir = 'dataset/Godess_carbon_gnn/Godess_carbon_unmatched_pdb/'
csv_dir = 'dataset/Godess_carbon_gnn/Godess_carbon_unmatched_csv/'
out_labeled_pdb_dir = 'dataset/Godess_carbon_gnn/Godess_carbon_labeled_pdb/'
carbon_list = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
hydrogen_list_1_6 = ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9']
pdb_files = os.listdir(pdb_dir)
csv_files = os.listdir(csv_dir)
three_letter_non_residual_list = ['PDa', 'ACY']
incorrect_pdb_list = ['1983.pdb.csv', '690.pdb.csv', '441.pdb.csv', '737.pdb.csv']

ct = 0
for i in tqdm(range(len(pdb_files))):
# for i in range(len(pdb_files)):
# for i in range(1):
# for i in [30]:
# for i in [40]:
# for i in [40]:

# for i in range(1786, len(pdb_files)):
    pdb_name = pdb_files[i]
    csv_name = pdb_name.replace('.pdb.csv', '.csv')

    pdb_name_path = os.path.join(pdb_dir, pdb_name)
    csv_name_path = os.path.join(csv_dir, csv_name)

    pdb_f = pd.read_csv(pdb_name_path)
    csv_f = pd.read_csv(csv_name_path)

    csv_f = csv_f.loc[csv_f['Residue'] != 'Ac']
    csv_f.index = range(len(csv_f))


    if pdb_name in incorrect_pdb_list:
        continue

    if len(csv_f) == len(np.unique(pdb_f['Residual_num'])):
        pass
    else:
        print(csv_name)
        ct += 1

    temp_labels = np.repeat(-1.0, len(pdb_f))

    prev_residual_name = ''

    # if we see and ACY, skip the label of it.
    diff = 1
    for j in range(len(pdb_f)):

        current_atom_type = pdb_f.loc[j, ['Atom_name']].values[0]
        current_residual = pdb_f.loc[j, ['Residual_num']].values[0]

        current_residual_name = pdb_f.loc[j, ['Residual_name']].values[0]

        if (current_residual_name in three_letter_non_residual_list) and \
            (prev_residual_name not in three_letter_non_residual_list):
            diff += 1

        prev_residual_name = current_residual_name

        if current_atom_type in carbon_list:
            corresponding_residual = current_residual - diff

            if csv_f.loc[corresponding_residual, [current_atom_type]].values[0]:

                current_shift_val = csv_f.loc[corresponding_residual, [current_atom_type]].values[0]

                if current_shift_val == '?':
                    current_shift_val = -1

                temp_labels[j] = current_shift_val

    pdb_f_labeled = pdb_f.copy()
    pdb_f_labeled['label'] = temp_labels

    current_out_path = os.path.join(out_labeled_pdb_dir, str(i) + '.csv')

    pdb_f_labeled.to_csv(current_out_path, index = False)
