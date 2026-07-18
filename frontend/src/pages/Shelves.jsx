import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ShelfCard from "../components/ShelfCard";
import { getShelves, getSharedShelves } from "../services/shelfService";

function Shelves() {
  const [shelves, setShelves] = useState([]);
  const [sharedShelves, setSharedShelves] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchShelves = async () => {
    try {
      setLoading(true);

      const [myShelvesData, sharedShelvesData] = await Promise.all([
        getShelves(),
        getSharedShelves().catch((err) => {
          console.error("Failed to load shared shelves:", err);
          return [];
        }),
      ]);

      if (Array.isArray(myShelvesData)) {
        setShelves(myShelvesData);
      } else if (myShelvesData && Array.isArray(myShelvesData.items)) {
        setShelves(myShelvesData.items);
      } else {
        setShelves([]);
      }

      if (Array.isArray(sharedShelvesData)) {
        setSharedShelves(sharedShelvesData);
      } else {
        setSharedShelves([]);
      }
    } catch (error) {
      console.error("Load Shelves Error:", error);
      alert(
        error.response?.data?.detail ||
        "Failed to load shelves."
      );
      setShelves([]);
      setSharedShelves([]);
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
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="text-white">📚 My Shelves</h2>

        <Link to="/shelves/add" className="btn btn-primary">
          + Create Shelf
        </Link>
      </div>

      {shelves.length === 0 ? (
        <div className="alert alert-info">No shelves found.</div>
      ) : (
        <div className="row">
          {shelves.map((shelf) => (
            <div key={shelf.id} className="col-md-6 col-lg-4 mb-4">
              <ShelfCard shelf={shelf} refreshShelves={fetchShelves} />
            </div>
          ))}
        </div>
      )}

      <h2 className="text-white mt-5 mb-4">👥 Shared With Me</h2>
      {sharedShelves.length === 0 ? (
        <div className="alert alert-info">No shelves have been shared with you yet.</div>
      ) : (
        <div className="row">
          {sharedShelves.map((shelf) => (
            <div key={`shared-${shelf.id}`} className="col-md-6 col-lg-4 mb-4">
              <ShelfCard shelf={shelf} isShared={true} refreshShelves={fetchShelves} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Shelves;