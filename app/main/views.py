from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User, Post, Comment, Subscribe
from .. import db
from .forms import PostForm, CommentForm, SubscribeForm
from flask_login import login_required, current_user
import datetime
from ..email import mail_message
from ..request import get_quotes
#Views


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to my favorite Blog!!'
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    quotes= get_quotes()
    return render_template('index.html', title=title,  posts=posts, quotes=quotes)


@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.title.data
        text = post_form.text.data

        users = User.query.all()

        # Update post instance
        new_post = Post(title=title, text=text, post=current_user)

        # Save post method
        new_post.save_post()

        for user in users:
            if user.subscription:
                mail_message("New Post", "email/new_post",user.email, user=user)

        return redirect(url_for('.index'))

    # else:
    #     return redirect(url_for('.index'))

    title = 'New post'
    return render_template('new_post.html', title=title, post_form=post_form)


@main.route('/posts')
def all_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()

    title = 'Blogger posts'

    return render_template('posts.html', title=title, posts=posts)


@main.route('/post/<int:id>', methods=['GET', 'POST'])

def post(id):
    form = CommentForm()
    post = Post.get_post(id)

    if form.validate_on_submit():
        comment = form.text.data
        username = form.names.data
        new_comment = Comment(username=username,comment=comment, post=post.id)

        new_comment.save_comment()

    comments = Comment.get_comments(post)

    title = f'{post.title}'
    return render_template('post.html', title=title, post=post, form=form, comments=comments)


@main.route('/delete_comment/<id>/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id, post_id):
    comment = Comment.query.filter_by(id=id).first()

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.post', id=post_id))


@main.route('/delete_post/<id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.all_posts'))


@main.route('/subscribe/', methods=['GET', 'POST'])

def subscribe():
    """
    Function that enables one to subscribe to the post blog
    """
    form = SubscribeForm()
    if form.validate_on_submit():
        subscribe = Subscribe(email=form.email.data)
        db.session.add(subscribe)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('auth/subscribe.html', form=form)



@main.route('/post/update/<id>', methods=['GET', 'POST'])
@login_required
def update_post(id):
    form = PostForm()

    post = Post.query.filter_by(id=id).first()

    form.title.data = post.title
    form.text.data = post.text

    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data

        post.title = title
        post.text = text

        db.session.commit()

        return redirect(url_for('main.post', id=post.id))

    return render_template('update.html', form=form)

