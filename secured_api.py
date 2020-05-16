#libraries
from flask import Flask, jsonify, make_response, abort, request, render_template, current_app, redirect
#from deploy import prediction
from datetime import timedelta
import jwt
import datetime
from functools import wraps,update_wrapper

#app instance
app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

#ml libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
#pickles
vect = joblib.load('vectorizer.pkl')
clf = joblib.load('svm_emotoion_text.pkl')
dict_emotion = {'Neutral':0,'Disapproval':1,'Optimism':2,'Joy':3,'Anticipation':4,'Anger':5,'Fear':6,'Sadness':7,'Surprise':8,'Ambiguous':9,'Contempt':10,'Submission':11,'Love':12,'Remorse':13,'Aggression':14,'Disgust':15,'Trust':16,'Awe':17}

# function to return key for any value
def get_key(val):
    for key, value in dict_emotion.items():
         if val == value:
             return key

    return "key doesn't exist"

optimism = "Optimism"
submission = "Submission"
awe = "Awe"
disapproval = "Disapproval"
remorse = "Remorse"
contempt = "Contempt"
aggresiveness = "Aggresiveness"

def prediction(inp):
    input_data = [inp]
    x_input = vect.transform(input_data)
    y_pred = clf.predict(x_input)
    print("predicted: ",y_pred)
    y_pred = get_key(y_pred)
    emotion = y_pred
    if optimism in emotion:
        return "Anticipation + Joy = Optimism"
    elif submission in emotion:
        return "Trust + Fear = Submission"
    elif awe in emotion:
        return "Fear + Surprise = Awe"
    elif disapproval in emotion:
        return "Surprise + Sadness = Disapproval"
    elif remorse in emotion:
        return "Sadness + Disgust = Remorse"
    elif contempt in emotion:
        return "Disgust + Anger = Contempt"
    elif aggresiveness in emotion:
        return "Anger + Anticipation = Aggressiveness"
    else:
        return y_pred



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'token is invalid'}), 403

        return f(*args, **kwargs)
    return decorated

#cryptographic key generated via fernet
'''
What is a fernet key?¶
A fernet key is used to encrypt and decrypt fernet tokens. 
Each key is actually composed of two smaller keys: a 128-bit AES encryption key and 
a 128-bit SHA256 HMAC signing key. 
The keys are held in a key repository that keystone passes to a library 
that handles the encryption and decryption of tokens.'''
app.config['SECRET_KEY'] = 'RNa3Rhodhf-l5g1PFt5DAOnJnmkLH2RQOMxvdVkvVac='

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message':'this is only available for people with valid tokens'})

@app.route('/login')
def login():
    auth = request.authorization

    #if auth and auth.password == 'password':
    if auth and auth.username == 'nadeem' and auth.password == 'password_123':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100)}, app.config['SECRET_KEY'])
        key = token.decode('UTF-8')
        print("key",key)
        return jsonify({'key':token.decode('UTF-8')})
        #return '<html><body><h1>working</h1><br><a href="/logout">logout</a><br><a href="/protected?token=' + key + '">protected</a></body></html>'
    return make_response('Could not verify!', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})

@app.route('/logout')
def logout():
    return redirect('/')

#/emotion-text/api/v1.0/text=today?token=
@app.route('/emotion-text/api/v1.0/<string:text>', methods=['GET'])
@crossdomain(origin='*')
@token_required
def get_emotion(text):
    '''
    text = ['this is great','this is cool']
    text.reverse()
    text[0]
    '''
    output = prediction(text)
    return jsonify({'text':output})

'''
@app.route('/')
def home():
	return render_template('index.html')'''


"""
api - text input [post] | function call - json return

Make sure you use a salt (or even API key) that is given to your JS client 
on a session basis (a.o.t. hardcoded). 
"""

if __name__ == '__main__':
    app.run(debug=True)