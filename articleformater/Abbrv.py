#Abreviates serial titles

#Imports pickle 
import pickle
import requests
import json


def generate_pickle(abbrv_data):
    """
    Generates and serializes a dictionary object containing abbreviation data
    """
  
    #open text file containing alph sorted serial titles
    with open(abbrv_data,errors='ignore') as f:
        data = f.readlines()
    
    #dictionary with data
    data_dict = {}

    #separates entries in text file by '=' char to populate dictionary
    for line in data:
        split = (line.rstrip("\r\n")).split('=')
        head = split[0].rstrip()
        tail = split[1].lstrip()

        data_dict[head] = tail

    #output location
    output_file = open("pickle.obj","wb")

    #Generates pickle and dumps
    pickle.dump(data_dict,output_file,-1)


class abbrv:
    '''
        Abreviates single string. Needs to be initialized with a pickle object
    '''


    def __init__(self, pickle_location = "pickle.obj"):
        with open(pickle_location,'rb') as p:
            self.data_dict:dict = pickle.load(p)

    def abbreviate(self,input_text):
        """
            Abreviates inputed text
        """

        if input_text in self.data_dict:
            return self.data_dict[input_text]
        else:
            #Abreviates using AbbrevIso app(see github)
            passada = input_text.replace(" ","_")
            r = requests.get("http://criolipolisepirassununga.com.br:21103/?{0}".format(passada))
            return r.text


    def isAbbrv(self,input_text):
        """Tests if string is abbreviated"""
        counter = 0
        for char in input_text:
            if char == '.':
                counter = 1 + counter
            if counter == 2:
                return True

        return False

                




