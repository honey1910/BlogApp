from app import app, mongo, bcrypt, login_manager
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from models import User, Blog

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def home():
    blogs = Blog.get_all()
    return render_template('home.html', blogs=blogs)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user_data = {"username": username, "email": email, "password": password}
        mongo.db.users.insert_one(user_data)
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:   
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = mongo.db.users.find_one({"email": email})
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(user_data['username'], user_data['email'], user_data['password'], user_data['_id'])
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    blogs = Blog.get_all()
    return render_template('dashboard.html', username=current_user.username, blogs=blogs)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = current_user.username
        Blog.create(title, content, author)
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_blog.html')

@app.route('/blog/<blog_id>')
def view_blog(blog_id):
    blog = Blog.get(blog_id)
    if blog:
        return render_template('blog.html', blog=blog)
    else:
        flash('Blog post not found', 'danger')
        return redirect(url_for('home'))

@app.route('/delete_blog/<blog_id>')
@login_required
def delete_blog(blog_id):
    blog = Blog.get(blog_id)
    if blog and blog.author == current_user.username:
        Blog.delete(blog_id)
        flash('Blog post deleted successfully!', 'success')
    else:
        flash('You are not authorized to delete this blog post', 'danger')
    return redirect(url_for('dashboard'))
