import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getBooks } from "../services/bookService";
import { addBookToShelf } from "../services/shelfService";

function AddBookToShelf() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [addingBookId, setAddingBookId] = useState(null);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      setLoading(true);

      const data = await getBooks();

      // Handle both array and paginated response
      if (Array.isArray(data)) {
        setBooks(data);
      } else if (Array.isArray(data.items)) {
        setBooks(data.items);
      } else {
        setBooks([]);
      }
    } catch (error) {
      console.error(error);
      alert("Failed to load books.");
    } finally {
      setLoading(false);
    }
  };

  const handleAddBook = async (bookId) => {
    try {
      setAddingBookId(bookId);

      await addBookToShelf(id, bookId);

      alert("Book added to shelf successfully!");

      navigate(`/shelves/${id}`);
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.detail ||
          "Failed to add book."
      );
    } finally {
      setAddingBookId(null);
    }
  };

  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div className="spinner-border text-primary"></div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>📚 Add Book to Shelf</h2>

        <button
          className="btn btn-secondary"
          onClick={() => navigate(`/shelves/${id}`)}
        >
          Back
        </button>
      </div>

      {books.length === 0 ? (
        <div className="alert alert-info">
          No books available.
        </div>
      ) : (
        <div className="row">
          {books.map((book) => (
            <div
              className="col-md-6 col-lg-4 mb-4"
              key={book.id}
            >
              <div className="card shadow-sm h-100">
                <div className="card-body">
                  <h5>{book.title}</h5>

                  <p className="text-muted">
                    {book.author}
                  </p>

                  <p>
                    <strong>Status:</strong> {book.status}
                  </p>

                  <button
                    className="btn btn-success w-100"
                    disabled={addingBookId === book.id}
                    onClick={() =>
                      handleAddBook(book.id)
                    }
                  >
                    {addingBookId === book.id
                      ? "Adding..."
                      : "Add to Shelf"}
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

export default AddBookToShelf;