import { useNavigate } from "react-router-dom";
import api from "../api/axios";

// Top navigation bar displayed across the application
function Navbar() {
  const navigate = useNavigate();

  // Handle user logout
  const handleLogout = async () => {
    if (window.confirm("Are you sure you want to logout?")) {
      try {
        // Clears the HttpOnly refresh_token cookie on the server
        await api.post("/auth/logout");
      } catch (_) {
        // Even if logout API fails, clear local state
      }

      // Remove the stored access token
      sessionStorage.removeItem("access_token");

      // Close the active WebSocket connection
      import("../services/websocketService").then(m => m.default.disconnect());

      // Notify the user and redirect to the login page
      alert("Logout successful");
      navigate("/login");
    }
  };

  return (
    <nav
      className="navbar navbar-expand-lg navbar-dark bg-primary shadow"
    >
      <div className="container-fluid">

        {/* Application logo and dashboard navigation */}
        <span
          className="navbar-brand fw-bold fs-3"
          style={{ cursor: "pointer", color: "red" }}
          onClick={() => navigate("/dashboard")}
        >
          📚 BookNest
        </span>

        {/* Logout button */}
        <button
          className="btn btn-danger"
          onClick={handleLogout}
        >
          🚪 Logout
        </button>

      </div>
    </nav>
  );
}

export default Navbar;