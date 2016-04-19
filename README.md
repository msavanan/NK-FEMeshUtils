# NK-FEMeshUtils
Python implementation for handling of FE Mesh data.

This Module was created for handling Mesh Data. Data is currently stored in Dictionaries.
Due to the Hashtable structure accessing specific data is quite fast. 
In order to perform operations with the mesh entities a object structure has been implemented.

To use this object structure you have to initialize these objects. 
In is not done automatically in order to make it possible to handle large models but only do calculation on a subset of parts.
Therefore you can either init Objects by part ID or just init all Objects. 

In pure python Initialization of all Objects take approx. 60 sec for the Taurus model.
In cython this time is cut down to 40 sec. 