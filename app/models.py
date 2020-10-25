from flask_login import UserMixin

from . import db, login_manager

from werkzeug.security import generate_password_hash,check_password_hash
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    picth = db.relationship('Pitch',backref = 'pitch',lazy="dynamic")

    # @property
    # def password(self):
    #     raise AttributeError('You cannnot read the password attribute')

    def set_password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'
class Category(db.Model):
    __tablename__ = 'categorys'

    id = db.Column(db.Integer,primary_key = True)     
    name = db.Column(db.String(255),index = True)
    pitch = db.relationship('Pitch',backref = 'cat_ pitch',lazy="dynamic")

class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)    
    title = db.Column(db.String(255),index = True)
    content = db.Column(db.String(255),index = True)
    user = db.Column(db.Integer,db.ForeignKey('users.id'))       
    category = db.Column(db.Integer,db.ForeignKey('categorys.id'))       
    votes = db.Column(db.Integer,nullable=True)    