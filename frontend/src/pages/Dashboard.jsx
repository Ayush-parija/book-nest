import { useEffect, useState } from "react";
import { getDashboard } from "../services/dashboardService";
import DashboardCard from "../components/DashboardCard";
import BookCard from "../components/BookCard";
import ShelfCard from "../components/ShelfCard";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const data = await getDashboard();
      setDashboard(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load dashboard.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <h3>Loading Dashboard...</h3>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger">{error}</div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h2 className="mb-4">
        Welcome, {dashboard.user.name} 👋
      </h2>

      <div className="row">

        <DashboardCard
          title="Total Books"
          value={dashboard.statistics.total_books}
        />

        <DashboardCard
          title="Want To Read"
          value={dashboard.statistics.want_to_read}
        />

        <DashboardCard
          title="Reading"
          value={dashboard.statistics.reading}
        />

        <DashboardCard
          title="Finished"
          value={dashboard.statistics.finished}
        />

        <DashboardCard
          title="Pages Read"
          value={dashboard.statistics.total_pages_read}
        />

        <DashboardCard
          title="Average Rating"
          value={dashboard.statistics.average_rating}
        />

      </div>

      <hr />

      <h3>📖 Currently Reading</h3>

      <div className="row">
        {dashboard.currently_reading.length === 0 ? (
          <p>No books found.</p>
        ) : (
          dashboard.currently_reading.map((book) => (
            <div className="col-md-4 mb-3" key={book.id}>
              <BookCard book={book} />
            </div>
          ))
        )}
      </div>

      <hr />

      <h3>⭐ Favorite Books</h3>

      <div className="row">
        {dashboard.favorite_books.length === 0 ? (
          <p>No favorite books.</p>
        ) : (
          dashboard.favorite_books.map((book) => (
            <div className="col-md-4 mb-3" key={book.id}>
              <BookCard book={book} />
            </div>
          ))
        )}
      </div>

      <hr />

      <h3>🕒 Recent Books</h3>

      <div className="row">
        {dashboard.recent_books.length === 0 ? (
          <p>No recent books.</p>
        ) : (
          dashboard.recent_books.map((book) => (
            <div className="col-md-4 mb-3" key={book.id}>
              <BookCard book={book} />
            </div>
          ))
        )}
      </div>

      <hr />

      <h3>📂 My Shelves</h3>

      <div className="row">
        {dashboard.shelves.length === 0 ? (
          <p>No shelves found.</p>
        ) : (
          dashboard.shelves.map((shelf) => (
            <div className="col-md-4 mb-3" key={shelf.id}>
              <ShelfCard shelf={shelf} />
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Dashboard;