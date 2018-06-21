import TeXanalyser
from TeXanalyser import Article
import colorama
import easygui
import os


colorama.init()


used_options = {"file_input":"dialog","uncited":"no","save_name":"default(file_new.tex)","terminator":"N/A","log_name":"default(file.log)","comment_removed":"no"}
unused_options ={"file_input":"console", "uncited":"yes","save_name":"open save dialog","log_name":"open save dialog","comment_removed":"yes"}
restart = '0'

print(colorama.Fore.CYAN + colorama.Style.BRIGHT + "Options:\n")
print(colorama.Fore.GREEN + "1)File input: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["file_input"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["file_input"]))
print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "2)Remove uncited bibliography entries: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["uncited"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["uncited"]))
print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "3)New file name: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["save_name"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["save_name"]))
print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "4)Missing entry text: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["terminator"]))
print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "5)Log file name: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["log_name"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["log_name"]))
print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "6)Comment removed fields: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["comment_removed"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["comment_removed"]))

print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "\nEnter a number to change options or 0 to continue" + colorama.Style.RESET_ALL)


#i wish python had do-whiles..
user_input = input()
while (restart == '0'):
    while (user_input != "0"):
        if user_input == "1":
            (used_options["file_input"],unused_options["file_input"]) = (unused_options["file_input"],used_options["file_input"])
        elif user_input == "2":
            (used_options["uncited"],unused_options["uncited"]) = (unused_options["uncited"],used_options["uncited"])
        elif user_input == "3":
            (used_options["save_name"],unused_options["save_name"]) = (unused_options["save_name"],used_options["save_name"])
        elif user_input == "4":
            used_options["terminator"] = input("Enter new text: ")
        elif user_input == "5":
            (used_options["log_name"],unused_options["log_name"]) = (unused_options["log_name"],used_options["log_name"])
        elif user_input =="6":
            (used_options["comment_removed"],unused_options["comment_removed"]) = (unused_options["comment_removed"],used_options["comment_removed"])







        os.system('cls')
        print(colorama.Fore.CYAN + colorama.Style.BRIGHT + "Options:\n")
        print(colorama.Fore.GREEN + "1)file input: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["file_input"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["file_input"]))
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "2)Remove uncited bibliography entries: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["uncited"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["uncited"]))
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "3)New file name: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["save_name"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["save_name"]))
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "4)Missing entry text: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["terminator"]))
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "5)Log file name: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["log_name"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["log_name"]))
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "6)Comment removed fields: " + colorama.Fore.LIGHTYELLOW_EX + "{0}".format(used_options["comment_removed"]) + " / " + colorama.Style.DIM +colorama.Fore.LIGHTBLACK_EX + "{0}".format(unused_options["comment_removed"]))


        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "\nEnter a number to change options or 0 to continue" + colorama.Style.RESET_ALL)


        user_input = input()


    if used_options["file_input"] == "dialog":

        print("Select Tex and Bib files")
        dados = Article(easygui.fileopenbox("Select tex File",None,"*.tex"),easygui.fileopenbox("Select viv File",None,"*.bib"))
    else:
        dados = Article(input("tex file location: "),input("bib file location: "))

    if used_options["uncited"] == "yes":
        dados.bib_data.cite_block_library = dados.bib_data.cull_useless(dados.tex_data.cited_list)

    if used_options["comment_removed"] == "yes":
        dados.current_bib_data = dados.bib_data.generate_writable_bib_object(used_options["terminator"],1)
    else:
        dados.current_bib_data = dados.bib_data.generate_writable_bib_object(used_options["terminator"],0)

    if used_options["save_name"] == "default(file_new.tex)":
        dados.write_bib()
        dados.write_tex()
    else:
        dados.tex_file_location = easygui.filesavebox("new tex file name",None,(("{0}_{1}").format(((dados.tex_file_location).split(".")[0]).lower(),"new.tex")),r'*.tex')

        dados.bib_file_location = easygui.filesavebox("new bib file name",None,(("{0}_{1}").format(((dados.bib_file_location).split(".")[0]).lower(),"new.bib")),r'*.bib')

        dados.write_bib(1)
        dados.write_tex(1)

    print(colorama.Fore.RED + colorama.Style.BRIGHT + "Completed!\n")
    
    if used_options["log_name"] == "default(file.log)":
        dados.write_log()
    else:
        dados.log_file_location = easygui.filesavebox("New log file name",None,dados.log_file_location,r"*.log")
        dados.write_log(1)

  
    
    print(colorama.Fore.CYAN + "press 0 to restart\n")
    restart = input()
    user_input = ''
