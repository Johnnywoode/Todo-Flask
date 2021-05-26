from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import url_for;
from flask_sqlalchemy import SQLAlchemy;
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    completed = db.Column(db.Boolean)
    # created_at = db.Column(db.datetime.utc.now())

@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('views/index.html', todo_list=todo_list)

@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    completed = request.form.get("completed")
    new_todo = Todo(title=title, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)