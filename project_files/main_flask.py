"""
Program creates structure to local website using Flask framework.
"""

__author__ = "Lisa Hu"
__version__ = 1.0

import os
from flask import Flask, render_template, request
from werkzeug import exceptions
from modules import FastaRead, DataModel

app = Flask(__name__)

# removing all the files in the temp folder
filelist = [file_ for file_ in os.listdir("temp")]
for file_ in filelist:
    os.remove(os.path.join("temp", file_))

app.config["upload_folder"] = "temp"


@app.route("/")
def render_home():
    """
    home page
    :return: main template
    """
    return render_template("main_template.html")


@app.route("/background")
def render_background():
    """
    informatioan about FASTA files
    :return: jinja template
    """
    return render_template("background_info.html")


@app.route("/import")
def render_import():
    """
    file importing
    :return: jinja template
    """
    return render_template("import.html")


def allowed_file(filename):
    """
    checks extension of file if it's fasta
    :param filename: name of the file
    :return:boolean
    """
    allowed_extensions = ["fasta", "fna", "ffn", "faa", "frn"]
    extension = filename.rsplit(".")[1]
    if extension in allowed_extensions:
        return True
    return False


@app.route("/upload", methods=["POST"])
def handle_form():
    """
    catch the file import, saving it
    :return: jinja template with the filename and the header(s) of the file
    :return: if the file is not a fasta file it'll return an error page
    """
    count = 0
    catch_header = {}
    file_ = request.files["filename"]  # get file input
    fname = file_.filename  # get filename
    if allowed_file(fname):  # check if file is fasta file
        file_.save(os.path.join(app.config["upload_folder"], fname))
        save_file = f"{app.config['upload_folder']}/{fname}"
        headers = FastaRead(save_file, None).get_headers()  # file input and responses give headers

        for header in headers:
            catch_header[header] = {}
            count += 1
            catch_header[header]["id"] = f"header{count}"
        return render_template("fasta_option.html", filename=fname, headers=catch_header)
    return render_template("error403.html")


@app.route("/results", methods=["POST"])
def show_results():
    """
    catch the options given for the file, which header(s) and data to show
    :return: jinja template with the results
    :return: if there were no options given on the previous page it'll show an error page
    :return: error page if the given file is a protein sequence instead of nucleotides
    """
    # setting variables
    data_res = {"percentage": False, "aa_count": False, "protein": False}
    res_headers = []
    reading_frame = None

    # get file from "saved_files"
    file_ = f"{app.config['upload_folder']}/{request.form['filename']}"

    # check if there was data returned, error page if no checkboxes were filled
    if "on" not in request.form.values():
        return render_template("error400.html")

    # going through form
    for response in request.form:
        # get the reading frame
        if response == "reading_frame":
            reading_frame = request.form["reading_frame"]
        # get the selected headers
        if response.startswith(">"):
            res_headers.append(response)
        # get selected data
        else:
            for i in data_res:
                try:
                    data_checkbox = request.form[i]
                    data_res[i] = True  # setting response to True if checkbox checked
                except exceptions.BadRequestKeyError:  # error if checkbox not checked
                    pass

    if not res_headers:  # user needs to check at least one header
        return render_template("error400.html")

    try:
        # results = [{header:"results of fasta1"}, {header:"results of fasta2"}, etc]
        results = FastaRead(file_, reading_frame).get_results()
    except FileNotFoundError:
        return render_template("error500.html")

    if results is None:  # if the file is a protein sequence, error page
        return render_template("protein_fasta_page.html")

    # setting variables
    pie_charts = []
    bar_charts = []
    pro_seqs = []
    final = {}
    count = 0

    for header in results:  # loop through the headers of all the results
        if header in res_headers:  # check if header was asked
            final[header] = {}
            count += 1
            result = results[header]  # result is only set if header was asked
            for key in result:  # for each data in result

                datamodel = DataModel(key, result[key])  # call class
                if key == "percentage":
                    if data_res["percentage"]:  # check if data response was asked
                        if datamodel.pie_plot() not in pie_charts:  # check if it already exists
                            pie_charts.append(datamodel.pie_plot())
                            final[header]["pie"] = datamodel.pie_plot()
                    else:  # set the variable to None if the data was not asked
                        final[header]["pie"] = None

                # repetitive code for 2 other data responses
                elif key == "aa_count":
                    if data_res["aa_count"]:
                        if datamodel.bar_plot() not in bar_charts:
                            bar_charts.append(datamodel.bar_plot())
                            final[header]["bar"] = datamodel.bar_plot()
                    else:
                        final[header]["bar"] = None

                else:
                    if data_res["protein"]:
                        if result["protein"] not in pro_seqs:
                            pro_seqs.append(result["protein"])
                            final[header]["protein"] = result["protein"]
                    else:
                        final[header]["protein"] = None
                final[header]["id"] = str(count)

    return render_template("result_page.html", headers=final)


if __name__ == "__main__":
    app.run()
