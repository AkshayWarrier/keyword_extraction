from flask import Flask, render_template, request, jsonify
from keybert import KeyBERT


app = Flask(__name__)


kw_model = KeyBERT()

def get_keywords(text):
    return kw_model.extract_keywords(text)

@app.route('/', methods=["POST","GET"])
def home():
    if request.method == "POST":
        formatted = "The keywords are: "
        for i in get_keywords(request.form['text']):
            formatted += i[0] + ", "
        return render_template('index.html',keywords= formatted)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)