import pandas as pd
from unidecode import unidecode
from flask import Flask, render_template, request
from youtube_search import YoutubeSearch


df = pd.read_csv('html/ragas.csv')

app = Flask(__name__)


@app.route('/')
def student():
    return render_template('webapp.html')

@app.route('/byscale')
def next():
    return render_template("byscale.html")

@app.route('/byname')
def haha():
    return render_template("byname.html")


@app.route('/result_scale', methods=['POST', 'GET'])
def getraga():
    result = ""
    if request.method == 'POST':
        ascending = request.form["fname"].upper()
        descending = request.form["lname"].upper()
        listr = df[(df['Ascending Scale(ārohanam)'].str.lower() == ascending.lower()) & (df['Descending Scale(Avarohanam)'].str.lower() == descending.lower())]["Raga Name"].tolist()
        if len(listr) <= 1:
            result = "".join(df[(df['Ascending Scale(ārohanam)'].str.lower() == ascending.lower()) & (df['Descending Scale(Avarohanam)'].str.lower() == descending.lower())]["Raga Name"].tolist())
        else:
            for item in listr:
                result = result + "" + item + ", "
        if result != "":
            prelink = YoutubeSearch(listr[0], max_results=3).to_dict()
            link1 = "https://www.youtube.com/embed/"+prelink[0]["id"]
            link2 = "https://www.youtube.com/embed/"+prelink[1]["id"]
            link3 = "https://www.youtube.com/embed/"+prelink[2]["id"]
            return render_template("result.html", result="Ragam: "+''.join([i for i in result if not i.isdigit()]), ascending=ascending, descending=descending, link1=link1, link2=link2, link3=link3)
        else:
            return "<h1>No match found!</h1>"

@app.route('/result_ragam', methods=['POST', 'GET'])
def getscale():
    if request.method == 'POST':
        raganame = request.form["fname"]
        matches = []

        for item in df["Raga Name"]:
            if raganame == unidecode(item) or raganame == item:
                matches.append(item)

        if len(matches) > 0:
            ragam = "Ragam: " + matches[0]
            ascending = ' '.join(df[df["Raga Name"] == matches[0]]['Ascending Scale(ārohanam)'].tolist())
            descending = ' '.join(df[df["Raga Name"] == matches[0]]['Descending Scale(Avarohanam)'].tolist())
            return render_template("result1.html", result=ragam, ascending=ascending, descending=descending)
        else:
            return "<h1>No match found!</h1>"
    else:
        return "<h1>L</h1>"


if __name__ == "__main__":
    app.debug = True
    app.run()
