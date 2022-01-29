Author: Lisa Hu
Date: 01-04-2021
Version: 1.0

Theme03: Creating Flask Website

Description
This theme is focussed on creating our own website using the web application framework Flask.
Flask was formerly used as a simple wrapper for Werkzeug and Jinja,
but has become one of the most popular Python web frameworks.

For Bio-informatics, it is common to use files filled with information about
the molecular biology in organisms. To read such files is very complicated to do by hand.
To make it easier to read, we can build a website that reads a file and
gives the user the wanted data. This website is build to specifically read FASTA formatted files.

Installation
1. Open the directory in PyCharm as a new project
2. Go to "File" > "Settings" or press Ctrl + Alt + S
3. Open the project tab and click on Python Interpreter
4. From here you can configure the project's download packages by clicking the "+" icon
   Please add the following packages: Flask, Jinja2, matplotlib, numpy
5. To run the site on a local host, open the PyCharm terminal and run the following commands:
   set FLASK_APP=main_flask.py
   python -m flask run
   The terminal should show a clickable link which will open a browser tab.

Contents
main_flask.py		Python code for web framework
modules.py			Modules used in web environment
poster.pdf			Poster flash
static (folder)		Stylesheet (CSS file) and images (folder) for website
templates (folder)	HTML files written with Jinja templating
temp (folder)		Temporary folder where the uploaded files are temporarily saved 

Usage
To make use of the FASTA reader, navigate to the "Import FASTA file" tab in the "Content Menu".
This will open the page where you can send a FASTA file. The next page shows the headers
of the FASTA files.

Support
If there are any problems with the project, please contact via e-mail: l.j.b.hu@st.hanze.nl

Lastly I want to thank Jasper Bosman for giving me new ideas and helping me out whenever I got stuck.