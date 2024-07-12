from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import openai

class Dream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    dreamer_background = db.Column(db.String(10000))
    wakeup_state = db.Column(db.String(10000))
    dreami_inter = db.Column(db.String(10000))
    rating1 = db.Column(db.Integer)
    rating2 = db.Column(db.Integer)
    comments = db.relationship('Comment')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    public = db.Column(db.String(10), default='yes')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    job_title = db.Column(db.String(1000), default=' ')
    dreams = db.relationship('Dream')
    commenter = db.relationship('Comment')
    profiles = db.relationship('Profile', uselist=False)
    upvoters = db.relationship('Upvote')


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(110))
    country = db.Column(db.String(110))
    relationship = db.Column(db.String(110))
    occupation = db.Column(db.String(110))
    struggles = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    dream_id = db.Column(db.Integer, db.ForeignKey('dream.id'))
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    upvote_user = db.relationship('Upvote')

class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer, default=0)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    upvoter_id = db.Column(db.Integer, db.ForeignKey('user.id'))

def gpt3_classifier(dream_text, user_bg, wakeup_st, fine_tuned_model, is_log=False):
    if not user_bg or user_bg == '':
        user_bg = '__'

    if not wakeup_st or wakeup_st == '':
        wakeup_st = '__'

    item = 'Dream_Text: '+dream_text.strip()+'.'+' ; '+' Background_Info: '+user_bg.strip()+' ; '+' Wakeup_State: '+wakeup_st.strip()+' ###'
    result = openai.Completion.create(model=fine_tuned_model,
                                      prompt=item,
                                      max_tokens=600, temperature=0.7, frequency_penalty= 0.5 , presence_penalty= 0.5,  stop=[" [END]"] )['choices'][0]['text']

    if is_log: print('- ', item, ': ', result)

    return result