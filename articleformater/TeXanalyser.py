import regex

class TeXIO(object):
    """Implements tex file IO and diff checking"""




    def __init__(self,tex_file_location,bib_file_location):
        """Create lists containing Tex/Bib file data from file"""
        
        self.tex_file_location = tex_file_location
        self.bib_file_location = bib_file_location

        #reads Tex/Bib file and push to list. 
        with open(tex_file_location,"r",encoding="utf8") as tex_reader:
            self.original_tex_data = tex_reader.readlines()
            self.current_tex_data = self.original_tex_data

        with open(bib_file_location,"r",encoding="utf8") as bib_reader:
            self.original_bib_data = bib_reader.readlines()
            self.current_bib_data = self.original_bib_data


    def write_bib(self):
        """Writes current_bib_data to filename.new"""

        new_file_location = (("{0}_{1}").format(((self.bib_file_location).split(".")[0]).lower(),"new.bib"))
        with open(new_file_location,"w",encoding="utf8") as bib_writer:
            for line in self.current_bib_data:
                bib_writer.write(line)

    def write_tex(self):
        """Writes current_tex_data to filename.new"""

        new_file_location = (("{0}_{1}").format(((self.tex_file_location).split(".")[0]).lower(),"new.tex"))
        with open(new_file_location,"w",encoding="utf8") as tex_writer:
            for line in self.current_tex_data:
                tex_writer.write(line)


class Article(TeXIO):
    """Implements formating methods and initializes BibData/TexData/PreambleData objects"""
    
    def __init__(self,tex_file_location,bib_file_location):

       

        """Separates the main file in 3 lists and initializes BibData/TexData/PreambleData objects with the data"""
        super().__init__(tex_file_location,bib_file_location)
        
        #finds line where the preamble ends
        preamble_found = self.current_tex_data.index("\\begin{document}\n")

        #Separates preamble and text in distinct objects
        self.preamble_data = PreambleData(self.current_tex_data[:preamble_found])
        self.tex_data = TexData(self.current_tex_data[preamble_found:])
        
        #Initializes bibliography object
        self.bib_data = BibData(self.current_bib_data)
        
        
        #


class GenericTex(object):
    """Generic class implementing IO and diff checking to be inherited by BibData/TexData/PreambleData objects"""
    
    def __init__(self, received_data):
        self.received_data = received_data

class BibData(GenericTex):
    """Implements bibliography formating methods"""

     #Lists for attributes of each citation type

    article =["author","title","journal","year","number","pages","volume"]
    book = ["author","title","publisher","year","volume","series","address","edition"]
    booklet =["title","author","howpublished","address","month","year"]
    conference = ["author","title","year","editor","volume","series","pages","address","publisher"]
    inbook = ["author","title","chapter","pages","publisher","year","volume","series","address","edition"]
    incollection = ["author","title","publisher","year","editor","volume","series","chapter","pages","address","edition"]
    manual = ["title","author","organization","address","edition","month","year"]
    mastersthesis = ["title","author","school","year","address"]
    misc = ["author","title","howpublished","month","year","note"]
    phdthesis = ["author","title","school","year","address"]
    proceedings = ["author","title","year","editor","volume","series","address","month","organization","publisher"]
    inproceedings = ["author","title","year","editor","volume","series","address","month","organization","publisher"]
    techreport =["author","title","institution","year","number","address"]
    report =["author","title","institution","year","number","address"]
    unpublished =["author","title","note","month","year"]
    online=["author","title","year","url"]


    #Initializes type dictionary
    cit_type_dict =  {"article":article,"book":book,"booklet":booklet,"conference":conference,"inbook":inbook,"incollection":incollection,"manual":manual, "mastersthesis":mastersthesis,"misc":misc,"phdthesis":phdthesis,"proceedings":proceedings,"inproceedings":inproceedings,"techreport":techreport,"report":report,"unpublished":unpublished,"online":online}
    



    def __init__(self, received_data):
        """Creates a list of citation objects with raw bibliograpy data in a list"""


        self.end_of_cite = 0
        self.cite_block =[]
        self.cite_block_library =[]

        for line in received_data:
            print("welp")
            #If the line starts an entry, begin another block
            if (regex.match(r'@\w+(?={)',line,regex.IGNORECASE)):
                self.end_of_cite = 0
                print("match")
            if regex.match(r'(?<!(\d|\w|\.|,))}(?=\n)',line,regex.IGNORECASE):
                self.end_of_cite = 1
            if(self.end_of_cite == 0):
                self.cite_block.append(line)
            if(self.end_of_cite == 1):
                self.cite_block.append(line)
                if (self.cite_block[0] == '\n'):
                    print("discarded")
                    self.cite_block = []
                else:
                    self.cite_block_library.append(Citation(self.cite_block,self.cit_type_dict))
                    self.cite_block = []

    

class TexData(GenericTex):
    
    def __init__(self, received_data):
        return super().__init__(received_data)


class Citation(object):

        
    """Data structures  and formating for each reference """
    
    def __init__(self, cit_data, cit_dict):
        self.REGEX_FLAGS = regex.IGNORECASE|regex.MULTILINE|regex.UNICODE|regex.V1
        self.bib_data_string = ""
        self.cit_data = cit_data
        self.cit_dict = cit_dict
        #Tries to search for citation type. matches every word after @ and before {
        self.type_pattern = regex.compile(r"@\K\b\w+(?<=)",self.REGEX_FLAGS)

        #Tries to search for label value. Matches every word-num in after the (@w+{) ending in a comma
        self.cite_label_pattern = regex.compile(r"@\w+{\K[\w +\d]+(?<!,$)",(self.REGEX_FLAGS))

        #Searches for article type
        self.citation_type = regex.findall(self.type_pattern,cit_data[0])[0]

        #Creates list with allowed citation camps
        self.cit_allowed_list = self.cit_dict[self.citation_type.lower()]


        #Creates dictionary using allowed item types as keys and the respective camp value in the citation data
        self.attribute_data_dict = {
            type:[self.gen_regex_pattern(type).match(x).captures()[0][0] for x in self.cit_data if self.gen_regex_pattern(type).match(x)] for type in self.cit_allowed_list}
            

    def gen_regex_pattern(self,cit_type):
        """ Generates regex string with the type passed to the function to search for text inside  brtackets from cit_type={} in each citation camp"""

        #Strings to generate regex to to search for cit_type value. Matches everything after author= and before ,} or '',

        self.regex_gen_part1 = r'((( |\t)*'
        self.regex_gen_part2 = r')[ =]+)[{"]\K.+(?=((}|")(,|\n)$))'
        return regex.compile("{0}{1}{2}".format(self.regex_gen_part1,cit_type,self.regex_gen_part2),self.REGEX_FLAGS)



    
class PreambleData(GenericTex):
    
    def __init__(self, received_data):
        return super().__init__(received_data)



dados = Article("article_3.tex","Bibliografia.bib")
#a = Citation(dados.current_bib_data)

print ("WELP")
