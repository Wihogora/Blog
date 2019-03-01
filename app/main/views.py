from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PostForm, CommentForm
from .. import db,photos
from ..models import User, Post, Comment
from flask_login import login_required,current_user
import datetime
from ..email import mail_message

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to my favorite Blog!!'

   return render_template('index.html', title=title, posts=posts)



# @main.route('/user/<uname>')
# def profile(uname):
#     user = User.query.filter_by(username = uname).first()
#     pitches_count = Pitch.count_pitches(uname)
#     if user is None:
#         abort(404)

#     return render_template("profile/profile.html", user = user,pitches = pitches_count)


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
                mail_message("New Post", "email/new_post", user.email, user=user)

        return redirect(url_for('.index'))


     else:
        return redirect(url_for('.index'))

    title = 'New post'
    return render_template('new_post.html', title=title, post_form=post_form)





# @main.route('/user/<uname>/update/pic',methods= ['POST'])
# @login_required
# def update_pic(uname):
#     user = User.query.filter_by(username = uname).first()
#     if 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         path = f'photos/{filename}'
#         user.profile_pic_path = path
#         db.session.commit()
#     return redirect(url_for('main.profile',uname=uname))


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

        new_comment = Comment(comment=comment, user=current_user, post=post.id)

        new_comment.save_comment()

    comments = Comment.get_comments(post)

    title = f'{post.title}'
    return render_template('post.html', title=title, post=post, form=form, comments=comments)



# @main.route('/user/<uname>/pitches')
# def user_pitches(uname):
#     user = User.query.filter_by(username=uname).first()
#     pitches = Pitch.query.filter_by(user_id = user.id).all()
#     pitches_count = Pitch.count_pitches(uname)
#     user_joined = user.date_joined.strftime('%b %d, %Y')

#     return render_template("profile/user.html", user=user,pitches=pitches,pitches_count=pitches_count)


@main.route('/delete_comment/<id>/<post_id>', methods=['GET', 'POST'])
def delete_comment(id, post_id):
    comment = Comment.query.filter_by(id=id).first()

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.post', id=post_id))


@main.route('/delete_post/<id>', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.all_posts'))


@main.route('/subscribe/<id>')
def subscribe(id):
    user = User.query.filter_by(id=id).first()

    user.subscription = True

    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/post/update/<id>', methods=['GET', 'POST'])
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





















# Views
# @app.route('/')
# def index():

#     '''
#     View root page function that returns the index page and its data
#     '''

#     message = 'Hello World'
#     return render_template('index.html',message = message)
# @main.route('/')
# def index():

#     '''
#     View root page function that returns the index page and its data
#     '''

#     # Getting popular movie
#     popular_movies = get_movies('popular')
#     upcoming_movie = get_movies('upcoming')
#     now_showing_movie = get_movies('now_playing')

#     title = 'Home - Welcome to The best Movie Review Website Online'

#     search_movie = request.args.get('movie_query')

#     if search_movie:
#         return redirect(url_for('search',movie_name=search_movie))
#     else:
#         return render_template('index.html', title = title, popular = popular_movies, upcoming = upcoming_movie, now_showing = now_showing_movie )
# @main.route('/movies/<int:id>')
# def movies(movie_id):

#     '''
#     View movie page function that returns the movie details page and its data
#     '''
#     return render_template('movie.html',id = movie_id)
# @main.route('/movie/<int:id>')
# def movie(id):

#     '''
#     View movie page function that returns the movie details page and its data
#     '''
#     movie = get_movie(id)
#     title = f'{movie.title}'
#     reviews = Review.get_reviews(movie.id)

#     return render_template('movie.html',title = title,movie = movie,reviews = reviews)

# @main.route('/search/<movie_name>')
# def search(movie_name):
#     '''
#     View function to display the search results
#     '''
#     movie_name_list = movie_name.split(" ")
#     movie_name_format = "+".join(movie_name_list)
#     searched_movies = search_movie(movie_name_format)
#     title = f'search results for {movie_name}'
#     return render_template('search.html',movies = searched_movies)

# @main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
# @login_required
# def new_review(id):
#     form = ReviewForm()
#     movie = get_movie(id)

#     if form.validate_on_submit():
#         title = form.title.data
#         review = form.review.data
#         new_review = Review(movie.id,title,movie.poster,review)
#         new_review.save_review()
#         return redirect(url_for('movie',id = movie.id ))

#     title = f'{movie.title} review'
#     return render_template('new_review.html',title = title, review_form=form, movie=movie)
    

