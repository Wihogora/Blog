from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    subscription = db.Column(db.Boolean)
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    
    posts = db.relationship('Post', backref='post', lazy="dynamic")
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

# class Pitch(db.Model):
#     __tablename__ = 'pitches'

#     id = db.Column(db.Integer,primary_key = True)
#     pitch_title = db.Column(db.String)
#     pitch_content = db.Column(db.String(1000))
#     category = db.Column(db.String)
#     posted = db.Column(db.DateTime,default=datetime.utcnow)
#     user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
#     likes = db.Column(db.Integer)
#     dislikes = db.Column(db.Integer)

#     comments = db.relationship('Comment',backref =  'pitch_id',lazy = "dynamic")

#     def save_pitch(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_pitches(cls,category):
#         pitches = Pitch.query.filter_by(category=category).all()
#         return pitches

#     @classmethod
#     def get_pitch(cls,id):
#         pitch = Pitch.query.filter_by(id=id).first()

#         return pitch

#     @classmethod
#     def count_pitches(cls,uname):
#         user = User.query.filter_by(username=uname).first()
#         pitches = Pitch.query.filter_by(user_id=user.id).all()

#         pitches_count = 0
#         for pitch in pitches:
#             pitches_count += 1

#         return pitches_count
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __repr__(self):
        return f'User {self.name}'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='post_id', lazy='dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def get_post(id):
        post = Post.query.filter_by(id=id).first()
        return post
        






























