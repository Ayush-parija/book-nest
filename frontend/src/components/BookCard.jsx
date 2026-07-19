import React from "react";

// Displays book information in a reusable card component
function BookCard({ book }) {
  // Prevent rendering if no book data is provided
  if (!book) return null;

  // Format dates into a readable format
  const formatDate = (date) => {
    if (!date) return "N/A";
    return new Date(date).toLocaleDateString();
  };

  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">

        {/* Book title and favorite badge */}
        <div className="d-flex justify-content-between align-items-center">
          <h5 className="card-title mb-0">
            {book.title}
          </h5>

          {book.is_favorite && (
            <span className="badge bg-warning text-dark">
              ⭐ Favorite
            </span>
          )}
        </div>

        <hr />

        {/* Book author */}
        <p className="mb-2">
          <strong>Author:</strong> {book.author}
        </p>

        {/* Reading status */}
        <p className="mb-2">
          <strong>Status:</strong>{" "}
          <span className="badge bg-primary">
            {book.status}
          </span>
        </p>

        {/* Total number of pages */}
        <p className="mb-2">
          <strong>Total Pages:</strong>{" "}
          {book.total_pages ?? "N/A"}
        </p>

        {/* Current reading progress */}
        <p className="mb-2">
          <strong>Current Page:</strong>{" "}
          {book.current_page ?? 0}
        </p>

        {/* User rating */}
        <p className="mb-2">
          <strong>Rating:</strong>{" "}
          {book.rating ? `⭐ ${book.rating}/5` : "No Rating"}
        </p>

        {/* Display notes if available */}
        {book.notes && (
          <div className="mb-2">
            <strong>Notes:</strong>
            <p className="text-muted mb-0">
              {book.notes}
            </p>
          </div>
        )}

        <hr />

        {/* Book creation date */}
        <small className="text-muted d-block">
          <strong>Added:</strong>{" "}
          {formatDate(book.created_at)}
        </small>

        {/* Book completion date */}
        <small className="text-muted d-block">
          <strong>Finished:</strong>{" "}
          {formatDate(book.finished_at)}
        </small>

      </div>
    </div>
  );
}

export default BookCard;