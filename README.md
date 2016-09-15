# security

A Collection of code to break classical ciphers

Note
- If you are using this to break your own ciphers I would focus on the cython/packages/ scripts as they have better documentation.
- cython directory houses code for specific ciphers.
- cython/packages houses general code for analysing, breaking and brutefocing common ciphers.
- cython/packages should be built using cython to increase compute speed using 'python3 setup.py build_ext --inplace'

cython/corpus_start.py
- A collection of scripts for analysing corpus.

cython/quag_start.py
- A script created to break a specific quagmire-like cipher.

cython/rail_fence.py
- A script to brute force rail_fence ciphers.

cython/runnning_start.py
- depretiated?

cython/son_rail_start.py
- A script created to break a specfic rail fence-like cipher.

cython/start.py
- A script for breaking specific transpositional and substition ciphers.

cython/word_builder
- A script used to create a list of words from a given set of characters.

cython/packages/pad.py
- A collection of scripts to brute forceing ciphers.

cython/packages/analyse.py
- A collection of scripts to break ciphers.

cython/packages/pre-analysis.py
- A collection of scripts used to discover details of ciphers.
