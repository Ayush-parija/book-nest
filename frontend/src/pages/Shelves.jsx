import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ShelfCard from "../components/ShelfCard";
import { getShelves } from "../services/shelfService";

function Shelves() {
  const [shelves, setShelves] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchShelves = async () => {
    try {
      setLoading(true);

      const data = await getShelves();

      console.log("Shelves Response:", data);

      if (Array.isArray(data)) {
        setShelves(data);
      } else if (data && Array.isArray(data.items)) {
        setShelves(data.items);
      } else {
        setShelves([]);
      }
    } catch (error) {
      console.error("Load Shelves Error:", error);

      alert(
        error.response?.data?.detail ||
        "You don't have permission to access this shelf.."
      );

      setShelves([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchShelves();
  }, []);

  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div
          className="spinner-border text-primary"
          role="status"
        >
          <span className="visually-hidden">
            Loading...
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">

      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="text-white">📚 My Shelves</h2>

        <Link
          to="/shelves/add"
          className="btn btn-primary"
        >
          + Create Shelf
        </Link>
      </div>

      {shelves.length === 0 ? (
        <div className="alert alert-info">
          No shelves found.
        </div>
      ) : (
        <div className="row">
          {shelves.map((shelf) => (
            <div
              key={shelf.id}
              className="col-md-6 col-lg-4 mb-4"
            >
              <ShelfCard
                shelf={shelf}
                refreshShelves={fetchShelves}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Shelves;