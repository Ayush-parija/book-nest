import axios from "axios";

// Create a reusable Axios instance for all API requests
const api = axios.create({
  // Backend API base URL
  baseURL: "http://127.0.0.1:8000",

  // Enable sending and receiving HttpOnly cookies
  withCredentials: true, // Required to send/receive HttpOnly cookies (refresh_token)
});

// ──────────────────────────────────────────────
// Request Interceptor: Attach access token
// ──────────────────────────────────────────────

// Attach the access token to every authenticated request
api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// ──────────────────────────────────────────────
// Response Interceptor: Transparent token refresh
// ──────────────────────────────────────────────

// Track whether a token refresh request is already in progress
let isRefreshing = false;

// Store requests waiting for a refreshed token
let failedQueue = [];

// Resolve or reject all queued requests after refresh completes
const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedQueue = [];
};

// Automatically refresh expired access tokens
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    // Retry requests only once for expired access tokens
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes("/auth/login") &&
      !originalRequest.url.includes("/auth/refresh")
    ) {

      // Queue additional requests while the token is being refreshed
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Request a new access token using the refresh token cookie
        const response = await api.post("/auth/refresh");

        const newAccessToken = response.data.access_token;

        // Store the refreshed access token
        sessionStorage.setItem("access_token", newAccessToken);

        // Update default authorization header
        api.defaults.headers.common["Authorization"] = `Bearer ${newAccessToken}`;

        // Resume all queued requests
        processQueue(null, newAccessToken);

        // Retry the original request
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);

      } catch (refreshError) {
        // Clear authentication data if token refresh fails
        processQueue(refreshError, null);

        sessionStorage.removeItem("access_token");

        // Redirect the user to the login page
        window.location.href = "/login";

        return Promise.reject(refreshError);

      } finally {
        // Reset the refresh state
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;