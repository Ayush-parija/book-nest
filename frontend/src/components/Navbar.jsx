import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to logout?")) {
      localStorage.removeItem("token");
      localStorage.removeItem("refreshToken");

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
          style={{ cursor: "pointer" }}
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