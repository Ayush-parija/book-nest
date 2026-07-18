import api from "../api/axios";

const getAuthHeader = () => ({
  headers: {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
});

// Get current user's activities
export const getMyActivities = async () => {
  const response = await api.get(
    "/activity/me",
    getAuthHeader()
  );

  return response.data;
};

// Get all activities
export const getAllActivities = async () => {
  const response = await api.get(
    "/activity",
    getAuthHeader()
  );

  return response.data;
};