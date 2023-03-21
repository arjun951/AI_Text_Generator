from flask import Flask, render_template, request, send_file
from bs4 import BeautifulSoup
import requests
import nltk
from fpdf import FPDF

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result", methods = ['POST','GET'])
def result():
    output = request.form.to_dict()
    link = output["name1"]
    keyword = output["name2"]

    response = requests.get(link)
    html_data = response.text
    parsed_data = BeautifulSoup(html_data, 'html.parser')

    li = parsed_data.find_all('p')
    list1 = []

    for i in li:
        list1.append(i.text)

    final_list = []

    for i in list1:
        sentences = nltk.sent_tokenize(i)
        for j in sentences:
            words = nltk.word_tokenize(j)
            if keyword in words:
                final_list.append(i)

    temp = []
    for i in final_list:
        t = i.strip()
        temp.append(t)

    res = [*set(temp)]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)
    for i in res:
        j = i.encode('latin-1', 'replace').decode('latin-1')
        pdf.write(4, j + "\n\n")


    file = open("number.txt",mode='r')
    file_name = file.read()
    file_name+='.pdf'

    pdf.output(file_name)

    return send_file(file_name, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
