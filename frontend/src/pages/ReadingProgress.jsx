import { useEffect, useState } from "react";
import {
  getBooks,
  updateReadingProgress,
} from "../services/bookService";

function ReadingProgress() {
  const [books, setBooks] = useState([]);

  const fetchBooks = async () => {
    try {
      const data = await getBooks();
      setBooks(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load books.");
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleProgressChange = async (bookId, currentPage) => {
    try {
      await updateReadingProgress(bookId, {
        current_page: Number(currentPage),
      });

      fetchBooks();
    } catch (error) {
      console.error(error);
      alert("Failed to update progress.");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2>📖 Reading Progress</h2>

      {books.length === 0 ? (
        <p>No books available.</p>
      ) : (
        books.map((book) => {
          const totalPages = book.total_pages || 0;
          const currentPage = book.current_page || 0;

          const percentage =
            totalPages > 0
              ? Math.round((currentPage / totalPages) * 100)
              : 0;

          return (
            <div
              key={book.id}
              style={{
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "20px",
                marginBottom: "20px",
              }}
            >
              <h3>{book.title}</h3>

              <p>Author: {book.author}</p>

              <p>
                Progress: {currentPage} / {totalPages} pages
              </p>

              <progress
                value={currentPage}
                max={totalPages || 1}
                style={{
                  width: "100%",
                  height: "20px",
                }}
              />

              <p>{percentage}% Completed</p>

              <input
                type="number"
                min="0"
                max={totalPages}
                defaultValue={currentPage}
                onBlur={(e) =>
                  handleProgressChange(
                    book.id,
                    e.target.value
                  )
                }
                style={{
                  padding: "8px",
                  width: "120px",
                  marginTop: "10px",
                }}
              />
            </div>
          );
        })
      )}
    </div>
  );
}

export default ReadingProgress;import { useEffect, useState } from "react";
import {
  getBooks,
  updateReadingProgress,
} from "../services/bookService";

function ReadingProgress() {
  const [books, setBooks] = useState([]);

  const fetchBooks = async () => {
    try {
      const data = await getBooks();
      setBooks(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load books.");
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleProgressChange = async (bookId, currentPage) => {
    try {
      await updateReadingProgress(bookId, {
        current_page: Number(currentPage),
      });

      fetchBooks();
    } catch (error) {
      console.error(error);
      alert("Failed to update progress.");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2>📖 Reading Progress</h2>

      {books.length === 0 ? (
        <p>No books available.</p>
      ) : (
        books.map((book) => {
          const totalPages = book.total_pages || 0;
          const currentPage = book.current_page || 0;

          const percentage =
            totalPages > 0
              ? Math.round((currentPage / totalPages) * 100)
              : 0;

          return (
            <div
              key={book.id}
              style={{
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "20px",
                marginBottom: "20px",
              }}
            >
              <h3>{book.title}</h3>

              <p>Author: {book.author}</p>

              <p>
                Progress: {currentPage} / {totalPages} pages
              </p>

              <progress
                value={currentPage}
                max={totalPages || 1}
                style={{
                  width: "100%",
                  height: "20px",
                }}
              />

              <p>{percentage}% Completed</p>

              <input
                type="number"
                min="0"
                max={totalPages}
                defaultValue={currentPage}
                onBlur={(e) =>
                  handleProgressChange(
                    book.id,
                    e.target.value
                  )
                }
                style={{
                  padding: "8px",
                  width: "120px",
                  marginTop: "10px",
                }}
              />
            </div>
          );
        })
      )}
    </div>
  );
}

export default ReadingProgress;