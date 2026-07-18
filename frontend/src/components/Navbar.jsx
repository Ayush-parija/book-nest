import { useNavigate } from "react-router-dom";
import api from "../api/axios";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    if (window.confirm("Are you sure you want to logout?")) {
      try {
        // Clears the HttpOnly refresh_token cookie on the server
        await api.post("/auth/logout");
      } catch (_) {
        // Even if logout API fails, clear local state
      }

      sessionStorage.removeItem("access_token");
      import("../services/websocketService").then(m => m.default.disconnect());
      alert("Logout successful");
      navigate("/login");
    }
  };

  return (
    <nav
      className="navbar navbar-expand-lg navbar-dark bg-primary shadow"
    >
      <div className="container-fluid">

        <span
          className="navbar-brand fw-bold fs-3"
          style={{ cursor: "pointer", color: "red" }}
          onClick={() => navigate("/dashboard")}
        >
          📚 BookNest
        </span>

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