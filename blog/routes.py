from blog import app, db
from blog.models import User, Post
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def index():
    post = Post.query.all()
    return render_template('home.html', posts=post)

@app.route('/register')
def register():
    if request.args:
        username = request.args.get('user')
        password = request.args.get('pass')
        if User.query.filter_by(username=username).first():
            return render_template('invalid_Register.html')
        else:
            db.session.add(User(username=username, password=password))
            db.session.commit()
            flash('you registered successfully...', 'success')
            login_user(User.query.filter_by(username=username, password=password).first(), remember=True)
            return redirect(url_for('index'))
    else:
        return render_template('Register.html')

@app.route('/login')
def login():
    if not current_user.is_authenticated:
        if request.args:
            username = request.args.get('user')
            password = request.args.get('pass')
            next_page = request.args.get('next')
            if username and password:
                if User.query.filter_by(username=username, password=password).first():
                    if request.args.get('Remember') == 'on':
                        login_user(User.query.filter_by(username=username, password=password).first()
                                                                                    , remember=True)
                    else:
                        login_user(User.query.filter_by(username=username, password=password).first())
                    flash('you logedd is successfully', 'success')
                    if not next_page:
                        return redirect(url_for('index'))
                    else:
                        return redirect(next_page)
            
                else:
                    return render_template('invalid_Login.html')
            else:
                print(request.args.get('next'))
                return render_template('Login.html', next=request.args.get('next'))
        else:
            return render_template('Login.html')
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def log_out():
    if current_user.is_authenticated:
        logout_user()
        flash('you logedd out is successfully', 'success')
        return redirect(url_for('index'))
    else:
        flash('you are not logedd in', 'warning')
        return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    if request.args.get('Error'):
        return render_template('Profile.html', Err=True)
    else:
        return render_template('Profile.html')

@app.route('/change')
@login_required
def change():
    if request.args:
        username = request.args.get('user')
        password = request.args.get('pass')
        if username:
            if not User.query.filter_by(username=username).first() or username == current_user.username:
                current_user.username = username
                db.session.commit()
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('profile', Error='username'))
        elif password:
            current_user.password = password
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            return '401 - Bad request'
    else:
        return '401 - Bad request'

@app.route('/DelAcc')
@login_required
def delete_account():
    return abort(500)

@app.route('/write', methods=['POST', "GET"])
@login_required
def write():
    if request.form:
        print(12)
        Title = request.form.get('title')
        Text = request.form.get('content')
        if Title and Text:
            print(34)
            P = Post(Title=Title, content=Text, writer=current_user)
            db.session.add(P)
            db.session.commit()
            flash('post created', 'success')
            return redirect(url_for('index'))
        else:
            return render_template('create_post.html')

    return render_template('create_post.html')

@app.route('/posts/<int:id>')
def posts(id):
    P = Post.query.get_or_404(id)
    return render_template('show_post.html', post=P)

@app.route('/posts/<int:id>/delete')
@login_required
def delet(id):
    P = Post.query.get_or_404(id)
    if P.writer != current_user:
        return abort(403)
    else:
        db.session.delete(P)
        db.session.commit()
    flash('post deleted', 'info')
    return redirect(url_for('index'))

@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
@login_required
def UpDate(id):
    P = Post.query.get_or_404(id)
    if P.writer != current_user:
        return abort(403)
    else:
        Title = request.form.get('title')
        content = request.form.get('content')
        if Title:
            P.Title = Title
            db.session.commit()
            print(Title)
        if content:
            P.content = content
            db.session.commit()
            print(content)
        else:
            return render_template('Update.html', Title=P.Title, content=P.content)
        flash('post Updated', 'info')
        return redirect(url_for('index'))
    flash('post Updated', 'info')
    return redirect(url_for('index'))