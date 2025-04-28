# PersianVerbNet
A testing project for making a Persian Verbnet-style Dataset based on the Colorado open-source English VerbNet.

The output is a dataset of TTL format files that was basically implemented with these assumptions:
- A class is considered for each verb
- A higher class is considered for verb categories, thus creating a hierarchy of verbs.
- Thematic relations were also represented both in the form of OWL logical constraints and placed in class categories corresponding to these constraints.
- The correspondence between linguistic layer and semantic structures expressed in the form of templates is not currently included in this dataset. I have designed a special database to retrieve these templates, which is not yet complete.
