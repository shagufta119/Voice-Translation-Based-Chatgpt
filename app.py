
import openai
from flask import Flask, app, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from googletrans import Translator, LANGUAGES
from flask import Flask, request,render_template, redirect,session
from flask import Flask, redirect, url_for
import bcrypt
from psycopg2 import IntegrityError
import pyttsx3


def get_all_languages():
    return LANGUAGES

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(1000))
    response_text = db.Column(db.String(10000))
    language = db.Column(db.String(10))
with app.app_context():
    db.create_all()

translator = Translator()

engine = pyttsx3.init()


openai.api_key = ""

app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    language_options = get_all_languages()

    hide = False
    response_text = None

    if request.method == "POST":
        user_input = request.form["user_input"]
        selected_language = request.form.get("language", "en")
        
        translated_user_input = translator.translate(user_input, dest=selected_language).text
        response_text = chatGPT(translated_user_input, selected_language)
        conversation = Conversation(user_input=translated_user_input, response_text=response_text, language=selected_language)
        db.session.add(conversation)
        db.session.commit()

        conversation_history = Conversation.query.all()
        hide = True

        return render_template("website.html", response=response_text, language_options=language_options, conversation_history=conversation_history, hide=hide)
    
    conversation_history = Conversation.query.all()

    return render_template("login.html", language_options=language_options, conversation_history=conversation_history, hide=hide)

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(name=name).first()

        if existing_user:
            return render_template('login.html', error='Username already exists. Please choose a different one.')

        try:
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/signin')
        except IntegrityError:
            db.session.rollback()
            return render_template('login.html', error='Email already exists. Please use a different email.')

    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    language_options = get_all_languages()

    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()

        if user and user.check_password(password):
            session['name'] = user.email

            selected_language = request.form.get("language", "en")
            response_text = chatGPT("", selected_language)  
            conversation = Conversation(user_input="", response_text=response_text, language=selected_language)
            db.session.add(conversation)
            db.session.commit()
            conversation_history = Conversation.query.all()
            return redirect(url_for('render_website',response=response_text,language_options=language_options,
                                    conversation_history=conversation_history))
        else:
            return render_template('login.html', error='Invalid user')
    return render_template('login.html', language_options=language_options)
   



@app.route('/website', methods=['GET'])
def render_website():
    language_options = get_all_languages()

    if 'name' in session:
        return render_template('website.html', language_options=language_options)
    else:
         return redirect(url_for('website'))
@app.route('/index')
def index():
    language_options = get_all_languages()
    return render_template('website.html', language_options=language_options)

@app.route("/delete_response/<int:response_id>", methods=["POST"])
def delete_response(response_id):
    response = Conversation.query.get(response_id)
    if response:
        db.session.delete(response)
        db.session.commit()
        return jsonify({"status": "success", "message": "Response deleted successfully"})
    else:
        return jsonify({"status": "error", "message": "Response not found"})


def chatGPT(user_input, target_language='en'):
    try:
        translated_user_input = translator.translate(user_input, dest=target_language).text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": translated_user_input}]
        )
        print("OpenAI Response:", response)
       
        response_content = response["choices"][0]["message"]["content"]
        translated_response = translator.translate(response_content, dest=target_language).text
        return translated_response

    except Exception as e:
        print(f"OpenAI API error: {str(e)}")
        return f"OpenAI API error: {str(e)}"
if __name__ == '__main__':
    app.run(debug=True)
