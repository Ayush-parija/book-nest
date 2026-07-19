import { NavLink } from "react-router-dom";

// Sidebar navigation for accessing different sections of the application
function Sidebar() {
  // Apply styles based on the active navigation link
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
      {/* Application title */}
      <h2 style={{ marginBottom: "25px", color: "red" }}>📚 BookNest</h2>

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

      {/* Lending History */}
      <NavLink to="/lending" style={linkStyle}>
        📦 Lending History
      </NavLink>

      {/* Lend a new book */}
      <NavLink to="/lending/new" style={linkStyle}>
        ➕ Lend Book
      </NavLink>

      {/* Borrowed books */}
      <NavLink to="/lending/borrowed" style={linkStyle}>
        📖 Borrowed Books
      </NavLink>

      {/* Lent books */}
      <NavLink to="/lending/lent" style={linkStyle}>
        📚 Lent Books
      </NavLink>

      {/* Activity log */}
      <NavLink to="/activity" style={linkStyle}>
        📝 Activity
      </NavLink>
    </div>
  );
}

export default Sidebar;