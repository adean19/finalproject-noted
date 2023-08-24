from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from textblob import TextBlob
from models import db, User, Entries
from forms import JournalEntry_form, LoginForm, SignUpForm
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://hhnzfbip:c16ZfCswT0fsQJWsElHXc0JbcciraJdS@bubble.db.elephantsql.com/hhnzfbip"
app.config.from_object(Config)

#login manager for flask login
login_manager = LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)

#Routes

#Homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    form = JournalEntry_form()
    if request.method == "POST":
        #If form data is present
        if form.validate():
            #assign the subject input by the user to the subject variable
            subject = form.subject.data
            print(subject)
            #assign the body input by the user to the body variable
            body = form.body.data
            print(body)
            #Setting up adding the journal entry to the db for the current_user
            entry_info = Entries(current_user.id, subject, body)
            print(entry_info)
            #Add the userentry data to the db
            db.session.add(entry_info)
            db.session.commit()
            # Return confirm msg and redirect
            flash(f'Successfully added your entry.')
            return redirect(url_for('index'))
    entries = Entries.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', title='Noted', form=form, entries = entries)

#delete journal entry
@app.route('/delete_entry/<int:id>', methods=['POST'])
def delete_entry(id):
    entry = Entries.query.get_or_404(id)
    
    # Delete the entry from the database
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('index'))

#Signup Page
@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            #add user to the database
            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()
            flash('Successfully created user.', 'Success')
            return redirect(url_for('login'))
        flash('An error has occured. Please submit a valid form', 'danger')
    return render_template('signup.html', form = form)

#Login Page
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            #find user from db
            user = User.query.filter_by(username=username).first()

            if user:
                if user.password == password:
                    login_user(user)
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect username/password', 'danger')
            else:
                flash('Incorrect username.', 'danger')
        else:
            flash('An error has occurred. Please submit a valid form', 'danger')
    
    return render_template('login.html', form=form)

#logout Page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Analyze button
@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        content = request.form.get('body')

        # Analyze sentiment using TextBlob
        sentiment = analyze_sentiment(content)

        # Return the sentiment analysis result
        return jsonify({'sentiment': sentiment})

def analyze_sentiment(content):
    # Use TextBlob for sentiment analysis
    analysis = TextBlob(content)
    polarity = analysis.sentiment.polarity

    # Determine sentiment based on polarity
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment, polarity

if __name__ == '__main__':
    app.run(debug=True)
