from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Dream
from .models import User
from .models import Profile
from .models import gpt3_classifier
from .models import Comment
from .models import Upvote
from . import db
import json
import openai

with open('./ai_model/OpenAI_key.txt') as f:
    lines = f.readlines()
openai.api_key = str(lines[0])

views = Blueprint('views',__name__)


@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        try:
            if (request.form.get('submit')):
                comment = request.form.get('comment')
                dream_id1 = request.form.get('dreamid')

                if len(comment)<1:
                    flash('Interpretation is too short!', category='error')

                else:

                    new_comment = Comment(data=comment, commenter_id=current_user.id, dream_id=dream_id1)
                    db.session.add(new_comment)
                    db.session.commit()

            if (request.form.get('submit2')):
                if (request.form.get('star5')):
                    new_ratings = 5
                elif (request.form.get('star4')):
                    new_ratings = 4
                elif (request.form.get('star3')):
                    new_ratings = 3
                elif (request.form.get('star2')):
                    new_ratings = 2
                elif (request.form.get('star1')):
                    new_ratings = 1
                else:
                    new_ratings = 0

                commentid = request.form.get('submit2')
                new_upvote = Upvote(vote=new_ratings, upvoter_id=current_user.id, comment_id=commentid)
                db.session.add(new_upvote)
                db.session.commit()
                flash('Voting added!', category='success')


            return redirect(url_for('views.home'))

        except Exception as e:
            print(e)
            flash('Something went wrong. Check your input(s).', category='error')

    return render_template("home.html", user=current_user, dreams=Dream, users=User, comments=Comment, upvote=Upvote)

@views.route('/mydreams', methods=['GET','POST'])
@login_required
def mydreams():
    if request.method == 'POST':
        try:
            if (request.form.get('submit')):
                comment = request.form.get('comment')
                dream_id1 = request.form.get('dreamid')

                if len(comment) < 1:
                    flash('Interpretation is too short!', category='error')

                else:

                    new_comment = Comment(data=comment, commenter_id=current_user.id, dream_id=dream_id1)
                    db.session.add(new_comment)
                    db.session.commit()

            if (request.form.get('submit2')):
                if (request.form.get('star5')):
                    new_ratings = 5
                elif (request.form.get('star4')):
                    new_ratings = 4
                elif (request.form.get('star3')):
                    new_ratings = 3
                elif (request.form.get('star2')):
                    new_ratings = 2
                elif (request.form.get('star1')):
                    new_ratings = 1
                else:
                    new_ratings = 0

                commentid = request.form.get('submit2')
                new_upvote = Upvote(vote=new_ratings, upvoter_id=current_user.id, comment_id=commentid)
                db.session.add(new_upvote)
                db.session.commit()
                flash('Voting added!', category='success')

            return redirect(url_for('views.home'))

        except Exception as e:
            print(e)
            flash('Something went wrong. Check your input(s).', category='error')

    return render_template("mydreams.html", user=current_user, dreams=Dream, users=User, comments=Comment, upvote=Upvote)


@views.route('/adddream', methods=['GET','POST'])
@login_required
def adddream():
    if request.method == 'POST':
        try:
            dream = request.form.get('dream')
            user_bg = request.form.get('user_bg')
            wakeup_st = request.form.get('wakeup_st')
            if(request.form.get('submit_no')):
                public_val='no'
            elif(request.form.get('submit_yes')):
                public_val='yes'

            if len(dream)<3:
                flash('Dream text is too short!', category='error')
            else:
                response = gpt3_classifier(
                    dream, user_bg, wakeup_st,
                    fine_tuned_model='davinci:ft-personal:dreami0-1-2022-06-07-18-52-10', is_log=True)

                new_dream = Dream(data=dream, user_id=current_user.id, public=public_val,
                                 dreamer_background=user_bg, wakeup_state=wakeup_st,
                                 dreami_inter=response)
                db.session.add(new_dream)
                db.session.commit()
                flash('Dream added!', category='success')
                return redirect(url_for('views.viewdream'))
        except Exception as e:
            print(e)
            flash('Something went wrong. Check your input(s).', category='error')


    return render_template("adddream.html", user=current_user, dream=None)


@views.route('/profileview', methods=['GET', 'POST'])
@login_required
def profileview():
    if request.method == 'POST':
        return redirect(url_for('views.profile'))

    return render_template("profileview.html", user=current_user, profile=Profile.query.filter_by(user_id=current_user.id).order_by(Profile.id.desc()).first())


@views.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            new_age = int(request.form.get('age'))
            new_occupation = request.form.get('occupation')
            new_country = request.form.get('country')
            new_gender = request.form.get('gender')
            new_relationship = request.form.get('relationship')
            new_struggles = request.form.get('struggles')

            if (new_age<0 or new_age>120):
                flash('Age not within range!', category='error')
            else:
                new_profile = Profile(age=new_age, gender=new_gender, occupation=new_occupation, country=new_country, relationship=new_relationship, struggles=new_struggles, user_id=current_user.id)
                db.session.add(new_profile)
                db.session.commit()
                flash('Profile Updated!', category='success')
                return redirect(url_for('views.profileview'))
        except:
            flash('Re-check your input(s)!', category='error')

    return render_template("profile.html", user=current_user)

@views.route('/delete-dream', methods=['POST'])
def delete_dream():
    data = json.loads(request.data)
    dreamId = data['dreamId']
    dream = Dream.query.get(dreamId)
    if dream:
        if dream.user_id == current_user.id:
            db.session.delete(dream)
            db.session.commit()
            return jsonify({})

@views.route('/viewdream', methods=['GET','POST'])
@login_required
def viewdream():
    if request.method == 'POST':
        try:
            new_ratings1 = 0
            new_ratings2=0
            if (request.form.get('star5_1')):
                new_ratings1 = 5
            elif (request.form.get('star4_1')):
                new_ratings1 = 4
            elif (request.form.get('star3_1')):
                new_ratings1 = 3
            elif (request.form.get('star2_1')):
                new_ratings1 = 2
            elif (request.form.get('star1_1')):
                new_ratings1 = 1

            if (request.form.get('star5_2')):
                new_ratings2 = 5
            elif (request.form.get('star4_2')):
                new_ratings2 = 4
            elif (request.form.get('star3_2')):
                new_ratings2 = 3
            elif (request.form.get('star2_2')):
                new_ratings2 = 2
            elif (request.form.get('star1_2')):
                new_ratings2 = 1

            if (new_ratings1==0 or new_ratings2==0):
                flash('Give a minimum of 1 star!', category='error')
                return redirect(url_for('views.viewdream'))
            else:
                dream=Dream.query.filter_by(user_id=current_user.id).order_by(Dream.id.desc()).first()
                dream.rating1 = new_ratings1
                dream.rating2 = new_ratings2
                db.session.commit()
        except:
            flash('Error in input selection!', category='error')

        return redirect(url_for('views.home'))

    return render_template("viewdream.html", user=current_user, dream=Dream.query.filter_by(user_id=current_user.id).order_by(Dream.id.desc()).first())

@views.route('/privacy', methods=['GET','POST'])
def privacy():
    return render_template("privacy.html", user=current_user)

@views.route('/downloadaloha12', methods=['GET'])
def download():
    return render_template("downloadaloha12.html", user=current_user)