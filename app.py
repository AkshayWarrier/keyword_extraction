from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


app = Flask(__name__)

n_gram_range = (1, 1)
stop_words = "english"
model = SentenceTransformer('distilbert-base-nli-mean-tokens')


def get_keywords(doc,top_n = 5):
    count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([doc])
    candidates = count.get_feature_names()
    doc_embedding = model.encode([doc])
    candidate_embeddings = model.encode(candidates)
    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
    return keywords

@app.route('/', methods=["POST","GET"])
def home():
    if request.method == "POST":
        formatted = "The keywords are: "
        for i in get_keywords(request.form['text']):
            formatted += i + ", "
        return render_template('index.html',keywords= formatted)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)