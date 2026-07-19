import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ShelfCard from "../components/ShelfCard";
import { getShelves, getSharedShelves } from "../services/shelfService";

// Displays the user's shelves along with shelves shared by other users
function Shelves() {
  // Store the user's shelves
  const [shelves, setShelves] = useState([]);

  // Store shelves shared with the user
  const [sharedShelves, setSharedShelves] = useState([]);

  // Track loading state
  const [loading, setLoading] = useState(true);

  // Fetch both personal and shared shelves
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

      // Handle different response formats for personal shelves
      if (Array.isArray(myShelvesData)) {
        setShelves(myShelvesData);
      } else if (myShelvesData && Array.isArray(myShelvesData.items)) {
        setShelves(myShelvesData.items);
      } else {
        setShelves([]);
      }

      // Store shared shelves if available
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

      // Reset state if loading fails
      setShelves([]);
      setSharedShelves([]);
    } finally {
      // Stop the loading indicator
      setLoading(false);
    }
  };

  // Load shelves when the page is opened
  useEffect(() => {
    fetchShelves();
  }, []);

  // Display a loading spinner while data is being fetched
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

        {/* Page heading */}
        <h2 className="text-white">📚 My Shelves</h2>

        {/* Navigate to the create shelf page */}
        <Link to="/shelves/add" className="btn btn-primary">
          + Create Shelf
        </Link>

      </div>

      {/* Display the user's shelves */}
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

      {/* Shared shelves section */}
      <h2 className="text-white mt-5 mb-4">👥 Shared With Me</h2>

      {/* Display shelves shared with the current user */}
      {sharedShelves.length === 0 ? (
        <div className="alert alert-info">No shelves have been shared with you yet.</div>
      ) : (
        <div className="row">
          {sharedShelves.map((shelf) => (
            <div key={`shared-${shelf.id}`} className="col-md-6 col-lg-4 mb-4">
              <ShelfCard
                shelf={shelf}
                isShared={true}
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