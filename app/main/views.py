from app.models import Category,Pitch,Comment
from flask import flash, render_template, request,redirect,url_for  
from app import db
from . import main
from .forms import PitchForm

from flask_login import current_user,login_required

@main.route('/')
def index():
    pitches=Pitch.query.order_by(Pitch.timestamp.asc()).all()
    categories=Category.query.all()
    comments=Comment.query.order_by(Comment.timestamp.asc()).all()
    return render_template("index.html",pitches=pitches,categories=categories,comments=comments)
@main.route('/post', methods=['GET', 'POST'])
@login_required

def pitch():
    categories=Category.query.all()

    title= request.args.get('title')
    content= request.args.get('content')
    category= request.args.get('cat_id')
    if title !=None and content !=None and category!=None:
        cat=Category.query.filter_by(id=int(category)).first()
        new_pitch=Pitch(title=title,content=content,user=current_user.id,votes=0,category=cat.id)
        db.session.add(new_pitch)

        db.session.commit()
        flash('Pitch created successfully!')
        return redirect(url_for('.index'))        
    return render_template("pitch.html",categories=categories)
@main.route('/category', methods=['GET', 'POST'])
@login_required

def category():
    name= request.args.get('name')
    # import pdb; pdb.set_trace()
    if name != None:
        new_category = Category(name=name)
        
        db.session.add(new_category)
        db.session.commit()
        flash('Category created successfully!')
        return redirect(url_for('.pitch'))


    return render_template("category.html")
@main.route('/upvote/<int:id>', methods=['GET', 'POST'])
@login_required
def upvote(id):
    pitch=Pitch.query.filter_by(id=id).first()
    pitch.votes+=1
    db.session.add(pitch)
    db.session.commit()
    return redirect(url_for('.index'))

@main.route('/downvote/<int:id>', methods=['GET', 'POST'])
@login_required
def downvote(id):
    pitch=Pitch.query.filter_by(id=id).first()
    pitch.votes-=1
    db.session.add(pitch)
    db.session.commit()
    return redirect(url_for('.index'))

@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    pitch=Pitch.query.filter_by(id=id).first()
    comment=request.args.get('comment')
    if comment!=None:
        new_comment=Comment(text=comment,pitch=id)
        db.session.add(new_comment)
        db.session.commit()
    return redirect(url_for('.index'))