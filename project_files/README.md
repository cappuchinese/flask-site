# Theme03: Creating Flask Website

In this repository you will find code and instructions for the website made for Theme03.
The code is written in Python, using the Flask web application framework.
The HTML and CSS are written using Jinja templating and Bootstrap.
To set up the website, please follow the installation guide.

## Description
This theme is focussed on creating our own website using the web application framework Flask.
Flask was formerly used as a simple wrapper for Werkzeug and Jinja,
but has become one of the most popular Python web frameworks.

For Bio-informatics, it is common to use files filled with information about
the molecular biology in organisms. To read such files is very complicated to do by hand.
To make it easier to read, we can build a website that reads a file and
gives the user the wanted data. This website is build to specifically read FASTA formatted files.

## Installation guide
1. Open the directory in **PyCharm** as a new project
2. Go to **"File" > "Settings"** or press `Ctrl + Alt + S`
3. Open the project tab and click on Python Interpreter
4. From here you can configure the project's download packages by clicking the `+` icon
   Please add the following packages: `Flask`, `Jinja2`, `matplotlib`
5. To run the site on a local host, open the **PyCharm terminal** and run the following commands:<br>
   ```set FLASK_APP=main_flask.py```<br>
   ```python -m flask run```<br>
   The terminal should show a clickable [<u>link</u>]() which will open a browser tab.

## Contents
<table>
<tr><th>File</th><th>Information</th></tr>
<tr><td>main_flask.py</td><td>Python code for web framework</td></tr>
<tr><td>modules.py</td><td>Modules used in web environment</td></tr>
<tr><td>poster.pdf</td><td>Poster flash</td></tr>
<tr><td>static (folder)</td><td>Stylesheet (CSS file) and images (folder) for website</td></tr>
<tr><td>templates (folder)</td><td>HTML files written with Jinja templating</td></tr>
<tr><td>temp (folder)</td><td>Temporary folder where the uploaded files are temporarily saved</td></tr>
</table>

## Credits
### Contributors
- Lisa Hu ([l.j.b.hu@st.hanze.nl](<mailto:l.j.b.hu@st.hanze.nl>))

### Tools
  From the [Pallets Projects](https://palletsprojects.com/):
- [GitHub](https://github.com/pallets)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/)
- [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)

Other libraries:
- [matplotlib](https://matplotlib.org/)

### Organizations
- University of Applied Sciences Hanzehogeschool Groningen <br>
  ![](https://www.hanze.nl/Style%20Library/hanze/img/logo-black-wordmark.svg)
