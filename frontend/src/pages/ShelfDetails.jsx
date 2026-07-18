import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import {
  getShelf,
  getShelfBooks,
  removeBookFromShelf,
} from "../services/shelfService";

function ShelfDetails() {
  const { id } = useParams();

  const [shelf, setShelf] = useState(null);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchShelf = async () => {
    try {
      setLoading(true);

      const shelfData = await getShelf(id);
      const booksData = await getShelfBooks(id);

      setShelf(shelfData);
      setBooks(Array.isArray(booksData) ? booksData : []);
    } catch (error) {
      console.error("Load Shelf Error:", error);

      alert(
        error.response?.data?.detail ||
        "Failed to load shelf."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchShelf();
  }, [id]);

  const handleRemove = async (bookId) => {
    const confirmRemove = window.confirm(
      "Are you sure you want to remove this book from the shelf?"
    );

    if (!confirmRemove) return;

    try {
      await removeBookFromShelf(id, bookId);

      alert("Book removed successfully.");

      fetchShelf();
    } catch (error) {
      console.error("Remove Book Error:", error);

      alert(
        error.response?.data?.detail ||
        "Failed to remove book."
      );
    }
  };

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

        <div>
          <h2 className="text-white">
            📚 {shelf?.name}
          </h2>

          <p className="text-light">
            {books.length} Book(s)
          </p>
        </div>

        <div className="d-flex gap-2">

          <Link
            to={`/shelves/${id}/add-book`}
            className="btn btn-primary"
          >
            ➕ Add Book
          </Link>

          <Link
            to={`/shelves/${id}/share`}
            className="btn btn-success"
          >
            👥 Share Shelf
          </Link>

        </div>

      </div>

      {books.length === 0 ? (
        <div className="alert alert-info">
          No books found in this shelf.
        </div>
      ) : (
        <div className="row">

          {books.map((book) => (
            <div
              key={book.id}
              className="col-md-6 col-lg-4 mb-4"
            >
              <div
                className="card shadow-lg h-100 border-0"
                style={{
                  background: "#1f1f1f",
                  color: "#fff",
                  borderRadius: "15px",
                }}
              >
                <div className="card-body">

                  <h4 className="text-primary">
                    📖 {book.title}
                  </h4>

                  <hr className="border-secondary" />

                  <p>
                    <strong>Author:</strong>{" "}
                    {book.author}
                  </p>

                  <p>
                    <strong>Status:</strong>{" "}
                    <span className="badge bg-info">
                      {book.status}
                    </span>
                  </p>

                  <p>
                    <strong>Progress:</strong>{" "}
                    {book.current_page || 0} /{" "}
                    {book.total_pages || 0}
                  </p>

                </div>

                <div
                  className="card-footer"
                  style={{
                    background: "#2b2b2b",
                    borderTop: "1px solid #444",
                  }}
                >
                  <button
                    className="btn btn-danger w-100"
                    onClick={() => handleRemove(book.id)}
                  >
                    🗑 Remove Book
                  </button>
                </div>

              </div>
            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default ShelfDetails;