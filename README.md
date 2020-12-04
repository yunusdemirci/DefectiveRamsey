Defective Ramsey
======

Python 3 code for dealing with finite, simple graphs. Allows for
computation of defective Ramsey numbers and associated extremal
graphs.

This package is a companion to Defective Ramsey Numbers and Cocolorings on Some
Subclasses of Perfect Graphs by Yunus Emre Demirci, Tınaz Ekim and Mehmet Akif Yıldız

Package repository: https://github.com/yunusdemirci/DefectiveRamsey

Usage
-----

In its current form, DefectiveRamsey requires that the user be at least somewhat
familiar with Python and/or a Unix-derived shell or similar command-line
interface.

DefectiveRamsey consists of executable program (`defectiveramsey.py`) and two importable libraries used by these (`isograph.py`, `gengraph.py`). All are intended for use with Python 3. One of them (`isograph.py`) taken from GraphR can be found https://github.com/ggchappell/GraphR . Please read https://github.com/ggchappell/GraphR/blob/master/LICENSE .

To compute the _defective Ramsey number at stated subclass R^C_k(a, b), run `defectiveramsey.py`, passing k, a, b, C as command-line arguments. k, a, b represent numbers and C represents string.

    > defectiveramsey.py 1 4 7 "bip"

To compute the _defective Ramsey number at stated subclass with initial base graphs R^C_k(a, b), add initial base graphs to "base.txt" and run `defectiveramsey.py`, passing k, a, b, C as command-line arguments. k, a, b represent numbers and C represents string.

    > defectiveramsey.py --base 1 4 7 "bip"

C represents graph subclass. We just implement for two graph subclass.
"bip": can be used for bipartite graphs
"pg": can be used for perfect graphs
"all": can be used for all graphs without restriction. 


*See the individual files for API documentation. Data formats are described in
`isograph.py`.

Files
-----

* `isograph.py` -- Importable module. Functions for dealing with simple
  graphs & graph isomorphism.
* `gengraph.py` -- Importable module. Functions for finding defective
  Ramsey numbers & related extremal graphs. Requires `isograph.py`.
* `defectiveramsey.py` -- Executable program. Computes
  defectve Ramsey numbers. Requires `isograph.py` and `gengraph.py`.
* `RESULTS` -- Subdirectory for text files holding output of
  `defectiveramsey.py`. Files named `R^*_#def_#dense_#sparse.txt`,
  where `#` represents a integer, and `*` represents a string. The
  numbers in the filename are the command-line parameters. For example,
  file `R^BIP_1def_4dense_4sparse.txt` holds the output from the command
  `defectiveramsey.py 1 4 4 "bip" `.
* `Defective Cocoloring`. All executable programs and results for defective cocoloring version. For detailed information, please read `README.md` file in subdirectory
* `README.md` -- This file.