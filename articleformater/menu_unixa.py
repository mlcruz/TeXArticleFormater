#!/usr/bin/python3.6
import click
from Abbrv import abbrv
import TeXanalyser
from TeXanalyser import Article
@click.command()
@click.option('--tex_path',prompt='Path to tex file', help='Path to tex file')
@click.option('--bib_path',prompt='Path to bib file', help='Path to bib file')
@click.option('--tex_output_name',default="default",help='Output tex file path. Defaults to file.tex.new in the same folder')
@click.option('--bib_output_name',default="default",help='Output bib file path. Defaults to file.bib.new in the same folder')
@click.option('--remove_uncited',default="n",help='y/n Removes unused bibliography entries. Default: n')
@click.option('--log_file_path',default="default",help='Output .log file path. Defaults to file.log in the same folder')
@click.option('--comment_removed',default="n",help='y/n Comments removed fields from bib data. default: n')
@click.option('--terminator',default="N/A",help="String to fill missing entries with. Defaults to N/A")
@click.option('--abbreviate',default="n",help="Y/N Abbreviate serial titles?. Defaults to N")
@click.option('--format_file',default="y",help="Y/N Format file?. Defaults to Y")


def console_wrapper(bib_path,tex_path,tex_output_name,bib_output_name,remove_uncited,log_file_path,comment_removed,terminator,abbreviate,format_file):
	if abbreviate == ("y" or "yes" or "YES" or "Y"):
		abreviador = abbrv("/home/mlcruz/mysite/TeXArticleFormater/articleformater/pickle.obj")
	else:
		abreviador = 0

	dados = Article(tex_path,bib_path,abreviador)
<<<<<<< HEAD


	if format_file == ("y" or "yes" or "YES" or "Y"):
		dados.init_bib()

=======
	
	
	if format_file == ("y" or "yes" or "YES" or "Y"):
		dados.init_bib()
	
>>>>>>> 299d4318fb9befdf38ef872536836e93f6844d24
		if remove_uncited == ("y" or "yes" or "YES" or "Y"):
			dados.bib_data.cite_block_library = dados.bib_data.cull_useless(dados.tex_data.cited_list)

		if comment_removed == ("y" or "yes" or "YES" or "Y"):
			dados.current_bib_data = dados.bib_data.generate_writable_bib_object(terminator,1)
		else:
			dados.current_bib_data = dados.bib_data.generate_writable_bib_object(terminator,0)
<<<<<<< HEAD

	if(format_file == "n" and  (abreviador != 0) ) :
		dados.current_bib_data = Article.abbreviate_list(dados.current_bib_data,['journal'])


=======
	elif( (format_file == ("n" or "no" or "NO" or "N")) and  abreviador != 0) :
		dados.current_bib_data = Article.abbreviate_list(dados.current_bib_data,['article'])
		
	
>>>>>>> 299d4318fb9befdf38ef872536836e93f6844d24
	if tex_output_name == "default":
		dados.write_tex()

	else:
		dados.tex_file_location = tex_output_name
		dados.write_tex(1)

	if bib_output_name == "default":
		dados.write_bib()
	else:
		dados.bib_file_location = bib_output_name
		dados.write_bib(1)

	if log_file_path == "default":
		dados.write_log()
	else:
		dados.log_file_location = log_file_path
		dados.write_log(1)

if __name__ == '__main__':
    console_wrapper()
