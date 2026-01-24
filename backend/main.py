from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

class TodoItem(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    done: Mapped[bool] = mapped_column(default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done
        }
with app.app_context():
    db.create_all()


todo_list = [
    { "id": 1,
      "title": 'Learn Flask',
      "done": True },
    { "id": 2,
      "title": 'Build a Flask App',
      "done": False },
]

@app.route('/api/todos/', methods=['GET'])
def get_todos():
    return jsonify(todo_list)

def new_todo(data):
    if len(todo_list) == 0:
        id = 1
    else:
        id = 1 + max([todo['id'] for todo in todo_list])

    if 'title' not in data:
        return None
    
    return {
        "id": id,
        "title": data['title'],
        "done": data.get('done', False),
    }

@app.route('/api/todos/', methods=['POST'])
def add_todo():
    data = request.get_json()
    todo = new_todo(data)
    if todo:
        todo_list.append(todo)
        return jsonify(todo)
    else:
        # return http response code 400 for bad requests
        return (jsonify({'error': 'Invalid todo data'}), 400)  
    

@app.route('/api/todos/<int:id>/toggle/', methods=['PATCH'])
def toggle_todo(id):
    todos = [todo for todo in todo_list if todo['id'] == id]
    if not todos:
        return (jsonify({'error': 'Todo not found'}), 404)
    todo = todos[0]
    todo['done'] = not todo['done']
    return jsonify(todo)


@app.route('/api/todos/<int:id>/', methods=['DELETE'])
def delete_todo(id):
    global todo_list
    todos = [todo for todo in todo_list if todo['id'] == id]
    if not todos:
        return (jsonify({'error': 'Todo not found'}), 404)
    todo_list = [todo for todo in todo_list if todo['id'] != id]
    return jsonify({'message': 'Todo deleted successfully'})
