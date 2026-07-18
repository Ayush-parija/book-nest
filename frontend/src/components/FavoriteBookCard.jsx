import { toggleFavorite } from "../services/bookService";

function FavoriteBookCard({ book, refreshFavorites }) {
  const handleRemoveFavorite = async () => {
    try {
      await toggleFavorite(book.id);
      refreshFavorites();
    } catch (error) {
      console.error(error);
      alert("Failed to remove favorite.");
    }
  };

  const formatDate = (date) => {
    if (!date) return "N/A";
    return new Date(date).toLocaleDateString();
  };

  return (
    <div
      className="card shadow-lg mb-4 border-0"
      style={{
        backgroundColor: "#1e1e1e",
        color: "#ffffff",
        borderRadius: "15px",
      }}
    >
      <div className="card-body">

        <div className="d-flex justify-content-between align-items-center mb-3">

          <h3 className="mb-0 text-primary">
            📚 {book.title}
          </h3>

          <span className="badge bg-warning text-dark">
            ⭐ Favorite
          </span>

        </div>

        <hr className="border-secondary" />

        <div className="row">

          <div className="col-md-6">
            <p>
              <strong>Author:</strong> {book.author}
            </p>

            <p>
              <strong>Status:</strong>{" "}
              <span className="badge bg-info">
                {book.status}
              </span>
            </p>

            <p>
              <strong>Total Pages:</strong>{" "}
              {book.total_pages ?? "N/A"}
            </p>

            <p>
              <strong>Current Page:</strong>{" "}
              {book.current_page ?? 0}
            </p>
          </div>

          <div className="col-md-6">
            <p>
              <strong>Rating:</strong>{" "}
              {book.rating
                ? `⭐ ${book.rating}/5`
                : "Not Rated"}
            </p>

            <p>
              <strong>Added:</strong>{" "}
              {formatDate(book.created_at)}
            </p>

            <p>
              <strong>Finished:</strong>{" "}
              {formatDate(book.finished_at)}
            </p>
          </div>

        </div>

        {book.notes && (
          <>
            <hr className="border-secondary" />

            <p>
              <strong>Notes</strong>
            </p>

            <div
              className="p-3 rounded"
              style={{
                background: "#2b2b2b",
              }}
            >
              {book.notes}
            </div>
          </>
        )}

        <div className="mt-4">

          <button
            className="btn btn-danger"
            onClick={handleRemoveFavorite}
          >
            ⭐ Remove Favorite
          </button>

        </div>

      </div>
    </div>
  );
}

export default FavoriteBookCard;