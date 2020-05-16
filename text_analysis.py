from flask import Flask, jsonify, make_response, abort, request, render_template
from textblob import TextBlob, Word
import random
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm", parser=False, entity=False)

@app.route('/')
def home():
	return render_template('text-analysis.html')

@app.route('/analyse', methods=['GET','POST'])
def analyse():
	if request.method == 'GET':
		pass
	if request.method == 'POST':
		post = request.form['document']
		mid = request.form.get('mid')
		doc = nlp(post)
		if mid == '1':
			print("parts-of-speech tagging for whole document")
			pos_list = []
			for token in doc:
				out = token.text,token.pos_
				pos_list.append(out)
			output1 = "POS tags: ",pos_list
		elif mid == '2':
			print("lemmatization")
			lemma_list = []
			for lemma in doc:
				out = lemma.text, lemma.lemma_
				lemma_list.append(out)
			output1 = "Lemmatized text: ",lemma_list
		elif mid == '3':
			print("tokenization")
			token_list = []
			for token in doc:
				token_list.append(token.text)
			print(token_list)
			output1 = "Tokenized text: ",token_list
		elif mid == '4':
			print("named entity recognition")
			ner_list = []
			for ent in doc.ents:
				out = ent.text,ent.label_
				ner_list.append(out)
			output1 = "Named entity: ",ner_list
		elif mid == '5':
			print("sentiment analysis")
			blob = TextBlob(post)
			output1 = blob.sentiment.polarity
		else:
			print("nothing works")
		word_count = "word count: ",sum(len(line.split()) for line in post)
	return render_template('text-analysis.html',output=output1, word_count=word_count)
	


if __name__ == '__main__':
	app.run(debug = True)


'''
Text: The original word text.
Lemma: The base form of the word.
POS: The simple part-of-speech tag.
Tag: The detailed part-of-speech tag.
Dep: Syntactic dependency, i.e. the relation between tokens.
Shape: The word shape – capitalization, punctuation, digits.
is alpha: Is the token an alpha character?
is stop: Is the token part of a stop list, i.e. the most common words of the language?

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

'''

'''
Named entity recognition
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
'''