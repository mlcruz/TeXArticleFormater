import os
import secrets
from flask import Flask, request, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
import subprocess
import Abbrv


UPLOAD_FOLDER = '/home/mlcruz/mysite/uploads'
DOWNLOAD_FOLDER ='/home/mlcruz/mysite/downloads'
ALLOWED_EXTENSIONS = set(['tex', 'bib'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route('/download/<filename>')
def download_file(filename):
       return send_from_directory('/home/mlcruz/mysite/downloads',filename = "new_"+filename, attachment_filename=("new_"+filename),as_attachment=True)




@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if request.form.get('uncited'):
            checked_uncited = 'y'
        else:
            checked_uncited = 'n'
        if request.form.get('abbreviate'):
            checked_abbreviate = 'y'
        else:
            checked_abbreviate = 'n'
        # check if the post request has the file part
        if ('file_tex' or 'file_bib') not in request.files:
            return redirect(request.url)
        file_tex  = request.files['file_tex']
        file_bib = request.files['file_bib']
        # if user does not select file, browser also
        # submit a empty part without filename
        if (file_tex.filename or file_bib.filename) == '':
            return redirect(request.url)
        if (file_tex and file_bib) and allowed_file(file_tex.filename) and allowed_file(file_bib.filename):
            filename_tex = secure_filename(file_tex.filename)
            filename_bib = secure_filename(file_bib.filename)
            salt = "" #secrets.randbelow(99999999)

            tex_path_string = os.path.join(app.config['UPLOAD_FOLDER'], filename_tex)
            bib_path_string = os.path.join(app.config['UPLOAD_FOLDER'], filename_bib)

            tex_out_string = os.path.join(DOWNLOAD_FOLDER, (str(salt) + "new_" + filename_tex ))
            bib_out_string = os.path.join(DOWNLOAD_FOLDER, (str(salt) + "new_" + filename_bib))

            log_out_string = tex_out_string + ".log"

            file_tex.save(tex_path_string)
            file_bib.save(bib_path_string)

            script_path = os.path.join(os.getcwd(),"mysite/TeXArticleFormater/articleformater/menu_unixa.py")
            command_string = ["{0}".format(script_path),
            "--tex_path",tex_path_string,
            "--bib_path",bib_path_string,
            "--tex_output_name",tex_out_string,
            "--bib_output_name",bib_out_string,
            "--log_file_path",log_out_string,
            "--remove_uncited",checked_uncited,
	    "--abbreviate",checked_abbreviate,
            ]



            #mysite/TeXArticleFormater/articleformater/menu_unix.py --tex_path "mysite/TeXArticleFormater/articleformater/comite.tex" --bib_path "mysite/TeXArticleFormater/articleformater/comite.bib" --tex_output
#_name "mysite/uploads/new.tex" --bib_output_name "mysite/uploads/new.bib" --log_file_path "mysite/uploads/new.log"

            subprocess.run(command_string)  # doesn't capture output

            log_stringer = ""
            log_file = None
            try:
                with open(log_out_string,"r",encoding="utf8") as tex_reader:
                    log_file = tex_reader.readlines()

                for line in log_file:
                    log_stringer = log_stringer + line +"<br>"

            except:
                log_stringer = "Error: Subprocess exited with error. Probably some weird character or unbalanced brackets in the bibliography is messing things up"



        #send_from_directory('/home/mlcruz/mysite/downloads',filename = "new_"+filename_bib , attachment_filename=("new_"+filename_bib),as_attachment=True)

            return ('''
        <!doctype html>
        <title>Download files</title>
        <h3>Done!</h3><br>
        <h2>Download Formated Files:</h2><br>
        <a target="_blank" href={0}><input type="button" value="Download TeX file"/></a>
        <a target="_blank" href={1}><input type="button" value="Download Bib file"/></a>
        <a target="_blank" href={2}><input type="button" value="Download Log file"/></a>
        {3}
	<br>
        <br>
        <h2>LOG:</h2>
        </form>'''.format(request.url+"download/{0}".format(filename_tex),request.url+"download/{0}".format(filename_bib),request.url+"download/{0}".format(filename_tex+".log"),command_string) + log_stringer)


    return '''
    <!doctype html>
    <title>Select tex and bib files</title>
    <h1>Select tex and bib files to be formated</h1>
    <form method=post enctype=multipart/form-data>
      <p>tex: <input type=file name=file_tex><br>
         bib: <input type=file name=file_bib><br><br>
        <input type="checkbox" name="uncited" value="true"> Remove unused bibliography entries<br>
	<input type="checkbox" name="abbreviate" value="true"> Abreviate serial titles<br>
         <br><br><input type=submit value=Format>
    </form><br><br><br><br><br><br><br><br><br><br><br><br><br><a href="https://github.com/mlcruz/TeXArticleFormater">Project page @ github</a>'''



@app.route('/abbrv', methods=['GET', 'POST'])
def abreviate():
    if request.method == 'POST':
        abbreviator = Abbrv.abbrv("/home/mlcruz/mysite/TeXArticleFormater/articleformater/pickle.obj")
        abreviado = abbreviator.abbreviate(request.form['abbreviate'])
        return '''
        <!doctype html>
        <title>Abbreviate</title>
        <h1>Abbreviate</h1>
        <form method=post enctype=multipart/form-data>
            Serial title: <input type=text name=abbreviate><br><br>
            Abbreviated title:<textarea disabled>{0}</textarea>
            <br><br><input type=submit value=Abbreviate>
        </form>'''.format(abreviado)

    return '''
    <!doctype html>
    <title>Abbreviate</title>
    <h1>Abbreviate</h1>
    <form method=post enctype=multipart/form-data>
         Serial title: <input type=text name=abbreviate disable><br><br>
         Abbreviated title: <textarea disabled></textarea>
         <br><br><input type=submit value=Abbreviate>
    </form>'''
