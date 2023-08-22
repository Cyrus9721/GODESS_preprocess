import numpy as np
import pandas as pd
import shutil
from shutil import copyfile
from tqdm import tqdm
import os

pd.set_option('display.max_rows', 1000+1)


data_dir = 'dataset/Godess_carbon/'
pdb_out_dir = 'dataset/Godess_carbon_gnn/Godess_carbon_unmatched_pdb/'
csv_out_dir = 'dataset/Godess_carbon_gnn/Godess_carbon_unmatched_csv/'
name_out_dir = 'dataset/Godess_carbon_gnn/Godess_carbon_name.csv'

name_list = []
folder_names = os.listdir(data_dir)
def experiment_process_single_pdb(f):
    temp_shift = []
    for f_l in f:
        if 'HETATM' in f_l:
            temp_shift.append(f_l)

    new_shift = []
    for i in range(len(temp_shift)):
        temp_l = temp_shift[i].split(' ')
        temp_l_s = [i for i in temp_l if i != '']
        new_shift.append(temp_l_s[0:9] + list(temp_l_s[-2]))

    return new_shift

def extract_glycan_name(f):

    glycan_name = 'Missing glycan name'

    for f_l in f:
        if 'COMPND' in f_l:
            glycan_name = f_l.split('= ')[-1].split(' \n')[0]

    return glycan_name

def extract_process_single_label(c):
    new_g = []
    for c_l in c:
        c_temp = c_l.split('\t')

        new_l = []
        for i in c_temp:
            if '\n' in i:
                i = i.split('\n')[0]
            new_l.append(i)

        new_g.append(new_l)

    df = pd.DataFrame(new_g)

    df = df.rename(columns=df.iloc[0])
    df = df.tail(-1)
    df.index = range(len(df))




    return df


for i in range(len(folder_names)):

    folder = folder_names[i]
    pdb_path = os.path.join(data_dir, folder, 'PDB.pdb')
    label_path = os.path.join(data_dir, folder, 'c_tsv_hyb.txt')

    # pdb shifts
    with open(pdb_path) as f:
        f = f.readlines()
        new_shift = experiment_process_single_pdb(f)
        g_name = extract_glycan_name(f)

        df_pdb = pd.DataFrame(new_shift)


        # glycan names not included, in 549
        if g_name == 'Missing glycan name':
            continue

        # some pdb contain redundant columns
        if df_pdb.shape[1] > 10:

            df_pdb = df_pdb.iloc[:,:-1]

        df_pdb.columns = ['HETATM', 'Atom_num', 'Atom_name', 'Residual_name', 'Bound',
                          'Residual_num', 'x', 'y', 'z', 'Atom_type']


        df_pdb_out_path = os.path.join(pdb_out_dir, str(i) + '.pdb.csv')

        df_pdb.to_csv(df_pdb_out_path, index = False)

        name_list.append(g_name)

    # nmr labels
    with open(label_path) as c:
        c = c.readlines()
        df_label = extract_process_single_label(c)

        # some pdb shift contain more than 12 labels, this happens mostly from the
        if (df_label.shape[1] > 12):

            df_label = df_label.iloc[1:]
            df_label = df_label.dropna(axis=1, how='all')

        # one pdb contain only C1-C5, this happens because of the type of the monosaccharide
        elif (df_label.shape[1] < 9):
            print(df_pdb_out_path)
            df_label['C6'] = None

        df_label_out_path = os.path.join(csv_out_dir, str(i) + '.csv')

        df_label.to_csv(df_label_out_path, index = False)

    df_name = pd.DataFrame([str(i), name_list]).T
    df_name.to_csv(name_out_dir, index = False)
