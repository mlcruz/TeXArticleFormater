# TeXArticleFormater
Library to simplify LaTeX files parsing and analysis with python:

Functionalities:


Todo: Everything else.


-0.1: Reads.bib file and populate BibData class with Citation objects.

0.1:

Classes:

Article= Reads raw .tex and .bib files and creates PreambleData,TexData and Bib(liography)Data objects. 

BibData:Class containing a list with citation objects(BibData.cite_block_library). Each citation object is initialized with a list containing a single
reference camp raw text data.

Citation:Class representing a single bibliography file citation(label,type,values). Takes a list and a dictionary of allowed camps for each type of
reference entry and generate the regex patterns to search for the specified camps. Populates the self.attribute_data_dict dictionary
with {'attribute':'value'}(ex:{author:"Alan Mathison Turing",title:"COMPUTING MACHINERY AND INTELLIGENCE"..} and the self.removed_camps
list with whatever camps are removed(everything not specified in allowed camps dictionary). Also has label and citation type data and a regex
string generator method.

PreambleData:class containing a list with preamble data (everything before \begindocument) and io methods.

TexData:class containing a list with Tex file data (everything after \begindocument) and io methods.
