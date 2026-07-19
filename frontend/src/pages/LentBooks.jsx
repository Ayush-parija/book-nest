import { useEffect, useState } from "react";
import { getLentBooks } from "../services/lendingService";

// Displays the list of books that the user has lent to others
function LentBooks() {
  // Store the list of lent books
  const [books, setBooks] = useState([]);

  // Load lent books when the page opens
  useEffect(() => {
    loadLentBooks();
  }, []);

  // Fetch lent books from the backend
  const loadLentBooks = async () => {
    try {
      const data = await getLentBooks();
      setBooks(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error(error);
      alert("Failed to load lent books.");
    }
  };

  return (
    <div className="container mt-4">

      {/* Page heading */}
      <h2 className="text-white mb-4">📚 Lent Books</h2>

      {/* Display a message if no lent books are available */}
      {books.length === 0 ? (
        <div className="alert alert-info">
          No lent books found.
        </div>
      ) : (
        <table className="table table-dark table-hover">

          <thead>
            <tr>
              <th>Book</th>
              <th>Borrower Email</th>
              <th>Lent Date</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>

            {/* Display each lent book */}
            {books.map((book) => (
              <tr key={book.id}>
                <td>{book.book_title}</td>
                <td>{book.borrower_email}</td>
                <td>
                  {new Date(book.lent_at).toLocaleDateString()}
                </td>
                <td>

                  {/* Show whether the book has been returned */}
                  {book.returned_at ? (
                    <span className="badge bg-success">
                      Returned
                    </span>
                  ) : (
                    <span className="badge bg-warning text-dark">
                      Borrowed
                    </span>
                  )}

                </td>
              </tr>
            ))}

          </tbody>

        </table>
      )}

    </div>
  );
}

export default LentBooks;