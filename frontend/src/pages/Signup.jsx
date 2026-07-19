import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signupUser } from "../services/authService";

// Registration page for creating a new user account
function Signup() {
  // Used for page navigation
  const navigate = useNavigate();

  // Store all signup form fields
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  // Store validation errors
  const [errors, setErrors] = useState({});

  // Track signup request state
  const [loading, setLoading] = useState(false);

  // Update form values as the user types
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  // Validate the signup form before submission
  const validate = () => {
    const newErrors = {};

    if (!form.name.trim()) {
      newErrors.name = "Name is required";
    }

    // Validate email format
    if (!form.email.trim()) {
      newErrors.email = "Email is required";
    } else if (
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(form.email)
    ) {
      newErrors.email = "Invalid email address";
    }

    // Ensure password meets the minimum length
    if (form.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    }

    // Verify that both password fields match
    if (form.password !== form.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  // Submit the signup request
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) return;

    try {
      setLoading(true);

      // Send user registration data to the backend
      await signupUser({
        name: form.name,
        email: form.email,
        password: form.password,
      });

      alert("Signup Successful!");

      // Redirect the user to the login page
      navigate("/");

      // If you have "/login" route, replace with:
      // navigate("/login");
    } catch (error) {
      console.error("Signup Error:", error);

      alert(
        error.response?.data?.detail ||
          "Signup failed"
      );
    } finally {
      // Reset the loading state
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: "450px" }}>

      {/* Page heading */}
      <h2 className="mb-4">Create Account</h2>

      {/* Signup form */}
      <form onSubmit={handleSubmit}>

        {/* Name input */}
        <div className="mb-3">
          <label>Name</label>
          <input
            type="text"
            className="form-control"
            name="name"
            value={form.name}
            onChange={handleChange}
          />
          <small className="text-danger">{errors.name}</small>
        </div>

        {/* Email input */}
        <div className="mb-3">
          <label>Email</label>
          <input
            type="email"
            className="form-control"
            name="email"
            value={form.email}
            onChange={handleChange}
          />
          <small className="text-danger">{errors.email}</small>
        </div>

        {/* Password input */}
        <div className="mb-3">
          <label>Password</label>
          <input
            type="password"
            className="form-control"
            name="password"
            value={form.password}
            onChange={handleChange}
          />
          <small className="text-danger">{errors.password}</small>
        </div>

        {/* Confirm password input */}
        <div className="mb-3">
          <label>Confirm Password</label>
          <input
            type="password"
            className="form-control"
            name="confirmPassword"
            value={form.confirmPassword}
            onChange={handleChange}
          />
          <small className="text-danger">
            {errors.confirmPassword}
          </small>
        </div>

        {/* Submit button */}
        <button
          type="submit"
          className="btn btn-primary w-100"
          disabled={loading}
        >
          {loading ? "Creating..." : "Sign Up"}
        </button>

      </form>

      {/* Link to the login page */}
      <p className="mt-3">
        Already have an account?{" "}
        <Link to="/">Login</Link>
      </p>
    </div>
  );
}

export default Signup;