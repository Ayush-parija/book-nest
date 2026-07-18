import React from "react";

function BookCard({ book }) {
  if (!book) return null;

  const formatDate = (date) => {
    if (!date) return "N/A";
    return new Date(date).toLocaleDateString();
  };

  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">

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

        <p className="mb-2">
          <strong>Author:</strong> {book.author}
        </p>

        <p className="mb-2">
          <strong>Status:</strong>{" "}
          <span className="badge bg-primary">
            {book.status}
          </span>
        </p>

        <p className="mb-2">
          <strong>Total Pages:</strong>{" "}
          {book.total_pages ?? "N/A"}
        </p>

        <p className="mb-2">
          <strong>Current Page:</strong>{" "}
          {book.current_page ?? 0}
        </p>

        <p className="mb-2">
          <strong>Rating:</strong>{" "}
          {book.rating ? `⭐ ${book.rating}/5` : "No Rating"}
        </p>

        {book.notes && (
          <div className="mb-2">
            <strong>Notes:</strong>
            <p className="text-muted mb-0">
              {book.notes}
            </p>
          </div>
        )}

        <hr />

        <small className="text-muted d-block">
          <strong>Added:</strong>{" "}
          {formatDate(book.created_at)}
        </small>

        <small className="text-muted d-block">
          <strong>Finished:</strong>{" "}
          {formatDate(book.finished_at)}
        </small>

      </div>
    </div>
  );
}

export default BookCard;