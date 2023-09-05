## Data cleaning and preprocessing directory for GODESS dataset。


### Data cleaning, preprocessing and annotating doc for simulated GODESS dataset

We summarize the whole process into 7 steps below. Researchers interested in uploading carbohydrate data to this or other similar datasets should note that this preprocessing pipeline could be streamlined greatly if more completely and consistently annotated data is uploaded by the researchers who generated it.

1, Read-in the PDB file and the label file that contains NMR shift values, and then create atom connection file from the PDB file.

- PDB structure files produced by [GODESS](https://drive.google.com/file/d/15qIixe-irZyJKzvuoINuK1-d53nC8Jyh/view?usp=sharing) contain pairwise atom bond information while [Glycoscience](https://github.com/Cyrus9721/GlycoscienceDB_preprocess) PDB files do not. Glycoscience files however contain helpful monosaccharide linkage notes at the bottom of the PDB files that are not present in GODESS files. Thus the atom connections (stored in PDB format) helped match the monosaccharide ID between PDB file and csv file in a more automated way in GODESS.

2, Identify the monosaccharide components in the PDB file. Align the monosaccharide IDs between the PDB file and the label file with the help of the atom connection in GODESS or the monosaccharide linkage notes in the bottom of Glycoscience PDB files. Indentify non-monosaccharide components with the help of the atom connection information. 

- 2.1 For example the monosaccharide bound '(1-3)' indicates the carbon with position number 1 is connected to the carbon with position number 3 via dehydration synthesis reaction. Therefore, with the complete atom connection information, we can manually assign monosaccharides IDs for all the atoms in the PDB file. 

- 2.2 GODESS's terminal naming format for C and H, and double C/H is also internally consistent (e.g. H61,H62). 
    In contrast, Glycosciences data, has various inconsistent schemes, sometimes H61 is H6A, or H62 is H6B, or similar trends, etc. (C3a, C31). We 
  created lookup tables to resolve this inconsistent formatting issue in Glycosciences, but this was less needed in GODESS's data.

- 2.3 In Glycoscience the Acetyl (Ac) component is usually within monosaccharide name (e.g. GlcpNAc). When not specified Ac is usually a (1-2) linkage, though not always and usually when not specified as Glcp4Ac for C4 for example. GODESS treats Ac as a separate 
labeled component that is more clearly and consistently labeled ( GlcpNAc -> GlcpNAc -> Ac(1-2)GlcpN ) in the linear chemical formula, as well as in all shift and structure data files. This consistency advantage enables us to use the Ac interaction easily as an extra feature at the atom-level when modeling the GODESS data. Other non-monosaccharide components from the PDB file can also be obtained (and verified) using atom connection information. Future work could additionally use the linear chemical formula to find and validate non-monosaccharide components.

- 2.4 GODESS did not have missing shift issues to the extent Glycoscience did as it's an extensive simulation program rather than pure experimental data.

3, To verify whether we aligned the monosaccharides between the PDB file (document at three letter abbreviation from the simulation software) and the label file (document as full monosaccharide name) correctly, we created a matching table to allow easier manual or semi-automated validation of the matching between NMR and PDB rows. If there are exceptions, we then go back to step2.

4, We apply feature engineering to the full monosaccharides including extracting some useful features like fischer projection, bond information etc.

5, Sometimes Ac especially is annotated in an inconsistent way. E.g. sometimes within a single file, Ac's atoms might be given a separate Ac monosaccharide column label in one monosaccharide unit (despite not being a monosaccharide), but in the same file a different Ac's atoms are merged with the parent monosaccharide label. Analogously ambigous situations can exist in the NMR files. Using a list of exceptions to establish whether these or similar inconsistencies exist, we semi-automatically find them and validate with manual checks, then go back to step 2 and re-run the whole process. 

6, Over the course of the project, to more efficiently find the worst or most common outliers caused by ambiguous annotation first, we repeatedly ran a simple GNN model on coarsely-grained curated data and check for ranked discrepency outliers. We then conduct manually examinations, if the outlier is from annotation problem as usual, we then go back to step 2 and re-run the whole process. Outliers not directly caused by an annotation were typically a secondary effect of a view common primary issue that biased the model in some ways. This iterative process plus chemistry knowledge allowed us to compile exhaustive lists and lookup tables to solve the ambiguities in annotation in the original dataset. Again we strongly encourage experimental researchers in glycosciences to adopt more uniform annotation standards in the future to avoid the need for such extensive curation as datasets grow.

7, We identified some rarely occurring monosaccharides units (e.g. only appear once or twice) and dropped them due to insufficient statistics. These dropped glycans were not included in our dataset size count.

---

### Preliminary results of 2D GNN.

This is created to visualize the overall performance of 2D GNN on GODESS dataset. 

![gcn_all](/figures/testing_complete_label_v4.png?raw=true) <br />
