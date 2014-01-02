# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import Required, EqualTo, Length, Email, ValidationError
from app.models import User

class SignupForm(Form):
    username = TextField('username', 
        validators = [Required(message=u'Proszę wpisać nazwę użytkownika.')])
    password = PasswordField('password',
        validators = [Required(message=u'Proszę wypełnić pole hasło.')])
    password_again = PasswordField('password_again',
        validators = [Required(), EqualTo('password', message=u'Powtórzone hasło nie zgadza się z oryginalnym.')])
    email = TextField('email',
        validators = [Required(message=u'Proszę wpisać adres e-mail'), Email(message=u'To nie jest prawidłowy adres e-mail')])

    def is_faculty_email(form, field):
        if field.data.endswith('@student.if.pw.edu.pl') == False:
            raise ValidationError(u'Twój adres e-mail nie został zaakceptowany.')


class LoginForm(Form):
    username = TextField('username',
        validators = [Required(message=u'Proszę podać nazwę użytkownika')])
    password = PasswordField('password',
        validators = [])
    remember_me = BooleanField('remember_me', default = True)
    
    """def validate(self):
        if not Form.validate(self):
            return False
        if /username in db/ and hash(password) for this username = hash(password_in_form):
            return True
    """

class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 200)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('Ten nick jest już w użyciu. Wybierz inny.')
            return False
        return True

class PostForm(Form):
    title = TextField('title', 
        validators = [Required(message = u'Dodaj tytuł :)'), Length(min = 5, max = 100)])
    picture = TextField('picture', 
        validators = [Required(message =u'Przydałaby się jeszcze jakaś miniaturka'), Length(min = 10, max = 200)])
    body = TextAreaField('body',
        validators = [Required(message =u'Dodaj opis.'), Length(min = 5, max = 5000)])

class CommentForm(Form):
    text = TextAreaField('text', 
        validators = [Required(message = u'Dodaj treść komentarza.'), Length(min=10, max = 1000)])


