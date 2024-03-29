from flask import render_template, flash, redirect, url_for, session, request, Flask
from app import app
from app.forms import TranslationForm
from app import db
from app.models import Line
import random as rd
from app.advancedsearch import find_phrases

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = TranslationForm()
    if form.validate_on_submit():
        t = form.radio.data
        q = 'cached'
        if t == 'normal':
            q = form.text.data
        session['search_text'] = form.text.data
        return redirect(url_for('search', t=t, q=q))
    return render_template('index.html', title='Library', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search = request.args.get('t')
    page = request.args.get('page', 1, type=int)
    #videoss = session['rows']
    if 'search_text' in session:
        mline = session['search_text']
        mline = str(mline).rstrip()
        if search == 'advanced':
            f = find_phrases(mline)
            matches = {}
            for phrase in f:
                results = Line.query.filter(Line.flavor.like('%{}%'.format(phrase))).paginate(
                    page, app.config['POSTS_PER_PAGE'], False).items
                matches[phrase] = results
                rlength = len(results)
            if len(matches) == 1:
                lines = Line.query.filter(Line.flavor.like('%{}%'.format(mline))).paginate(
                    page, app.config['POSTS_PER_PAGE'], False)

                next_url = url_for('search', page=lines.next_num) \
                    if lines.has_next else None
                prev_url = url_for('search', page=lines.prev_num) \
                    if lines.has_prev else None

                matches[mline] = lines.items
                return render_template('search.html', title='Results', matches=matches, next_url=next_url, prev_url=prev_url, page=page, rlength=rlength)
            else:
                return render_template('search.html', title='Results', results=results, matches=matches, page=page, rlength=rlength)
        else:
            mline = request.args.get('q')
            mline = str(mline).rstrip()
            q = mline
            t = request.args.get('t')
            results = Line.query.filter(
                Line.flavor.like('%{}%'.format(mline))).all()
            lines = Line.query.filter(Line.flavor.like('%{}%'.format(mline))).paginate(
                page, app.config['POSTS_PER_PAGE'], False)

            next_url = url_for('search', page=lines.next_num, t=t, q=q) \
                if lines.has_next else None
            prev_url = url_for('search', page=lines.prev_num,t=t, q=q) \
                if lines.has_prev else None
            matches = {}
            matches[mline] = lines.items
            rlength = len(results)
            return render_template('search.html', title='Results', matches=matches, next_url=next_url, prev_url=prev_url, page=page, rlength=rlength)
    else:
        mline = request.args.get('q')
        mline = str(mline).rstrip()
        q = mline
        t = request.args.get('t')
        if mline != '':
            results = Line.query.filter(
                Line.flavor.like('%{}%'.format(mline))).all()

            lines = Line.query.filter(Line.flavor.like('%{}%'.format(mline))).paginate(
                page, app.config['POSTS_PER_PAGE'], False)

            next_url = url_for('search', page=lines.next_num,t=t, q=q) \
                if lines.has_next else None
            prev_url = url_for('search', page=lines.prev_num,t=t, q=q) \
                if lines.has_prev else None
            matches = {}
            matches[mline] = lines.items
            rlength = len(results)
            return render_template('search.html', title='Results', matches=matches, next_url=next_url, prev_url=prev_url, page=page, rlength=rlength)
    return redirect(url_for('index'))


@app.route('/random')
def random():
    all_lines = Line.query.all()
    video = rd.choice(all_lines)
    return render_template('random.html', title='Random', video=video)


@app.route('/donate')
def donate():
    return render_template('donate.html', title='Donate')


@app.route('/pewdsays')
def pewdsays():
    return render_template('pewdsays.html', title='Pewdsays')


@app.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')


@app.route('/discord')
def discord():
    return render_template('discord.html', title='Pewdie & Cutie Official Discord', description='Join our official discord Pewdie & Cutie, the largest Pewdiepie Discord! With 24.000 members and counting, you can chat with fellow 9 year olds from across the globe!')
