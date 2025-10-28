from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Post, Comment
from .forms import PostForm, CommentForm
from . import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)

@main_bp.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(title=form.title.data, body=form.body.data, author_id=current_user.id)
        db.session.add(p); db.session.commit()
        flash("글이 등록되었습니다.", "success")
        return redirect(url_for("main.index"))
    return render_template("new_post.html", form=form)

@main_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("로그인 후 댓글을 달 수 있습니다.", "warning")
            return redirect(url_for("auth.login"))
        c = Comment(body=form.body.data, author_id=current_user.id, post_id=post.id)
        db.session.add(c); db.session.commit()
        flash("댓글이 등록되었습니다.", "success")
        return redirect(url_for("main.post_detail", post_id=post.id))
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.created_at.asc()).all()
    return render_template("post_detail.html", post=post, form=form, comments=comments)
