from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Mapped, mapped_column
from flask_migrate import Migrate
from sqlalchemy import Integer, String, ForeignKey                            # เพิ่ม import Foreignkey
from sqlalchemy.orm import Mapped, mapped_column, relationship                # เพิ่ม import relatiohship
from models import TodoItem, Comment, db, User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import click

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

class Base(DeclarativeBase):
  pass

db.init_app(app)                                                     # แก้จาก db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)

app.config['JWT_SECRET_KEY'] = 'fdsjkfjioi2rjshr2345hrsh043j5oij5545'
jwt = JWTManager(app)

"""
class TodoItem(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(default=False)

    ##### เพิ่มส่วน relationship  ซึ่งตรงนี้จะไม่กระทบ schema database เลย (เพราะว่าไม่มีการ map ไปยังคอลัมน์ใดๆ)
    comments: Mapped[list["Comment"]] = relationship(back_populates="todo")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "comments": [
                comment.to_dict() for comment in self.comments
            ]
        }
"""
"""
class Comment(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(String(250))
    todo_id: Mapped[int] = mapped_column(ForeignKey('todo_item.id'))

    todo: Mapped["TodoItem"] = relationship(back_populates="comments")

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "todo_id": self.todo_id
        }
"""

with app.app_context():
    db.create_all()
"""
INITIAL_TODOS = [
    TodoItem(title='Learn Flask'),
    TodoItem(title='Build a Flask App'),
]

with app.app_context():
    if TodoItem.query.count() == 0:
         for item in INITIAL_TODOS:
             db.session.add(item)
         db.session.commit()
"""

todo_list = [
    { "id": 1,
      "title": 'Learn Flask',
      "done": True },
    { "id": 2,
      "title": 'Build a Flask App',
      "done": False },
]

@app.route('/api/todos/', methods=['GET'])
@jwt_required()
def get_todos():
    todos = TodoItem.query.all()
    return jsonify([todo.to_dict() for todo in todos])


def new_todo(data):
    return TodoItem(title=data['title'], 
                    done=data.get('done', False))


@app.route('/api/todos/', methods=['POST'])
def add_todo():
    data = request.get_json()
    todo = new_todo(data)
    if todo:
        db.session.add(todo)                       # บรรทัดที่ปรับใหม่
        db.session.commit()                        # บรรทัดที่ปรับใหม่ 
        return jsonify(todo.to_dict())             # บรรทัดที่ปรับใหม่
    else:
        # return http response code 400 for bad requests
        return (jsonify({'error': 'Invalid todo data'}), 400) 
    

@app.route('/api/todos/<int:id>/toggle/', methods=['PATCH'])
def toggle_todo(id):
    todo = TodoItem.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict())


@app.route('/api/todos/<int:id>/', methods=['DELETE'])
def delete_todo(id):
    todo = TodoItem.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

@app.route('/api/todos/<int:todo_id>/comments/', methods=['POST'])
def add_comment(todo_id):
    todo_item = TodoItem.query.get_or_404(todo_id)

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Comment message is required'}), 400

    comment = Comment(
        message=data['message'],
        todo_id=todo_item.id
    )
    db.session.add(comment)
    db.session.commit()
 
    return jsonify(comment.to_dict())


@app.route('/api/login/', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token)

@app.cli.command("create-user")
@click.argument("username")
@click.argument("full_name")
@click.argument("password")
def create_user(username, full_name, password):
    user = User.query.filter_by(username=username).first()
    if user:
        click.echo("User already exists.")
        return
    user = User(username=username, full_name=full_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"User {username} created successfully.")