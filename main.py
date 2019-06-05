from flask import Flask, render_template,request,redirect,logging,url_for,flash
from articlebag import Articles

from wtforms import Form, BooleanField, StringField, PasswordField, validators

from wtforms.validators import DataRequired,Required, Length, Email, Regexp, EqualTo

from flaskext.mysql import MySQL
from passlib.hash import sha256_crypt
import logging
Articles = Articles()

app = Flask(__name__)

# config db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# init MYSQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html',articles=Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html',id=id)



class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=2,max=20),validators.DataRequired()])
    username = StringField('Username',[validators.Length(min=2,max=20),validators.DataRequired()])
    email = StringField('Email',[validators.Length(min=2,max=20),validators.DataRequired()])
    password = PasswordField('Password',[
        validators.DataRequired()])
    confirm = PasswordField('Confirm',[
        validators.DataRequired(),
        EqualTo('password', message='Passwords must match')
        ])

@app.route('/register',methods=['GET','POST'])
def register():
    
    form = RegisterForm(request.form)
    app.logger.info(form)
    print('hello world')
    if request.method == 'POST' and form.validate():
        print("helooooooo")
        name = form.name.data
        app.logger.info(name)
        email = form.email.data
        username = form.username.data
        print('email' + email)
        password = sha256_crypt(form.password.data)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,email,username,password) VALUES (%s,%s,%s,%s)",(name,email,username,password))
        #commit to mysql
        mysql.coonection.commit()
        # close connection 
        cur.close()

        flash('You are now registered and can log in','success')
        return redirect(url_for('about'))
        
    return render_template('register.html',form=form)
    
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
