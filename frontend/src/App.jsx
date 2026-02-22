import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import PrivateRoute from "./PrivateRoute";

import TodoList from "./TodoList";
import LoginForm from "./LoginForm";

import "./App.css";

function App() {
  const TODOLIST_API_URL = "http://localhost:5000/api/todos/";
  const LOGIN_API_URL = "http://localhost:5000/api/login/";

  const isTest = import.meta.env.MODE === "test";

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              isTest ? (
                <TodoList apiUrl={TODOLIST_API_URL} />
              ) : (
                <PrivateRoute>
                  <TodoList apiUrl={TODOLIST_API_URL} />
                </PrivateRoute>
              )
            }
          />

          <Route
            path="/login"
            element={<LoginForm loginUrl={LOGIN_API_URL} />}
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;