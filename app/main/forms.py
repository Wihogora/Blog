from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required
from ..models import Subscribe

class PostForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    text = TextAreaField('Text', validators=[Required()])
    submit = SubmitField('Submit', validators=[Required()])

# class UpdateProfile(FlaskForm):
#     bio = TextAreaField('Your Bio.',validators = [Required()])
#     submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    names = StringField('Username', validators=[Required()])
    text = TextAreaField('Leave a comment:', validators=[Required()])
    submit = SubmitField('Submit')

# class SubscribeForm(FlaskForm):
#     email = StringField('Email', validators=[Required()])
#     submit = SubmitField('Submit')

class SubscribeForm(FlaskForm):
    email = StringField('Email ', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        email = Subscribe.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is already subscribed to our emailing list.')
