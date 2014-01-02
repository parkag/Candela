from app import db
from hashlib import md5

ROLE_STUDENT = 0
ROLE_ADMIN = 1

CATEGORY_NEWS = 0
CATEGORY_NOTES = 1
CATEGORY_QUESTIONS = 2
CATEGORY_STREAM = 3

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    #index_number = db.Column(db.Integer)
    password = db.Column(db.String(500))
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_STUDENT)
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    comments = db.relationship('Comment', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(200))
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() +'?d=mm&s=' + str(size)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname

    def __repr__(self):
        return '<User %r>' %(self.nickname)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(500))
    salt = db.Column(db.String(10))

    def __repr__(self):
        return '<Registration %r>' %(self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(5000))
    short = db.Column(db.String(300))
    category = db.Column(db.SmallInteger, default = CATEGORY_NEWS)
    thumbnail_link = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' %(self.body)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    comments = db.relationship('Post', backref = 'comments', lazy = 'dynamic')

    def __repr__(self):
        return '< Comment %r>' %(self.body)
