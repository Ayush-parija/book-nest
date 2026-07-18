import { useEffect, useState } from "react";
import { getMyActivities } from "../services/activityService";

function Activity() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

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
      setLoading(false);
    }
  };

  useEffect(() => {
    loadActivities();
  }, []);

  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div className="spinner-border text-primary"></div>
      </div>
    );
  }

  return (
    <div className="container mt-4">

      <h2 className="mb-4">
        📝 My Activity
      </h2>

      {activities.length === 0 ? (
        <div className="alert alert-info">
          No activity found.
        </div>
      ) : (
        <div className="list-group">

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