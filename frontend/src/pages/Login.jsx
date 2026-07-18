import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../services/authService";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const data = await loginUser(email, password);

      // access_token is stored in localStorage for request headers
      // refresh_token is stored as HttpOnly cookie automatically by the browser
      localStorage.setItem("access_token", data.access_token);

      navigate("/dashboard");
    } catch (error) {
      console.error(error);

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
        <div className="text-center mb-4">
          <h1
            style={{
              color: "#0d6efd",
              fontWeight: "bold",
              fontSize: "42px",
            }}
          >
            📚 BookNest
          </h1>

          <p style={{ color: "#bdbdbd" }}>
            Personal Library Management System
          </p>
        </div>

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

        <button
          className="btn btn-primary w-100"
          onClick={handleLogin}
        >
          Login
        </button>

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