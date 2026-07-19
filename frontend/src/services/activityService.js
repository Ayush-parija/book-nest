import api from "../api/axios";

// Service for fetching activity-related data

// Fetch activities performed by the currently logged-in user
export const getMyActivities = async () => {
  const response = await api.get("/activity/me");
  return response.data;
};

// Fetch all activity records from the backend
export const getAllActivities = async () => {
  const response = await api.get("/activity");
  return response.data;
};