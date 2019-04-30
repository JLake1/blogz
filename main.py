from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:cheese@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

#TODO login and signup page validations

#TODO logout link broken when user isn't logged in -- hide link or create if statement


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    #revisit backref parameter

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'list_blogs', 'test_blogs', 'index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login?login-required')


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = ""

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            flash(email)
            #return render_template('add.html', user=user)
            return redirect('/add')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html', email=email)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        if password != verify:
            flash("Passwords do not match")
            return render_template('signup.html')
            # TODO retain user email after redirect

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            user = User.query.filter_by(email=email).first()
            flash("New user registered")
            flash(email)
            #return render_template('add.html', user=user)
            return redirect('/add')
        else:
            # TODO - user better response messaging
            flash("Username is already taken")
            #return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

 
@app.route('/blog', methods=['GET', 'POST'])
def test_blogs():

    blog_id = ""
    author_id = ""
    
    authors = User.query.all()
    
    print(author_id)
    

    if request.method == 'GET':
        
        blog_id = request.args.get('id') 
        author_id = request.args.get('author_id')
        authors = User.query.all()
 
        if blog_id:
            blogs = Blog.query.filter_by(id=blog_id).first()
            authors = User.query.all()

        elif author_id:
            blogs = Blog.query.filter_by(owner_id=author_id) 
            
            return render_template('blog.html', blogs=blogs, blog_id=blog_id, authors=authors, author_id=author_id)

        else:
            blogs = Blog.query.order_by(desc(Blog.id))  
            authors = User.query.all()

            return render_template('blog.html', blogs=blogs, blog_id=blog_id, authors=authors, author_id=author_id)

        return render_template('single.html', blogs=blogs, blog_id=blog_id, authors=authors, author_id=author_id)   

    return render_template('blog.html', blogs=blogs, blog_id=blog_id, authors=authors, author_id=author_id)

@app.route('/add', methods=['POST', 'GET'])
def add():

    blog_title = Blog.title
    form_value = request.args.get('title')
    blogs = Blog.query.all()
    email = session['email']
 
    if request.method == 'GET':
        
        user_id = "test" 
        blog_id = request.args.get('id')
        blogs = Blog.query.filter_by(id=blog_id).first() 
        blogs_title = Blog.query.filter_by(id=blog_id)


        return render_template('add.html', title="Add form GET", blog_title=blog_title, blogs=blogs, blog_id=blog_id, user_id=user_id, blogs_title=blogs_title)

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        owner = User.query.filter_by(email=session['email']).first()
        
        new_title = Blog(blog_title, blog_body, owner)
        
        if not blog_title:
            if not blog_body:
                flash('Please enter a title and body')
            else:
                flash('Please enter a title')
            return redirect('/add')
            
        if not blog_body: 
            flash('Please fill out the body section')
            return redirect('/add')

        db.session.add(new_title) 
        db.session.commit()
        user_id =  str(new_title.id)
        url = '/blog?id=' + user_id
        return redirect(url) 
    
    blogs = Blog.query.all()
    form_value = request.args.get('title')
    print(form_value) 

    return render_template('add.html', title="Main Blog", url=url, new_title=new_title, blog_title=blog_title, blog_body=blog_body, blogs=blogs, form_value=form_value, user_id=user_id)

@app.route('/logout')
def logout():
    del session['email']
    return redirect('/blog')

@app.route('/', methods=['POST', 'GET'])
def index():

    #new_title=""
    #new_body= ""
    #blog_title = request.args.get('title')
    #owner_id = request.args.get('owner_id')
    #owner_id = int(owner_id)
    # TODO fix--> owner_id = request.args.get('owner_id')
 
    blog_id = ""

    if request.method == 'GET':
        
        authors = User.query.all()  
 

        return render_template('index.html', title="Title", authors=authors)

    return render_template('index.html', title="Title", authors=authors)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == '__main__':
    app.run()