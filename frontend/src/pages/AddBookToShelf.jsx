import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getBooks } from "../services/bookService";
import { addBookToShelf } from "../services/shelfService";

// Page for adding an existing book to a selected shelf
function AddBookToShelf() {
  // Get the shelf ID from the URL
  const { id } = useParams();
  const navigate = useNavigate();

  // Store the list of available books
  const [books, setBooks] = useState([]);

  // Track page loading state
  const [loading, setLoading] = useState(true);

  // Track the book currently being added
  const [addingBookId, setAddingBookId] = useState(null);

  // Load books when the page is opened
  useEffect(() => {
    fetchBooks();
  }, []);

  // Fetch all available books
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
      // Stop the loading indicator
      setLoading(false);
    }
  };

  // Add the selected book to the current shelf
  const handleAddBook = async (bookId) => {
    try {
      setAddingBookId(bookId);

      await addBookToShelf(id, bookId);

      alert("Book added to shelf successfully!");

      // Return to the shelf details page
      navigate(`/shelves/${id}`);
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.detail ||
          "Failed to add book."
      );
    } finally {
      // Reset the button loading state
      setAddingBookId(null);
    }
  };

  // Show a loading spinner while fetching books
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

        {/* Page title */}
        <h2>📚 Add Book to Shelf</h2>

        {/* Navigate back to the shelf details */}
        <button
          className="btn btn-secondary"
          onClick={() => navigate(`/shelves/${id}`)}
        >
          Back
        </button>
      </div>

      {/* Display a message if no books are available */}
      {books.length === 0 ? (
        <div className="alert alert-info">
          No books available.
        </div>
      ) : (
        <div className="row">

          {/* Display each available book */}
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

                  {/* Add the selected book to the shelf */}
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