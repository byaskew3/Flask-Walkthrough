from flask import Blueprint, render_template, request
from app.models import Post

from app.ig.forms import CreatePostForm
from flask_login import current_user

ig = Blueprint('ig', __name__, template_folder='igtemplates')

from app.models import db

@ig.route('/posts/create', methods=['GET', 'POST'])
def createPost():
    form = CreatePostForm()
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


    return render_template('createPost.html', form=form)

@ig.route('/posts')
def getAllPosts():
    return render_template('createPost.html')

@ig.route('/posts/delete')
def deletePost():
    return render_template('createPost.html')