import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

// Provides a common layout with navigation and page content
function Layout({ children }) {
  return (
    <>
      {/* Top navigation bar */}
      <Navbar />

      <div style={{ display: "flex" }}>

        {/* Sidebar navigation */}
        <Sidebar />

        {/* Main content area */}
        <main
          style={{
            flex: 1,
            padding: "20px",
          }}
        >
          {children}
        </main>

      </div>
    </>
  );
}

export default Layout;