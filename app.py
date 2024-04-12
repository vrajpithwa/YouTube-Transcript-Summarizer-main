from flask import Flask, redirect, render_template,request,redirect, url_for
import flask
import subprocess
import time
from youtube_transcript_api import YouTubeTranscriptApi
import nltk
import re
from nltk.corpus import stopwords
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np 
from gtts import gTTS
import pyttsx3
import os
import boto3

nltk.download('punkt')

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id) # Use a different index to select a different voice
# engine.setProperty('rate', 120) # Set the rate of speech
# engine.say(text)
# engine.runAndWait()


app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def summarize():
    if request.method == "POST":
        print(request.form['input'])
        global link
        link = request.form['input']
       
    
    return render_template("main.html")

        
@app.route("/new", methods=['GET', 'POST'])
def show():
    if request.method == "POST":
        link = request.form['input']
        unique_id = link.split("=")[-1]
        #unique_id = '0I3WXCKfpEQ'
        sub = YouTubeTranscriptApi.get_transcript(unique_id)  #,languages=['en-IN']
        #transcript = sub.find_transcript(['de', 'en','en-IN'])
        subtitle = " ".join([x['text'] for x in sub])
        #print(subtitle)
        
        from nltk.tokenize import sent_tokenize
        #subtitle = subtitle.replace("n","")
        sentences = sent_tokenize(subtitle)

        organized_sent = {k:v for v,k in enumerate(sentences)}
        tf_idf = TfidfVectorizer(min_df = 1, 
                                            strip_accents='unicode',
                                            max_features= 5,
                                            lowercase = True,
                                            token_pattern=r'w{1,}',
                                            ngram_range=(0, 3), 
                                            use_idf=1,
                                            smooth_idf=1,
                                            sublinear_tf=1,
                                            stop_words = 'english')

        sentence_vectors = tf_idf.fit_transform(sentences)
        sent_scores = np.array(sentence_vectors.sum(axis=1)).ravel()
        N = 5
        top_n_sentences = [sentences[index] for index in np.argsort(sent_scores, axis=0)[::-1][:N]]

        # mapping the scored sentences with their indexes as in the subtitle
        mapped_sentences = [(sentence,organized_sent[sentence]) for sentence in top_n_sentences]
        # Ordering the top-n sentences in their original order
        mapped_sentences = sorted(mapped_sentences, key = lambda x: x[1])
        ordered_sentences = [element[0] for element in mapped_sentences]
        # joining the ordered sentence
        global summary
        summary = " ".join(ordered_sentences)
        
        print(summary)

        # Convert the summarized text into speech and save it as an mp3 file
        # tts = gTTS(text=summary, lang='en')
        # tts.save("../summary.mp3")
        # Play the mp3 file
        # subprocess.call(["afplay", "summary.mp3"])
        # os.system("start summary.mp3")
        return render_template("summary.html", summary = summary)
    return render_template("summary.html")
        # return render_template("summary.html", summary = summary)

# @app.route("/speak", methods=["GET","POST"])
# def speak():
#     if request.method == "POST":
#         engine = pyttsx3.init()
#         voices = engine.getProperty('voices')
#         engine.setProperty('voice', voices[1].id) # Use a different index to select a different voice
#         engine.setProperty('rate', 120) # Set the rate of speech
#         engine.say(summary)
#         engine.startLoop()
#         engine.save_to_file("../1234567.mp3")
#         return "Speech Generated"    
        

@app.route("/explore", methods=['GET', 'POST'])
def new():
    return render_template("about.html")
if __name__ == '__main__':
   app.run(debug=True)


   