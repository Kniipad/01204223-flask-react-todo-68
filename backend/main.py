from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    comments = db.relationship(
        "Comment",
        backref="todo",
        cascade="all, delete",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": False,
            "comments": [c.to_dict() for c in self.comments]
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300), nullable=False)

    todo_id = db.Column(
        db.Integer,
        db.ForeignKey("todo.id"),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "todo_id": self.todo_id
        }


@app.route("/api/todos/<int:todo_id>/comments/", methods=["POST"])
def add_comment(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Comment message is required"}), 400

    comment = Comment(
        message=data["message"],
        todo=todo
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


# ---------- Models ----------
@app.route("/api/todos/<int:todo_id>/toggle/", methods=["PATCH"])
def toggle_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return jsonify(todo.to_dict())


@app.route("/")
def hello():
    return "Flask backend is running"


if __name__ == "__main__":
    app.run(debug=True)
