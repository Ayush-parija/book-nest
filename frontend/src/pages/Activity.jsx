import { useEffect, useState } from "react";
import { getMyActivities } from "../services/activityService";

// Displays the logged-in user's activity history
function Activity() {
  // Store activity records
  const [activities, setActivities] = useState([]);

  // Track loading state
  const [loading, setLoading] = useState(true);

  // Fetch activity data from the backend
  const loadActivities = async () => {
    try {
      const data = await getMyActivities();
      setActivities(data);
    } catch (error) {
      console.error(error);
      alert(
        error.response?.data?.detail ||
        "Failed to load activities."
      );
    } finally {
      // Hide the loading spinner after the request completes
      setLoading(false);
    }
  };

  // Load activities when the page is opened
  useEffect(() => {
    loadActivities();
  }, []);

  // Show a loading spinner while fetching data
  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div className="spinner-border text-primary"></div>
      </div>
    );
  }

  return (
    <div className="container mt-4">

      {/* Page heading */}
      <h2 className="mb-4">
        📝 My Activity
      </h2>

      {/* Display a message if no activities are available */}
      {activities.length === 0 ? (
        <div className="alert alert-info">
          No activity found.
        </div>
      ) : (
        <div className="list-group">

          {/* Display each activity */}
          {activities.map((activity) => (
            <div
              key={activity.id}
              className="list-group-item shadow-sm mb-3 rounded"
            >
              <h5 className="mb-2 text-primary">
                {activity.action}
              </h5>

              <p className="mb-2">
                {activity.message}
              </p>

              {/* Show the activity creation date and time */}
              <small className="text-muted">
                {new Date(activity.created_at).toLocaleString()}
              </small>
            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default Activity;