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
            flash('You\'ve created a post!', category='success')
            return redirect(url_for('ig.getAllPosts'))


    return render_template('createPost.html', form=form)
# get all posts from database

@ig.route('/')
@ig.route('/posts')
def getAllPosts():
    posts = Post.query.all()
    return render_template('feed.html', posts=posts)

@ig.route('/posts/<int:post_id>')
def singlePost(post_id):
    post = Post.query.get(post_id)
    return render_template('singlePost.html', post=post)

@ig.route('/posts/update/<int:post_id>', methods=['GET', 'POST'])
def updatePost(post_id):
    form = PostForm()
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
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
            flash('You\'ve updated your post!', category='success')            
            return render_template('updatePost.html', form=form, post=post)

@ig.route('/posts/delete/<int:post_id>')
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        return redirect(url_for('ig.singlePost', post_id=post_id))
    
    # delete data from database
    db.session.delete(post)
    db.session.commit()
    flash('You\'ve deleted your post!', category='success')
    return redirect(url_for(('ig.getAllPosts')))




############################## API ROUTES #################################
# @ig.route('/api/posts/')
# def getAllPostsAPI():
#     posts = Post.query.all()
#     my_posts = [post.to_dict() for post in posts]
#     return {'posts': my_posts}

# adding the layer of security (basic) #
@ig.route('/api/posts')
def getAllPostsAPI():
    args = request.args
    print(args)
    pin = args.get('pin')
    print(pin, type(pin))
    if pin == '1234':
        posts = Post.query.all()
        my_posts = [post.to_dict() for post in posts]
        return {'posts': my_posts}
    else:
        return {
          'status': 'error',
          'code': 'pin error',
          'message': 'invalid pin, please try again'
        }

# Get single post
@ig.route('/api/posts/<int:post_id>')
def getSinglePostsAPI(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'post': post.to_dict()
            }
    else:
        return {
            'status': 'error',
            'code': 'post error',
            'message': 'invalid post, please try again'
        }

# Get create post (Post Request)
@ig.route('/api/posts/create', methods=["POST"])
def createPostAPI():
    data = request.json # this is coming from POST request body
    print(data)
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
        'message': 'Post was successfully created.'
    }