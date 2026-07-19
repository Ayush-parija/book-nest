import { useEffect, useState } from "react";
import { getBorrowedBooks } from "../services/lendingService";
import { useWebSocket } from "../components/WebSocketContext";

function BorrowedBooks() {
  const [books, setBooks] = useState([]);
  const { lastMessage } = useWebSocket();

  const loadBorrowedBooks = async () => {
    try {
      const data = await getBorrowedBooks();
      setBooks(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error(error);
      alert("Failed to load borrowed books.");
    }
  };

  useEffect(() => {
    loadBorrowedBooks();
  }, []);

  // Auto-refresh when a WebSocket message is received (lending/return events)
  useEffect(() => {
    if (lastMessage) {
      loadBorrowedBooks();
    }
  }, [lastMessage]);

  return (
    <div className="container mt-4">
      <h2 className="text-white mb-4">
        📖 Borrowed Books
      </h2>

      {books.length === 0 ? (
        <div className="alert alert-info">
          No borrowed books found.
        </div>
      ) : (
        <table className="table table-dark table-hover">
          <thead>
            <tr>
              <th>Book</th>
              <th>Author</th>
              <th>Owner</th>
              <th>Lent Date</th>
            </tr>
          </thead>

          <tbody>
            {books.map((book) => (
              <tr key={book.lending_id}>
                <td>{book.title}</td>
                <td>{book.author}</td>
                <td>{book.owner_name}</td>
                <td>
                  {new Date(book.lent_at).toLocaleDateString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default BorrowedBooks;