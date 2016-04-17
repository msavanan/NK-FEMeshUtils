# NK-FEMeshUtils
Python implementation for handling of FE Mesh data.

This Module was created for handling Mesh Data. Data is currently stored in Dictionaries.
Due to the Hashtable structure accessing specific data is quite fast.
Nevertheless Mass / Volume calculation for a single part in a large assembly mesh is slow
Therefore it is better to use the ObjectStructure and the Part.getPartMass() Method

