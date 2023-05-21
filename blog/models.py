from blog import db, Lomg
from datetime import datetime
from flask_login import UserMixin

@Lomg.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password =  db.Column(db.String(50), unique=False, nullable=False)
    posts = db.relationship("Post", backref='writer', lazy=True)
    def delete_account(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} ---> {self.username})'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now, nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(30), default='...')
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.date.strftime("%Y - %m - %d")} ---> {self.Title[:30]})'