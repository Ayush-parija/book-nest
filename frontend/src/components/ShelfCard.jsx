import { Link } from "react-router-dom";

function ShelfCard({ shelf }) {
  if (!shelf) return null;

  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">

        <h5 className="card-title">
          📚 {shelf.name}
        </h5>

        <p className="text-muted">
          Shelf ID: {shelf.id}
        </p>

        <p>
          Owner ID: {shelf.owner_id}
        </p>

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