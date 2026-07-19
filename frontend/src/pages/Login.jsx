import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";

// Login page for existing users
function Login() {
  // Used for page navigation after successful login
  const navigate = useNavigate();

  // Store the user's email
  const [email, setEmail] = useState("");

  // Store the user's password
  const [password, setPassword] = useState("");

  // Authenticate the user
  const handleLogin = async () => {
    try {
      const data = await loginUser(email, password);

      // Store the access token for authenticated requests
      // This allows testing multiple users in different browser tabs
      sessionStorage.setItem("access_token", data.access_token);
      
      // Establish the WebSocket connection after login
      import("../services/websocketService").then(m => m.default.connect());

      // Redirect to the dashboard
      navigate("/dashboard");
    } catch (error) {
      console.error(error);

      // Display the appropriate login error
      if (error.response) {
        alert(error.response.data.detail || "Login Failed");
      } else {
        alert("Cannot connect to backend");
      }
    }
  };

  return (
    <div
      className="d-flex justify-content-center align-items-center"
      style={{
        minHeight: "100vh",
        background: "#000000",
      }}
    >
      <div
        className="card shadow-lg border-0"
        style={{
          width: "430px",
          borderRadius: "20px",
          backgroundColor: "#1e1e1e",
          color: "#ffffff",
          padding: "40px",
        }}
      >
        {/* Application title */}
        <div className="text-center mb-4">
          <h1
            style={{
              color: "red",
              fontWeight: "bold",
              fontSize: "42px",
            }}
          >
            📚 BookNest
          </h1>
        </div>

        {/* Email input */}
        <div className="mb-3">
          <label className="form-label">Email</label>

          <input
            type="email"
            className="form-control"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        {/* Password input */}
        <div className="mb-4">
          <label className="form-label">Password</label>

          <input
            type="password"
            className="form-control"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {/* Login button */}
        <button
          className="btn btn-primary w-100"
          onClick={handleLogin}
        >
          Login
        </button>

        {/* Link to the registration page */}
        <div className="text-center mt-4">
          <span style={{ color: "#bdbdbd" }}>
            Don't have an account?
          </span>{" "}
          <Link
            to="/signup"
            className="text-decoration-none fw-bold"
          >
            Create Account
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Login;