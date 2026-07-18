import { NavLink } from "react-router-dom";

function Sidebar() {
  const linkStyle = ({ isActive }) => ({
    display: "block",
    padding: "12px 16px",
    color: isActive ? "#fff" : "#333",
    backgroundColor: isActive ? "#1976d2" : "transparent",
    textDecoration: "none",
    borderRadius: "5px",
    marginBottom: "8px",
    fontWeight: "500",
  });

  return (
    <div
      style={{
        width: "240px",
        minHeight: "100vh",
        backgroundColor: "#f5f5f5",
        padding: "20px",
        boxSizing: "border-box",
      }}
    >
      <h2 style={{ marginBottom: "25px" }}>📚 BookNest</h2>

      {/* Dashboard */}
      <NavLink to="/dashboard" style={linkStyle}>
        🏠 Dashboard
      </NavLink>

      {/* Books */}
      <NavLink to="/books" style={linkStyle}>
        📚 Books
      </NavLink>

      {/* Favorites */}
      <NavLink to="/favorites" style={linkStyle}>
        ⭐ Favorites
      </NavLink>

      {/* Reading Progress */}
      <NavLink to="/reading-progress" style={linkStyle}>
        📖 Reading Progress
      </NavLink>

      {/* Shelves */}
      <NavLink to="/shelves" style={linkStyle}>
        🗂 Shelves
      </NavLink>

      {/* ========================= */}
      {/* Lending */}
      {/* ========================= */}

      <NavLink to="/lending" style={linkStyle}>
        📦 Lending History
      </NavLink>

      <NavLink to="/lending/new" style={linkStyle}>
        ➕ Lend Book
      </NavLink>

      <NavLink to="/lending/borrowed" style={linkStyle}>
        📖 Borrowed Books
      </NavLink>

      <NavLink to="/lending/lent" style={linkStyle}>
        📚 Lent Books
      </NavLink>


      {/* Activity */}
      <NavLink to="/activity" style={linkStyle}>
        📝 Activity
      </NavLink>
    </div>
  );
}

export default Sidebar;