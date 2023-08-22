# GODESS_preprocess: The preprocessing Github for the GODESS dataset
Data cleaning and preprocessing code for the simulated GODESS dataset, we also include a 2D GNN model as an example.

# Outline

- 1, PDB structure files produced by GODESS contain pairwise atom bond information while Glycosciences' PDB files do not.
These atom connection(stored in pdb) info helped match the monosaccharide ID between PDB file and csv file in a more automated way.

- 2, In Glycoscience the Acetyl (Ac) component is usually within monosaccharide name (e.g. GlcpNAc), GODESS treats it as separate 
    labeled components that is more clearly labeled (GlcpN / Ac), this enables us using the Ac interaction as extra feature at the atom-level. 

- 3, GODESS's terminal naming format for C and H, and double C/H is internally consistent (e.g. H61,H62). 
    In contrast, glycoscience's data, has various inconsistent schemes, sometimes H61 is H6A, or H62 is H6B things, etc.. C3a, C31 things. We 
  created lookup tables to resolve this issue in Glycosciences, but this was less needed in GODESS's data.

- 4, GODESS did not have missing shift issues to the extend Glycoscience did as it's a simulation program.

