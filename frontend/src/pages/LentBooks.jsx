import { useEffect, useState } from "react";
import { getLentBooks } from "../services/lendingService";

function LentBooks() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    loadLentBooks();
  }, []);

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
      <h2 className="text-white mb-4">📚 Lent Books</h2>

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
            {books.map((book) => (
              <tr key={book.id}>
                <td>{book.book_title}</td>
                <td>{book.borrower_email}</td>
                <td>
                  {new Date(book.lent_at).toLocaleDateString()}
                </td>
                <td>
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