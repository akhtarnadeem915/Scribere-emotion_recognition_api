from flask import Flask, jsonify, make_response, abort, request, render_template
import random
from deploy import prediction
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def home():
	return render_template('blogging.html')

@app.route('/analyse', methods=['GET','POST'])
def analyse():
	if request.method == 'GET':
		pass
	if request.method == 'POST':
		post = request.form['document']
		mid = request.form.get('mid')
		doc = nlp(post)
		heading = ""
		output1 = ""
		text_class = ""
		if mid == '1':
			print("Metadata Extraction")
			pos_list = []
			for token in doc:
				out = token.text,token.pos_
				pos_list.append(out)
			output1 = pos_list
		elif mid == '2':
			print("Heading Generation")
			pos_list = []
			for token in doc:
				out = token.text,token.pos_
				pos_list.append(out)
			heading = pos_list
		elif mid == '3':
			print("Text Classification")
			output = prediction(post)
			text_class = output
		elif mid == '4':
			print("Auto hashtag generation")
			pos_list = []
			for token in doc:
				out = token.text,token.pos_
				pos_list.append(out)
			heading = pos_list
		else:
			print("nothing works")
	return render_template('blogging.html',post=post,output=output1,heading=heading,text_class=text_class)
	


if __name__ == '__main__':
	app.run(debug = True)
