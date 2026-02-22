import { useState } from "react";

function TodoItem({
  todo,
  toggleDone = () => {},
  deleteTodo = () => {},
  addNewComment = () => {},
}) {
  const [newComment, setNewComment] = useState("");

  const commentCount = todo.comments ? todo.comments.length : 0;

  return (
    <li>
      <span className={todo.done ? "done" : ""}>
        {todo.title}
      </span>

      {" "}
      <button onClick={() => toggleDone(todo.id)}>
        Toggle
      </button>

      {" "}
      <button onClick={() => deleteTodo(todo.id)}>
        ❌
      </button>

      {/* ✅ แสดงจำนวน comment */}
      <div>{commentCount}</div>

      <ul>
        {commentCount > 0 ? (
          todo.comments.map((comment) => (
            <li key={comment.id}>
              {comment.message}
            </li>
          ))
        ) : (
          <li>No comments</li>
        )}
      </ul>

      <input
        type="text"
        value={newComment}
        onChange={(e) => setNewComment(e.target.value)}
      />

      <button
        onClick={() => {
          addNewComment(todo.id, newComment);
          setNewComment("");
        }}
      >
        Add Comment
      </button>
    </li>
  );
}

export default TodoItem;