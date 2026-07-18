import api from "../api/axios";

// Get current user's activities
export const getMyActivities = async () => {
  const response = await api.get("/activity/me");
  return response.data;
};

// Get all activities
export const getAllActivities = async () => {
  const response = await api.get("/activity");
  return response.data;
};