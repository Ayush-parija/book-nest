import api from "../api/axios";

// =======================
// Login
// =======================
export const loginUser = async (email, password) => {
    try {
        const formData = new URLSearchParams();

        formData.append("username", email);
        formData.append("password", password);

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
export const signupUser = async (userData) => {
    try {
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
export const getCurrentUser = async () => {
    try {
        const response = await api.get("/auth/me");
        return response.data;
    } catch (error) {
        console.error("GetCurrentUser Error:", error);
        throw error;
    }
};