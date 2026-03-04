from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    JWTManager,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt
import click
import os

from backend.models import db, TodoItem, Comment, User

# -------------------------
# App Setup
# -------------------------

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:///todos.db'
)
app.config['JWT_SECRET_KEY'] = os.getenv(
    'JWT_SECRET_KEY',
    'fdslkfjsdlkufewhjroiewurewrew'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)


# -------------------------
# Routes
# -------------------------

@app.route('/api/todos/', methods=['GET'])
@jwt_required()
def get_todos():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first_or_404()

    todos = TodoItem.query.filter_by(user_id=user.id).all()

    return jsonify([todo.to_dict() for todo in todos])


@app.route('/api/todos/', methods=['POST'])
@jwt_required()
def add_todo():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first_or_404()

    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Invalid todo data'}), 400

    todo = TodoItem(
        title=data['title'],
        done=data.get('done', False),
        user_id=user.id
    )

    db.session.add(todo)
    db.session.commit()

    return jsonify(todo.to_dict()), 201


@app.route('/api/todos/<int:id>/toggle/', methods=['PATCH'])
@jwt_required()
def toggle_todo(id):
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first_or_404()

    todo = TodoItem.query.filter_by(
        id=id,
        user_id=user.id
    ).first_or_404()

    todo.done = not todo.done
    db.session.commit()

    return jsonify(todo.to_dict())


@app.route('/api/todos/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first_or_404()

    todo = TodoItem.query.filter_by(
        id=id,
        user_id=user.id
    ).first_or_404()

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': 'Todo deleted successfully'})


@app.route('/api/todos/<int:todo_id>/comments/', methods=['POST'])
@jwt_required()
def add_comment(todo_id):
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first_or_404()

    todo_item = TodoItem.query.filter_by(
        id=todo_id,
        user_id=user.id
    ).first_or_404()

    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': 'Comment message is required'}), 400

    comment = Comment(
        message=data['message'],
        todo_id=todo_item.id
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


# -------------------------
# Login
# -------------------------

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


# -------------------------
# CLI
# -------------------------

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


# -------------------------
# Run (local only)
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)