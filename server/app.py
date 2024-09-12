#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    session['page_views'] = 0 if 'page_views' not in session else session['page_views']
    return jsonify({'page_views': session['page_views']}), 200

@app.route('/articles/<int:id>')
def show_article(id):
    session['page_views'] = session.get('page_views', 0) + 1
    if session['page_views'] <= 3:
        article = Article.query.filter_by(id=id).first()
        if article:
            # Return the article data at the top level of the response JSON
            article_data = {
                'id': article.id,
                'author': article.author,
                'title': article.title,
                'content': article.content,
                'preview': article.preview,
                'minutes_to_read': article.minutes_to_read,
                'date': article.date.isoformat()  # Convert datetime to ISO format
            }
            return jsonify(article_data), 200
        else:
            return {'error': 'Article not found'}, 404
    else:
        return {'message': 'Maximum pageview limit reached'}, 401


if __name__ == '__main__':
    app.run(port=5555)


# If this is the first request this user has made, set session['page_views'] to an initial value of 0.
# Hint: consider using a ternary operator to set this initial value!
# For every request to /articles/<int:id>, increment the value of session['page_views'] by 1.
# If the user has viewed 3 or fewer pages, render a JSON response with the article data.
# If the user has viewed more than 3 pages, render a JSON response including an error message {'message': 'Maximum pageview limit reached'}, and a status code of 401 unauthorized.
# An API endpoint at /clear is available to clear your session as needed.