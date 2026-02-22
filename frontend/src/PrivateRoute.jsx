import { Navigate } from "react-router-dom";
import { useAuth } from "./context/AuthContext";

export default function PrivateRoute({ children }) {
  const { accessToken } = useAuth();

  if (accessToken)
    return children;
  else 
    return (
      <Navigate to="/login" replace />
    );
}