from flask import Flask, render_template, request, redirect, url_for, session
import os
from typing import Callable
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Float: Callable


db = MySQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)


if not os.path.isfile('database/books-collection.db'):
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', book_list=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        db.session.add(
            Books(
                title=request.form['title'],
                author=request.form['author'],
                rating=request.form['rating'],
            )
        )
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    book_update = Books.query.get(id)
    if request.method == 'POST':
        book_update.rating = request.form['new_rating']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book_update=book_update)


if __name__ == "__main__":
    app.run(debug=True)

