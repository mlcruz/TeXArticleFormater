import regex
import Abbrv
import unicodedata


log_file_data = []

class TeXIO(object):
    """Implements tex file IO and diff checking"""



    def __init__(self,tex_file_location,bib_file_location):
        """Create lists containing Tex/Bib file data from file"""
        log_file_data.clear()
        #clear log file

        self.tex_file_location = tex_file_location
        self.bib_file_location = bib_file_location
        self.log_file_location = (("{0}{1}").format(((self.bib_file_location).split(".")[0]),".log"))

        #reads Tex/Bib file, #Handles utf8/latin1 encoding and push to list.
        try:
            with open(tex_file_location,"r",encoding="utf8") as tex_reader:
                self.original_tex_data = tex_reader.readlines()
                self.current_tex_data = self.original_tex_data


        except UnicodeDecodeError:

            try:
                print("Error: Not utf8 - Trying Latin1 Decoding")
                log_file_data.append("Error:Tex file not unicode - Trying Latin1 Decoding\n")
                with open(tex_file_location,"r",encoding="latin-1") as tex_reader:
                    self.original_tex_data = tex_reader.readlines()
                    self.current_tex_data = self.original_tex_data
            except UnicodeDecodeError:
                print("Error: Not latin1- Trying cp1252 Decoding")
                log_file_data.append("Error: Not latin1- Trying ANSI Decoding")
                with open(tex_file_location,"r",encoding="cp1252") as tex_reader:
                    self.original_tex_data = tex_reader.readlines()
                    self.current_tex_data = self.original_tex_data


        try:
            with open(bib_file_location,"r",encoding="utf8") as bib_reader:
                self.original_bib_data = bib_reader.readlines()
                self.current_bib_data = self.original_bib_data
        except UnicodeDecodeError:

            try:
                print("Error:Bib file not not utf8 - Trying Latin1 Decoding")
                log_file_data.append("Error:Bib file not unicode - Trying Latin1 Decoding\n")
                with open(tex_file_location,"r",encoding="latin-1") as bib_reader:
                    self.original_bib_data = bib_reader.readlines()
                    self.current_bib_data = self.original_bib_data
            except UnicodeDecodeError:
                print("Error: Not latin1- Trying cp1252 Decoding")
                log_file_data.append("Error: Not latin1- Trying cp1252 Decoding")

                with open(tex_file_location,"r",encoding="cp1252") as tex_reader:
                    self.original_tex_data = tex_reader.readlines()
                    self.current_tex_data = self.original_tex_data


    def write_bib(self,dialog=0):
        """Writes current_bib_data to filename.new"""

        if dialog == 0:
            new_file_location = (("{0}_{1}").format(((self.bib_file_location).split(".")[0]),"new.bib"))
        else:
            new_file_location = self.bib_file_location

        with open(new_file_location,"w+",encoding="utf8") as bib_writer:
            for line in self.current_bib_data:
                bib_writer.write(line)

    def write_tex(self,dialog=0):
        """Writes current_tex_data to filename.new"""
        if dialog == 0:
            new_file_location = (("{0}_{1}").format(((self.tex_file_location).split(".")[0]),"new.tex"))
        else:
            new_file_location = self.tex_file_location

        with open(new_file_location,"w+",encoding="utf8") as tex_writer:
            for line in self.current_tex_data:
                tex_writer.write(line)


    def write_log(self,dialog=0):

        if dialog == 0:
            new_file_location = (("{0}_{1}").format(((self.log_file_location).split(".")[0]),".log"))
        else:
            new_file_location = self.log_file_location

        with open (new_file_location,"w+",encoding="utf8") as log_writer:
            for line in log_file_data:
                log_writer.write(line)




class Article(TeXIO):
    """Implements formating methods and initializes BibData/TexData/PreambleData objects"""

    def __init__(self,tex_file_location,bib_file_location,abbrv = 0):

        self.abbrv_local = abbrv
        """Separates the main file in 3 lists and initializes BibData/TexData/PreambleData objects with the data"""
        super().__init__(tex_file_location,bib_file_location)


        #finds line where the preamble ends
        preamble_found = self.current_tex_data.index("\\begin{document}\n")

        #Separates preamble and text in distinct objects
        self.preamble_data = PreambleData(self.current_tex_data[:preamble_found])
        self.tex_data = TexData(self.current_tex_data[preamble_found:])

    def init_bib(self):
        """Initializes and formats bibliography file"""
        #Merge multiline entries in bibliography file
        self.current_bib_data = (self.merge_lines(self.current_bib_data))

        #Initializes bibliography object with bibliography data
        self.bib_data = BibData(self.current_bib_data,self.abbrv_local)



    def merge_lines(self,a_file):
        """Merge multiline atributes in a bib file in a single line"""
        #Temp holder for non-terminated lines
        line_holder =""

        #line appended state; 0 = not appended, 1 = appended
        line_appended = 0

        #list to be returned by the function
        single_line_list = []

        for line in a_file:
            #matches every line terminated by , } "
            if regex.match(r'^.*([,\"}])\s*$',line):

                #if its a appended line, strips left side whitespaces and tabs
                if line_appended == 1:
                    line_striped = line.lstrip()
                else:
                    line_striped = line

                #Adds line to line_holder if its a terminated line.
                line_holder = '{0}{1}'.format(line_holder,line_striped)
                #appends terminated line to list
                single_line_list.append(line_holder)
                #clear line holder
                line_holder = ""

                line_appended = 0

            else:
                #if the line is not matched, its a non-terminated line
                #append line to temporary line holder
                line_holder = '{0}{1}'.format(line_holder,line.rstrip('\n'))
                line_appended = 1

        return single_line_list


    def normalize(input_text):
        """Normalizes strings and deals with some special chars"""
        return_str = regex.sub(r'\u00DF','ss',input_text,)
        return_str = regex.sub(r'\u1E9E','SS',return_str) # scharfes S
        return_str = regex.sub(r'\u0111','d',return_str,)
        return_str = regex.sub(r'\u0110','D',return_str) # crossed D
        return_str = regex.sub(r'\u00F0','d',return_str,)
        return_str = regex.sub(r'\u00D0','D',return_str) # eth
        return_str = regex.sub(r'\u00FE','th',return_str,)
        return_str = regex.sub(r'\u00DE','TH',return_str) # thorn
        return_str = regex.sub(r'\u0127','h',return_str,)
        return_str = regex.sub(r'\u0126','H',return_str) # H-bar
        return_str = regex.sub(r'\u0142','l',return_str,)
        return_str = regex.sub(r'\u0141','L',return_str) # L with stroke
        return_str = regex.sub(r'\u0153','oe',return_str,)
        return_str = regex.sub(r'\u0152','Oe',return_str) # Oe ligature
        return_str = regex.sub(r'\u00E6','ae',return_str,)
        return_str = regex.sub(r'\u00C6','Ae',return_str) # Ae ligature
        return_str = regex.sub(r'\u0131','i',return_str,) #dotless i
        return_str = regex.sub(r'\u00F8','o',return_str)
        return_str = regex.sub(r'\u00D8','O',return_str) # o with stroke
        return_str = regex.sub(r'[\u00B7\u02BA\uFFFD]','',return_str) # Catalan middle dot, double prime
        return_str = unicodedata.normalize('NFKD',return_str)
        return_str = regex.sub(r'[\u0300-\u036f]','',return_str) #Splits string into simple characters + modifiers and remove them

        return return_str


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
    incollection = ["author","title","booktitle","publisher","year","editor","volume","series","chapter","pages","address","edition"]
    manual = ["title","author","organization","address","edition","month","year"]
    mastersthesis = ["title","author","school","year","address"]
    misc = ["author","title","howpublished","month","year","note","url"]
    phdthesis = ["author","title","school","year","address"]
    proceedings = ["author","booktitle","title","year","editor","volume","series","address","month","organization","publisher"]
    inproceedings = ["author","booktitle","title","year","editor","volume","series","address","month","organization","publisher"]
    techreport =["author","title","institution","year","number","address"]
    report =["author","title","institution","year","number","address"]
    unpublished =["author","title","note","month","year"]
    online=["author","title","year","url"]


    #Initializes type dictionary
    cit_type_dict =  {"article":article,"book":book,"booklet":booklet,"conference":conference,"inbook":inbook,"incollection":incollection,"manual":manual, "mastersthesis":mastersthesis,"misc":misc,"phdthesis":phdthesis,"proceedings":proceedings,"inproceedings":inproceedings,"techreport":techreport,"report":report,"unpublished":unpublished,"online":online}


    bracket_stack = []

    def count_brackets(self,line):
        ''' Pushes brackets in the line into the bracket_stack for balancing'''
        for char in line:
            if char == '{':
                self.bracket_stack.append("{")

            if char == '}':

                self.bracket_stack.pop()




    def __init__(self, received_data, abbrv):
        """Populates a list of citation objects with the bibliography file data"""


        #variable for loop control. 0 = in the block ; 1 = outside of the block ; 2 = first line of the bib file
        self.end_of_cite = 2

        #Block that is being currently initialized
        self.cite_block =[]
        self.cite_block_library =[]
        label_pattern = regex.compile(r"@.+{\K[\w \d \: \_]+(?<!,$)",regex.IGNORECASE)

        #Fixes a weird bug related to reading the first entry in a file
        if(received_data[0][0] == ''):
            lista_temp = list(received_data[0])
            lista_temp.pop(0)
            received_data[0] = "".join(lista_temp)


        for line in received_data:



            #If the line starts an entry, begin another block
            matched = regex.match(r'@[\w \s]+(?={)',line,regex.IGNORECASE)
            matched_label = regex.match(label_pattern,line.lstrip())


            if (bool(matched)):

                self.end_of_cite = 0
                print("matched - type: {0}, label: {1}".format(matched.captures()[0],matched_label.captures()[0]))


            if(self.end_of_cite == 0):
                self.cite_block.append(line)
                self.count_brackets(line)


            #If the line ends in a block terminator(last } in the entry), change variable state to end of block
            if (self.bracket_stack == []) and self.end_of_cite == 0:
                #Removes last }/n in some entries
                if regex.sub(r'\s+', '',self.cite_block[-1]) == '}':
                    self.cite_block.pop()


                self.end_of_cite = 1


                self.cite_block_library.append(Citation(self.cite_block,self.cit_type_dict,abbrv))
                self.cite_block = []


    def generate_writable_bib_object(self,tag="N/A",comment=0):

        missing_tag = tag
        """Creates list containing a bibliography file text data with the current cite_block_library data"""
        file_data = []
        for citation in self.cite_block_library:
            #Write the first fixed line of each citation with type and label
            current_line = "@{0}{{{1},{2}".format(citation.citation_type,citation.label_name,'\n')
            file_data.append(current_line)

            #Write attribute data dict


            for key, value in citation.attribute_data_dict.items():
                if bool(value):
                    current_line = "\t{0} = {{{1}}},{2}".format(key,value,"\n")
                else:
                    current_line = "\t{0} = {{{1}}},{2}".format(key,missing_tag,"\n")

                file_data.append(current_line)

            if(comment == 1):
            #Write removed data as comments
                for line in citation.removed_camps:
                    current_line = "{0}%{1}{2}".format("\t",line.strip(),"\n")
                    file_data.append(current_line)


            #Close citation camp
            current_line = "}}{0}".format("\n")
            file_data.append(current_line)
            file_data.append("\n")

        return file_data

    def cull_useless(self,tex_cited):
        """"returns every citation in bibliography file and in the received list"""

        culled_list = []

        for item in self.cite_block_library:
            if item.label_name in tex_cited:
                culled_list.append(item)
            else:
                log_file_data.append("Removed {0}\n".format(item.label_name))
                print("Removed {0}".format(item.label_name))

        return culled_list


class TexData(GenericTex):

    def __init__(self, received_data):
        super().__init__(received_data)
        #pattern to serach for cited objects
        self.cite_pattern = regex.compile(r"\\cite{\K[\d \w \:]+",regex.IGNORECASE)

        #List of cited objects
        self.cited_list = []

        for line in self.received_data:
            if bool(regex.findall(self.cite_pattern,line)):
                for item in regex.findall(self.cite_pattern,line):
                    self.cited_list.append(item)


class PreambleData(GenericTex):

    def __init__(self, received_data):
        return super().__init__(received_data)




class Citation(object):


    """Citations represent a single reference entry in a bibliography file."""

    def __init__(self, cit_data, cit_dict,abbrv):
        """Initiliazes the citation object with raw text data from a list with data and a dictionary with the allowed attributes for each type of entry.
         Populates the attribute_data_dict atribute with data from bib file"""


        self.REGEX_FLAGS = regex.IGNORECASE|regex.MULTILINE|regex.UNICODE|regex.V1

        self.cit_data = cit_data
        self.cit_dict = cit_dict
        self.removed_camps = []
        self.attribute_data_dict = {}
        self.removed_data_dict = {}

       #pattern to search for citation type. matches every word after @ and before {
        self.type_pattern = regex.compile(r"(?:@)(\w*)(?:[\s]*)",self.REGEX_FLAGS)

        #pattern to search for label value. Matches every word-num in after the (@w+{) ending in a comma
        self.label_pattern = regex.compile(r"(?:^\s*@[\w \s]*{)(.*)(?:,)$",(self.REGEX_FLAGS))

        #pattern to search for camp type. Matches camp type in every line
        self.camp_pattern = regex.compile(r"^(?:\s*)(\b\w+)",(self.REGEX_FLAGS))

        #pattern to seach for camp data.
        self.data_pattern = regex.compile(r"^(?:[\s\w]*=[\s \{ \"]*)([a-zA-Z\u00C0-\u024F \s \d \- \. \' \– \( \) \$ \[ \] \% \’ \… \& \\ \/ \* \w \, \~ \{ \} \: \. \u0022 \` \~ \^ \¨ \# \@ \! \* \_ \+ \- \? \| \; \º \° \ç]*)(?:[\} \"]?,)$",(self.REGEX_FLAGS))

        #more generic patter to search for camp data
        self.generic_data_pattern = regex.compile(r"(?:\s[\{ \"\'])([\w \s]+)",self.REGEX_FLAGS)

        #Searches for citation type, removing any whitespace from citation type
        try:
            self.citation_type = regex.search(self.type_pattern,cit_data[0]).group(1)
            self.citation_type = self.citation_type.lower()
        except IndexError as err:
            print("Something bad happend here. Check bibliography entry formatting")
            log_file_data.append("Check bibliography entry formatting")

        #Searches for label name
        try:
            self.label_name = regex.search(self.label_pattern,cit_data[0]).group(1)
        except IndexError as err:
            print("Error: Can't find label name")
            log_file_data.append("")
            log_file_data.append(str(err))
            self.label_name = 'error'


        #Creates list with allowed citation camp attributes
        try:
            self.cit_allowed_list = self.cit_dict[self.citation_type.lower()]
        except KeyError as err:
            print( "!!-----Citation type unknown:{0}, defaulting as MISC-----!!".format(str(err)) )
            log_file_data.append("!!-----Citation type unknown:{0}, defaulting as MISC-----!!\n".format(str(err)))
            self.cit_allowed_list = self.cit_dict['misc']
            self.citation_type = 'misc'


        #Creates a null atribute_data_dict
        for type in self.cit_allowed_list:
            self.attribute_data_dict[type] = ''


        #Populate attribute_data_dict from data with the camp type as key and value as value.
        for key,line in enumerate(self.cit_data):
            if key > 0: #Skips matching the first line

                #Clean line for easier regex matching
                if(line.strip()[-1] != ','):
                    line = line.rstrip() + ',' #terminates with comma
                else:
                    line = line.rstrip() #rstrip

                #Remove closing terminator in a line for easier regex matching
                if(line[-2] == '}' or line[-2] == '"' or line[-2] == '"'):
                    line_array = list(line)
                    line_array.pop(-2) #Removes { or " or ' from item
                    line = "".join(line_array)
                    line = line + '\n' #Adds \n


                camp_type = regex.search(self.camp_pattern,line).group(1) #searches for citation camp type


                #Try searching for un-normalized camp data
                try: 
                    #Some optmizations to avoid computing regular expressions on large, useless blocks of text
                    if(camp_type != "abstract" and camp_type != "keywords" and camp_type != "issn" and camp_type != "doi" and camp_type !="timestamp" and camp_type != "acknowledgement" and camp_type != "bibsource"):
                        camp_data = regex.search(self.data_pattern,line).group(1) #Searches for citation camp data
                    else:
                        camp_data = None
                except Exception as e:
                    print("-Error on line {0}. Trying again after utf-8 normalization".format(line))
                    log_file_data.append("-Error on line {0}. Trying again after utf-8 normalization".format(line))
                    try:
                        camp_data = regex.search(self.data_pattern,Article.normalize(line)).group(1)
                        print("--Success!".format(line))
                        log_file_data.append("--Success!")
                    except Exception as t:
                        print("Failed to extract data after normalization at line {0}. Trying more generic capture".format(line))
                        log_file_data.append("Failed to extract data after normalization at line {0}. Trying more generic capture".format(line))
                        try:
                            camp_data = regex.search(self.generic_data_pattern,line).group(1)
                            print("---Success!".format(line))
                            log_file_data.append("---Success!")
                        except Exception as q:
                            try:
                                camp_data = regex.search(self.generic_data_pattern,Article.normalize(line)).group(1)
                                print("Success!".format(line))
                                log_file_data.append("---Success!")
                            except Exception as w:
                                print("Error matching camp data at {0}").format(line)
                                log_file_data.append("Error matching camp data at {0}".format(line))
                                camp_data = "error at {0}".format(line)


                if(camp_type in self.cit_allowed_list):
                    if((camp_type == "journal") and abbrv != 0 ):
                        #Abreviates serial titles
                        if(abbrv.isAbbrv(camp_data) == False):
                            abreviated = abbrv.abbreviate(camp_data)
                            self.attribute_data_dict.update({camp_type:abreviated})
                            print("-Abreviated journal title {0} from {1}\n".format(abreviated,camp_data))
                            log_file_data.append("-Abreviated journal title {0} from {1}\n".format(abreviated,camp_data))
                        else:
                            self.attribute_data_dict.update({camp_type:camp_data})
                            print("Failed to abreviate journal title {0}".format(camp_data))
                            log_file_data.append("Failed to abreviate journal title {0}".format(camp_data))
                    else:
                        self.attribute_data_dict.update({camp_type:camp_data}) #Populates citation if type is in allowed list
                else:
                    self.removed_data_dict[camp_type] = camp_data
                    self.removed_camps.append(line)
                    print("-removed {0} from {1}\n".format(camp_type,self.label_name)) #Populates removed items
                    log_file_data.append("-removed {0} from {1}\n".format(camp_type,self.label_name))




