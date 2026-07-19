import api from "../api/axios";

// Service for retrieving dashboard summary data

// Fetch dashboard statistics and overview information
export const getDashboard = async () => {
  const response = await api.get("/dashboard");
  return response.data;
};