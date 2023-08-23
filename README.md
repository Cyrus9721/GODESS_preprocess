# GODESS_preprocess: The preprocessing Github for the GODESS dataset
Data cleaning and preprocessing code for the simulated GODESS dataset, we also include a 2D GNN model as an example.

# Outline

- 1, PDB structure files produced by GODESS contain pairwise atom bond information while Glycosciences' PDB files do not.
These atom connections (stored in PDB format) helped match the monosaccharide ID between PDB file and csv file in a more automated way.

- 2, In Glycoscience the Acetyl (Ac) component is usually within monosaccharide name (e.g. GlcpNAc), GODESS treats it as separate 
    labeled components that is more clearly and consistently labeled (GlcpN / Ac) in the linear chemical formula, and all data files. This advantage enables us using the Ac interaction as extra feature at the atom-level. 

- 3, GODESS's terminal naming format for C and H, and double C/H is also internally consistent (e.g. H61,H62). 
    In contrast, Glycosciences data, has various inconsistent schemes, sometimes H61 is H6A, or H62 is H6B, or similar trends, etc. (C3a, C31). We 
  created lookup tables to resolve this issue in Glycosciences, but this was less needed in GODESS's data.

- 4, GODESS did not have missing shift issues to the extent Glycoscience did as it's an extensive simulation program rather than pure experimental data.

