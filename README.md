## Data cleaning and preprocessing directory for GODESS dataset。


### Data cleaning, preprocessing and annotating doc for simulated GODESS dataset

1, Read in the PDB file, label file that contains NMR shift values, and create atom connection file from the PDB file.

- PDB structure files produced by [GODESS](https://drive.google.com/file/d/15qIixe-irZyJKzvuoINuK1-d53nC8Jyh/view?usp=sharing) contain pairwise atom bond information while [Glycoscience](https://github.com/Cyrus9721/GlycoscienceDB_preprocess) PDB files do not.
These atom connections (stored in PDB format) helped match the monosaccharide ID between PDB file and csv file in a more automated way.

2, Identify the monosaccharide components in the PDB file. Align the monosaccharide IDs between the PDB file and the label file with the help of the atom connection. Indentify non-monosaccharide components with the help of the atom connection information. 

- 2.1 For example the monosaccharide bound '(1-3)' indicates the carbon with position number 1 is connected to the carbon with position number 3 via dehydration synthesis reaction. Therefore, with the atom connection information, we can manually assign monosaccharides IDs for all the atoms in the PDB file. 

- 2.2 GODESS's terminal naming format for C and H, and double C/H is also internally consistent (e.g. H61,H62). 
    In contrast, Glycosciences data, has various inconsistent schemes, sometimes H61 is H6A, or H62 is H6B, or similar trends, etc. (C3a, C31). We 
  created lookup tables to resolve this issue in Glycosciences, but this was less needed in GODESS's data.

- 2.3 In Glycoscience the Acetyl (Ac) component is usually within monosaccharide name (e.g. GlcpNAc), GODESS treats it as separate 
labeled components that is more clearly and consistently labeled (GlcpN / Ac) in the linear chemical formula, and all data files. This advantage enables us using the Ac interaction as extra feature at the atom-level. The non-monosaccharide components from the PDB file can also be obtained (and verified)using atom connection information.

- 2.4 GODESS did not have missing shift issues to the extent Glycoscience did as it's an extensive simulation program rather than pure experimental data.

3, To verify whether we aligned the monosaccharides between the PDB file(document at three letter abbreviation from the simulation software) and the label file(document as full monosaccharide name) correctly, we created a matching table to examine manually of the matching results. If there are exceptions, we then go back to step2.

4, We apply feature engineering to the full monosaccharides. Extract some useful features like fischer projection, bond information etc.

5, Some non-monosaccharide components (Ac) are completely messed up, we check whether some Ac components are mislabeled, or treated as monosaccharides. If it is we then go back to step 2 and re-run the whole process. 

6, We run a simple GNN model and check for outliers. We then conduct manually examinations, if the outlier is from annotation error, we then go back to step 2 and re-run the whole process. 

7, We identify some rarely appeared monosaccharides (like appears only once) and drop the carbohydrates.

---

### Preliminary results of 2D GNN.

This is created to visualize the overall performance of 2D GNN on GODESS dataset. 

![gcn_all](/figures/testing_complete_label_v4.png?raw=true) <br />
