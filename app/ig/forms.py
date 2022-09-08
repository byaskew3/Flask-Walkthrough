from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    img_url = StringField('Image URL:', validators=[])
    caption = StringField('Caption', validators=[])
    submit = SubmitField()