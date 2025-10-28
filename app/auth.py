from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegisterForm, LoginForm
from .models import User
from . import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("이미 존재하는 이메일입니다.", "warning")
        else:
            u = User(email=form.email.data, name=form.name.data)
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            flash("회원가입 완료. 로그인해주세요.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if not u or not u.check_password(form.password.data):
            flash("이메일 또는 비밀번호가 올바르지 않습니다.", "danger")
        else:
            login_user(u)
            flash("로그인되었습니다.", "success")
            next_url = request.args.get("next") or url_for("main.index")
            return redirect(next_url)
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("로그아웃되었습니다.", "info")
    return redirect(url_for("main.index"))
