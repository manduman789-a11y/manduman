from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    email = StringField("이메일", validators=[DataRequired(), Email(), Length(max=255)])
    name = StringField("이름", validators=[DataRequired(), Length(max=120)])
    password = PasswordField("비밀번호", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField("비밀번호 확인", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("회원가입")

class LoginForm(FlaskForm):
    email = StringField("이메일", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    submit = SubmitField("로그인")

class PostForm(FlaskForm):
    title = StringField("제목", validators=[DataRequired(), Length(max=200)])
    body = TextAreaField("내용", validators=[DataRequired()])
    submit = SubmitField("등록")

class CommentForm(FlaskForm):
    body = TextAreaField("댓글", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("댓글 달기")
