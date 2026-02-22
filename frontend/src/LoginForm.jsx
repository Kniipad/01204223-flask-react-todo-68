import { useState } from "react";
import { useAuth } from "./context/AuthContext";
import { useNavigate } from "react-router-dom";

function LoginForm({ loginUrl }) {
  const navigate = useNavigate();
  const { login, username: loggedInUsername } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  async function handleLogin(e) {
    e.preventDefault();

    try {
      const response = await fetch(loginUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();

        login(username, data.access_token);

        // redirect ไปหน้า TodoList
        navigate("/");
      } else if (response.status === 401) {
        setErrorMessage("Invalid username or password");
      } else {
        setErrorMessage("Something went wrong");
      }
    } catch (error) {
      console.log("Error logging in:", error);
      setErrorMessage("Server error");
    }
  }

  return (
    <form onSubmit={handleLogin}>
      {errorMessage && <p>{errorMessage}</p>}

      <div>
        Username:
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>

      <div>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <button type="submit">Login</button>

      {loggedInUsername && (
        <p>User {loggedInUsername} is already logged in.</p>
      )}
    </form>
  );
}

export default LoginForm;