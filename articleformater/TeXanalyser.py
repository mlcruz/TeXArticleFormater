import regex
import colorama


log_file_data = []

class TeXIO(object):
    """Implements tex file IO and diff checking"""

    def __init__(self,tex_file_location,bib_file_location):
        """Create lists containing Tex/Bib file data from file"""
        log_file_data.clear()
        #clear log file
       
        self.tex_file_location = tex_file_location
        self.bib_file_location = bib_file_location
        self.log_file_location = (("{0}{1}").format(((self.bib_file_location).split(".")[0]).lower(),".log"))

        #reads Tex/Bib file, #Handles utf8/latin1 encoding and push to list. 
        try:        
            with open(tex_file_location,"r",encoding="utf8") as tex_reader:
                self.original_tex_data = tex_reader.readlines()
                self.current_tex_data = self.original_tex_data
        
        
        except UnicodeDecodeError:
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "Error: Not unicode - Trying Latin1 Decoding" +colorama.Style.RESET_ALL)
            log_file_data.append("Error:Tex file not unicode - Trying Latin1 Decoding\n")
            with open(tex_file_location,"r",encoding="latin-1") as tex_reader:
                self.original_tex_data = tex_reader.readlines()
                self.current_tex_data = self.original_tex_data
                
        try:
            with open(bib_file_location,"r",encoding="utf8") as bib_reader:
                self.original_bib_data = bib_reader.readlines()
                self.current_bib_data = self.original_bib_data
        except UnicodeDecodeError:
            print(colorama.Fore.RED + colorama.Style.BRIGHT + "Error:Bib file not unicode - Trying Latin1 Decoding" +colorama.Style.RESET_ALL)
            log_file_data.append("Error:Bib file not unicode - Trying Latin1 Decoding\n")
            with open(tex_file_location,"r",encoding="latin-1") as bib_reader:
                self.original_bib_data = bib_reader.readlines()
                self.current_bib_data = self.original_bib_data




    def write_bib(self,dialog=0):
        """Writes current_bib_data to filename.new"""
        
        if dialog == 0:
            new_file_location = (("{0}_{1}").format(((self.bib_file_location).split(".")[0]).lower(),"new.bib"))
        else:
            new_file_location = self.bib_file_location

        with open(new_file_location,"w",encoding="utf8") as bib_writer:
            for line in self.current_bib_data:
                bib_writer.write(line)

    def write_tex(self,dialog=0):
        """Writes current_tex_data to filename.new"""
        if dialog == 0:
            new_file_location = (("{0}_{1}").format(((self.tex_file_location).split(".")[0]).lower(),"new.tex"))
        else:
            new_file_location = self.tex_file_location

        with open(new_file_location,"w",encoding="utf8") as tex_writer:
            for line in self.current_tex_data:
                tex_writer.write(line)


    def write_log(self,dialog=0):
        with open (self.log_file_location,"w",encoding="utf8") as log_writer:
            for line in log_file_data:
                log_writer.write(line)



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
        
        #Merge multiline entries in bibliography file
        self.current_bib_data = (self.merge_lines(self.current_bib_data))

        #Initializes bibliography object with bibliography data
        self.bib_data = BibData(self.current_bib_data)

        

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
    misc = ["author","title","howpublished","month","year","note"]
    phdthesis = ["author","title","school","year","address"]
    proceedings = ["author","booktitle","title","year","editor","volume","series","address","month","organization","publisher"]
    inproceedings = ["author","booktitle","title","year","editor","volume","series","address","month","organization","publisher"]
    techreport =["author","title","institution","year","number","address"]
    report =["author","title","institution","year","number","address"]
    unpublished =["author","title","note","month","year"]
    online=["author","title","year","url"]


    #Initializes type dictionary
    cit_type_dict =  {"article":article,"book":book,"booklet":booklet,"conference":conference,"inbook":inbook,"incollection":incollection,"manual":manual, "mastersthesis":mastersthesis,"misc":misc,"phdthesis":phdthesis,"proceedings":proceedings,"inproceedings":inproceedings,"techreport":techreport,"report":report,"unpublished":unpublished,"online":online}
    



    def __init__(self, received_data):
        """Populates a list of citation objects with the bibliography file data"""

        #variable for loop control. 0 = in the block ; 1 = end of block; 2 = outside of the block. 
        self.end_of_cite = 0

        #Block that is being currently initialized
        self.cite_block =[]
        self.cite_block_library =[]
        label_pattern = regex.compile(r"@.+{\K[\w \d \: \_]+(?<!,$)",regex.IGNORECASE)


        for line in received_data:
            
            #If the line starts an entry, begin another block
            matched = regex.match(r'@\w+(?={)',line,regex.IGNORECASE)
            matched_label = regex.match(label_pattern,line)


            if (bool(matched)):
                
                self.end_of_cite = 0
                print("matched - type: {0}, label: {1}".format(matched.captures()[0],matched_label.captures()[0]))

            #If the line ends in a block terminator(last } in the entry), change variable state to end of block
            if regex.match(r'(?<!(\d|\w|\.|,))}(?=\n)',line,regex.IGNORECASE):
                self.end_of_cite = 1

            
            if(self.end_of_cite == 0):
                self.cite_block.append(line)

            elif(self.end_of_cite == 1):
                self.cite_block.append(line)
                #discard empty text
                if (self.cite_block[0] == '\n'):
                    print("discarded")
                    self.cite_block = []
                else:
                    self.cite_block_library.append(Citation(self.cite_block,self.cit_type_dict))
                    self.cite_block = []


        
    def generate_writable_bib_object(self,tag="N/A"):
        
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
                    current_line = "\t{0} = {{{1}}},{2}".format(key,value[0],"\n")
                else:
                    current_line = "\t{0} = {{{1}}},{2}".format(key,missing_tag,"\n")

                file_data.append(current_line)
           
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





class Citation(object):

        
    """Citations represent a single reference entry in a bibliography file."""
    
    def __init__(self, cit_data, cit_dict):
        """Initiliazes the citation object with raw text data in a list from a single bibliography entry and a dictionary with the allowed attributes for each type of entry.
        and populates the attribute_data_dict dictionary with the data(key=citation type;Value=camp value(searched with the gen_regex_pattern function)""" 
        
        
        self.REGEX_FLAGS = regex.IGNORECASE|regex.MULTILINE|regex.UNICODE|regex.V1

        self.cit_data = cit_data
        self.cit_dict = cit_dict
        
        
        self.removed_camps = []
        
       #pattern to search for citation type. matches every word after @ and before {
        self.type_pattern = regex.compile(r"@\K\b[\w \s]*",self.REGEX_FLAGS)

        #pattern to search for label value. Matches every word-num in after the (@w+{) ending in a comma
        self.label_pattern = regex.compile(r"@.+{\K[\w \d \: \_ ]+(?<!,$)",(self.REGEX_FLAGS))

        #Searches for citation type
        try:
            self.citation_type = regex.findall(self.type_pattern,cit_data[0])[0]
        except IndexError as err:
            print(colorama.Fore.RED + colorama.Back.WHITE + colorama.Style.BRIGHT + "Something bad happend here. Check bibliography entry formatting, probably some whitespace is messing things up. defaulting as misc" + colorama.Style.RESET_ALL)
            log_file_data.append("Check for whitespaces in the bibliography file. being unable to read '@type {foo,' entries is a known bug")
            log_file_data.append(str(err))
            self.citation_type = 'misc'


        #Searches for label name
        try:
            self.label_name = regex.findall(self.label_pattern,cit_data[0])[0]
        except IndexError as err:
            print(colorama.Fore.RED + colorama.Back.WHITE + colorama.Style.BRIGHT + "Something bad happend here. Check bibliography entry formatting, probably some whitespace is messing things up. defaulting as misc" + colorama.Style.RESET_ALL)
            log_file_data.append("Check for whitespaces in the bibliography file. being unable to read '@type {foo,' entries is a known bug")
            log_file_data.append(str(err))
            self.label_name = 'error'


        #Creates list with allowed citation camp attributes
        try:
            self.cit_allowed_list = self.cit_dict[self.citation_type.lower()]
        except KeyError as err:
            print(colorama.Style.BRIGHT +colorama.Fore.RED + "!!-----Citation type unknown:{0}, defaulting as MISC-----!!".format(str(err)) + colorama.Style.RESET_ALL)
            log_file_data.append("!!-----Citation type unknown:{0}, defaulting as MISC-----!!\n".format(str(err)))
            self.cit_allowed_list = self.cit_dict['misc']
            self.citation_type = 'misc'

        #Pattern to search for camp attribute value(title, author etc.)
        self.cit_attribute_pattern = regex.compile(r"^[\w \s]*\w+",regex.IGNORECASE)

        #Creates dictionary using allowed item types as keys and the respective camp value in the citation data
        self.attribute_data_dict = {
            type:([self.gen_regex_pattern(type).match(x).captures()[0] for x in self.cit_data if self.gen_regex_pattern(type).match(x)]) for type in self.cit_allowed_list}
        
        #Populate removed camps list
        for line in cit_data:
            if (bool(self.cit_attribute_pattern.match(line)) and (self.cit_attribute_pattern.match(line).captures()[0].lower().strip() not in self.cit_allowed_list)):
                self.removed_camps.append(line)
                print(colorama.Fore.GREEN+"-removed {0} from {1}".format(line.strip(),self.label_name) + colorama.Style.RESET_ALL)
                log_file_data.append("-removed {0} from {1}\n".format(line.strip(),self.label_name))

    def gen_regex_pattern(self,cit_type):
        """ Generates regex string with the type passed to the function to search for text inside  brtackets from cit_type={} in each citation camp"""

        #Strings to generate regex to to search for citation camp data value value. Matches everything after {camp}= and before ,} or '',
        #Note:regex_gen not working yet with comments after the block terminator
        self.regex_gen_part1 = r'((( |\t)*'
        self.regex_gen_part2 = r')[ =]+)[{"]\K.+(?=((}|")(,|\n)$))'
        return regex.compile("{0}{1}{2}".format(self.regex_gen_part1,cit_type,self.regex_gen_part2),self.REGEX_FLAGS)



    
class PreambleData(GenericTex):
    
    def __init__(self, received_data):
        return super().__init__(received_data)

