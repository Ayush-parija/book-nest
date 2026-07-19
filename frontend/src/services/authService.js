import api from "../api/axios";

// Authentication service for user login, signup, and profile retrieval

// =======================
// Login
// =======================

// Authenticate a user with email and password
export const loginUser = async (email, password) => {
    try {
        // Create form data required by the authentication endpoint
        const formData = new URLSearchParams();

        formData.append("username", email);
        formData.append("password", password);

        // Send login request to the backend
        const response = await api.post(
            "/auth/login",
            formData,
            {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            }
        );

        return response.data;
    } catch (error) {
        console.error("Login Error:", error);
        throw error;
    }
};

// =======================
// Signup
// =======================

// Register a new user account
export const signupUser = async (userData) => {
    try {
        // Send registration details to the backend
        const response = await api.post(
            "/auth/signup",
            userData
        );

        return response.data;
    } catch (error) {
        console.error("Signup Error:", error);
        throw error;
    }
};

// =======================
// Get Current User
// =======================

// Retrieve the currently authenticated user's profile
export const getCurrentUser = async () => {
    try {
        const response = await api.get("/auth/me");
        return response.data;
    } catch (error) {
        console.error("GetCurrentUser Error:", error);
        throw error;
    }
};