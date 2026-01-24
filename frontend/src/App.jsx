import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const TODOLIST_API_URL = 'http://localhost:5000/api/todos/';

  const [todoList, setTodoList] = useState([]);
  const [newTitle, setNewTitle] = useState("");
  // newComments จะเก็บ object ในรูปแบบ { todo_id: "ข้อความ", ... }
  const [newComments, setNewComments] = useState({});

  useEffect(() => {
    fetchTodoList();
  }, []);

  async function fetchTodoList() {
    try {
      const response = await fetch(TODOLIST_API_URL);
      if (!response.ok) {
        throw new Error('Network error');
      }
      const data = await response.json();
      setTodoList(data);
    } catch (err) {
      alert("Failed to fetch todo list. Make sure backend is running.");
      console.error(err);
    }
  }

  async function toggleDone(id) {
    const toggle_api_url = `${TODOLIST_API_URL}${id}/toggle/`
    try {
      const response = await fetch(toggle_api_url, {
        method: 'PATCH',
      })
      if (response.ok) {
        const updatedTodo = await response.json();
        // อัปเดต state โดยแทนที่ตัวเดิมด้วยตัวใหม่ที่ได้จาก server
        setTodoList(todoList.map(todo => todo.id === id ? updatedTodo : todo));
      }
    } catch (error) {
      console.error("Error toggling todo:", error);
    }
  }

  async function addNewTodo() {
    try {
      const response = await fetch(TODOLIST_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'title': newTitle }),
      });
      if (response.ok) {
        const newTodo = await response.json();
        // เพิ่ม todo ใหม่เข้าไปใน list และเคลียร์ช่อง input
        setTodoList([...todoList, newTodo]);
        setNewTitle("");
      }
    } catch (error) {
      console.error("Error adding new todo:", error);
    }
  }

  async function deleteTodo(id) {
    const delete_api_url = `${TODOLIST_API_URL}${id}/`
    try {
      const response = await fetch(delete_api_url, {
        method: 'DELETE',
      });
      if (response.ok) {
        setTodoList(todoList.filter(todo => todo.id !== id));
      }
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  }

 {
    try {
      const url = `${TODOLIST_API_URL}${todoId}/comments/`;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'message': newComments[todoId] || "" }),
      });
      
      if (response.ok) {
        setNewComments({ ...newComments, [todoId]: "" });
        await fetchTodoList();
      }
    } catch (error) {
      console.error("Error adding new comment:", error);
    }
  }

  return (
    <>
      <h1>Todo List</h1>
      <ul>
        {todoList.map(todo => (
          <li key={todo.id} style={{ marginBottom: '20px', borderBottom: '1px solid #ccc', paddingBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span 
                className={todo.done ? "done" : ""} 
                style={{ textDecoration: todo.done ? 'line-through' : 'none', flexGrow: 1 }}
              >
                {todo.title}
              </span>
              <button onClick={() => toggleDone(todo.id)}>
                {todo.done ? "Undo" : "Done"}
              </button>
              <button onClick={() => deleteTodo(todo.id)}>❌</button>
            </div>

            {/* ส่วนแสดง Comments */}
            {(todo.comments && todo.comments.length > 0) && (
              <div style={{ marginTop: '10px', marginLeft: '20px', fontSize: '0.9em' }}>
                <b>Comments:</b>
                <ul>
                  {todo.comments.map(comment => (
                    <li key={comment.id}>{comment.message}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* ส่วนฟอร์มเพิ่ม Comment */}
            <div className="new-comment-forms" style={{ marginTop: '10px', marginLeft: '20px' }}>
              <input
                type="text"
                placeholder="Add a comment..."
                value={newComments[todo.id] || ""}
                onChange={(e) => {
                  const value = e.target.value;
                  // อัปเดต state เฉพาะ key ของ todo ตัวนี้
                  setNewComments({ ...newComments, [todo.id]: value });
                }}
              />
              <button onClick={() => addNewComment(todo.id)}>Add Comment</button>
            </div>
          </li>
        ))}
      </ul>

      <div style={{ marginTop: '20px', borderTop: '2px solid black', paddingTop: '10px' }}>
        <h3>New Task</h3>
        <input 
          type="text" 
          placeholder="New task title..."
          value={newTitle} 
          onChange={(e) => setNewTitle(e.target.value)} 
        />
        <button onClick={addNewTodo}>Add Task</button>
      </div>
    </>
  )
}

export default App