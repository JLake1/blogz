from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:asdf@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

"""
@app.route('/blog?<url>', methods=['GET'])
def single_post(url):
    return render_template('single.html', title="Main Blog", new_title=new_title, new_body=new_body, blogs=blogs)
    #return redirect("http://{0}/munin".format(field))
"""

 
@app.route('/blog', methods=['GET', 'POST'])
def page():
 
    blog_title = Blog.title
    form_value = request.args.get('title')
    blogs = Blog.query.all()
    

    if request.method == 'GET':
        
        #blog_title= "abc"
        #blog_title = request.args.get('blog_title')
        blog_id = request.args.get('id')
        blogs = Blog.query.filter_by(id=blog_id).first() 

        blogs_title = Blog.query.filter_by(id=blog_id)

        return render_template('single.html', title="If Get Statement Blog", blog_title=blog_title, blogs=blogs, blog_id=blog_id, blogs_title=blogs_title)

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_title = Blog(blog_title, blog_body)
        #new_body = Blog(blog_title, blog_body)
        db.session.add(new_title)
        #db.session.add(new_body)
        db.session.commit()
        return render_template('single.html', title="If Post Statement Blog", new_title=new_title, blog_title=blog_title, blog_body=blog_body, blogs=blogs)

    


    blogs = Blog.query.all()
    form_value = request.args.get('title')
    print(form_value) 

    return render_template('single.html', title="Main Blog", new_title=new_title, blog_title=blog_title, blog_body=blog_body, blogs=blogs, form_value=form_value)
 
@app.route('/add', methods=['POST', 'GET'])
def add():

 
    blog_title = Blog.title
    form_value = request.args.get('title')
    blogs = Blog.query.all()
    

    if request.method == 'GET':
        
        #blog_title= "abc"
        #blog_title = request.args.get('blog_title')
        user_id = "test"
        #user_id = request.args.get('id')
        blog_id = request.args.get('id')
        blogs = Blog.query.filter_by(id=blog_id).first() 

        blogs_title = Blog.query.filter_by(id=blog_id)

        return render_template('add.html', title="Add form GET", blog_title=blog_title, blogs=blogs, blog_id=blog_id, user_id=user_id, blogs_title=blogs_title)

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_title = Blog(blog_title, blog_body)
        
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
        #db.session.add(new_body)
        db.session.commit()
        user_id =  str(new_title.id)
        url = '/blog?id=' + user_id
        return redirect(url)
        #return render_template('add.html', url=url, title="Add form POST", new_title=new_title, blog_title=blog_title, blog_body=blog_body, blogs=blogs, user_id=user_id)

    


    blogs = Blog.query.all()
    form_value = request.args.get('title')
    print(form_value) 

    return render_template('add.html', title="Main Blog", url=url, new_title=new_title, blog_title=blog_title, blog_body=blog_body, blogs=blogs, form_value=form_value, user_id=user_id)



@app.route('/', methods=['POST', 'GET'])
def index():

    new_title=""
    new_body= ""
    blog_title = request.args.get('title')

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_title = Blog(blog_title, blog_body)
        #new_body = Blog(blog_title, blog_body)
        db.session.add(new_title)
        #db.session.add(new_body)
        db.session.commit()
        
    #user_id = request.args.get('id')
    #print(user_id)

    blogs = Blog.query.all()

    return render_template('blog.html', title="Main Blog", new_title=new_title, new_body=new_body, blogs=blogs, blog_title=blog_title)
    #return redirect("/")

    """
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Get It Done!", 
        tasks=tasks, completed_tasks=completed_tasks)
    """

"""
@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')
"""

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RU'

if __name__ == '__main__':
    app.run()