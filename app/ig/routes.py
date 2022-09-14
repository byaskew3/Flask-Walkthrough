from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Post

from app.ig.forms import PostForm
from flask_login import current_user, login_required

ig = Blueprint('ig', __name__, template_folder='igtemplates')

from app.models import db

@ig.route('/posts/create', methods=['GET', 'POST'])
@login_required
def createPost():
    form = PostForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            # add post to database
            post = Post(title, img_url, caption, current_user.id)

            # add instance to database
            db.session.add(post)
            db.session.commit()

            flash('Successfully created post.', category='success')
        else:
            flash('Invalid form, please check input fields!', category='danger')


    return render_template('createPost.html', form=form)

@ig.route('/')
@ig.route('/posts')
def getAllPosts():
    posts = Post.query.all()
    print(posts)
    return render_template('feed.html', posts=posts)

@ig.route('/posts/<int:post_id>') # dynamic route
def singlePost(post_id):
    post = Post.query.get(post_id)
    return render_template('singlePost.html', post=post)

@ig.route('/posts/update/<int:post_id>', methods=['GET','POST']) # dynamic route
def updatePost(post_id):
    form = PostForm()
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        flash('You are not allowed to update another user\'s post', category='danger')
        return redirect(url_for('ig.singlePost', post_id=post_id))
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            # update post from database
            post.title = title
            post.img_url = img_url
            post.caption = caption

            db.session.commit()
            flash('Successfully updated post.', category='success')
            return redirect(url_for('ig.singlePost', post_id=post_id))
        else:
            flash('Invalid form, please check input fields!', category='danger')
    return render_template('updatePost.html', form=form, post=post)

@ig.route('/posts/delete/<int:post_id>')
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        flash('You are not allowed to delete another user\'s post', category='danger')
        return redirect(url_for('ig.singlePost', post_id=post_id))
    # delete post from database
    db.session.delete(post)
    db.session.commit()
    flash('Successfully deleted post.', category='success')
    return redirect(url_for('ig.getAllPosts'))


############### API ROUTES ######################
# adding layer of security (Basic: Auth)
# @ig.route('/api/posts')
# def getAllPostsAPI():
#     posts = Post.query.all()
#     posts_json = [post.to_dict() for post in posts]
#     return {
#         'posts': posts_json
#     }

# get single post
@ig.route('/api/posts/<int:post_id>')
def getSinglePostAPI(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'post': post.to_dict()
        }
    else:
        return {
            'status': 'error',
            'code': 'Post does not exist',
            'message': 'Please access a post that exists'
        }

# create post (post request)
@ig.route('/api/posts/create', methods=['POST'])
def createPostAPI():
    data = request.json # this coming from the POST body
    title = data['title']
    img_url = data['img_url']
    caption = data['caption']
    user_id = data['user_id']

    post = Post(title, img_url, caption, user_id)

    # add instance to database
    db.session.add(post)
    db.session.commit()

    return {
        'status': 'ok',
        'message': 'Post has successfully created.'
    }