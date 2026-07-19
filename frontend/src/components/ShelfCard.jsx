import { Link } from "react-router-dom";

// Displays a summary card for a shelf
function ShelfCard({ shelf, isShared }) {
  // Prevent rendering if shelf data is unavailable
  if (!shelf) return null;

  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">

        {/* Shelf name */}
        <h5 className="card-title">
          📚 {shelf.name}
        </h5>

        {/* Shelf identifier */}
        <p className="text-muted">
          Shelf ID: {shelf.id}
        </p>

        {/* Show sharing details for shared shelves */}
        {isShared ? (
          <>
            <p>
              <strong>Owner:</strong> {shelf.owner_name}
            </p>
            <p>
              <strong>Role:</strong>{" "}
              <span className="badge bg-info">
                {shelf.role}
              </span>
            </p>
          </>
        ) : (
          // Display the owner's ID for personal shelves
          <p>
            Owner ID: {shelf.owner_id}
          </p>
        )}

        {/* Navigate to the shelf details page */}
        <Link
          to={`/shelves/${shelf.id}`}
          className="btn btn-primary"
        >
          View Shelf
        </Link>

      </div>
    </div>
  );
}

export default ShelfCard;