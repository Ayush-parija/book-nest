import { useEffect, useState } from "react";
import { getBooks, updateReadingProgress } from "../services/bookService";
import { Link } from "react-router-dom";

function ReadingProgress() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const data = await getBooks({ page_size: 100 });
      // Backend returns a plain list[BookResponse]
      if (Array.isArray(data)) {
        setBooks(data);
      } else if (Array.isArray(data?.items)) {
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

  useEffect(() => {
    fetchBooks();
  }, []);

  const handleProgressChange = async (bookId, currentPage) => {
    try {
      const updatedBook = await updateReadingProgress(bookId, {
        current_page: Number(currentPage),
      });
      // Use the full response from the backend so status & finished_at update
      setBooks(books.map(b =>
        b.id === bookId ? { ...b, ...updatedBook } : b
      ));

      if (updatedBook.status === "Finished") {
        alert(`🎉 Congratulations! You finished "${updatedBook.title}"!`);
      }
    } catch (error) {
      console.error(error);
      const detail = error.response?.data?.detail;
      const msg = typeof detail === "string"
        ? detail
        : Array.isArray(detail) ? detail[0]?.msg : "Failed to update progress.";
      alert(msg);
      // Revert local state on error
      fetchBooks();
    }
  };

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <h4>Loading...</h4>
      </div>
    );
  }

  const statusBadge = (status) => {
    const colors = {
      "Want to Read": "bg-warning text-dark",
      "Reading": "bg-info text-dark",
      "Finished": "bg-success",
    };
    return colors[status] || "bg-secondary";
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>📖 Reading Progress</h2>
        <Link to="/books" className="btn btn-outline-primary">
          Back to Books
        </Link>
      </div>

      {books.length === 0 ? (
        <div className="alert alert-info">No books available in your library.</div>
      ) : (
        <div className="row g-4">
          {books.map((book) => {
            const totalPages = book.total_pages || 0;
            const currentPage = book.current_page || 0;
            const percentage = totalPages > 0 ? Math.round((currentPage / totalPages) * 100) : 0;

            return (
              <div key={book.id} className="col-md-6 col-lg-4">
                <div className="card h-100 shadow-sm border-0" style={{ background: "#252525", color: "#fff" }}>
                  <div className="card-body">
                    <h5 className="card-title fw-bold text-primary text-truncate" title={book.title}>
                      {book.title}
                    </h5>
                    <h6 className="card-subtitle mb-2 text-muted">by {book.author}</h6>

                    <div className="mb-3">
                      <span className={`badge ${statusBadge(book.status)}`}>
                        {book.status}
                      </span>
                      {book.finished_at && (
                        <small className="text-muted ms-2">
                          ✅ Finished on {new Date(book.finished_at).toLocaleDateString()}
                        </small>
                      )}
                    </div>

                    <div className="mb-2 d-flex justify-content-between align-items-center">
                      <small>Progress: {currentPage} / {totalPages || '?'} pages</small>
                      <small className="fw-bold text-success">{percentage}%</small>
                    </div>

                    <div className="progress mb-4" style={{ height: "10px", backgroundColor: "#3a3a3a" }}>
                      <div 
                        className={`progress-bar ${percentage >= 100 ? 'bg-success' : 'bg-info'}`}
                        role="progressbar" 
                        style={{ width: `${percentage}%` }}
                        aria-valuenow={percentage} 
                        aria-valuemin="0" 
                        aria-valuemax="100"
                      ></div>
                    </div>

                    <div className="input-group">
                      <span className="input-group-text bg-dark text-light border-secondary">Update Page</span>
                      <input
                        type="number"
                        className="form-control bg-dark text-light border-secondary"
                        min="0"
                        max={totalPages || 9999}
                        value={currentPage}
                        onChange={(e) => {
                          const val = Math.min(e.target.value, totalPages || 9999);
                          setBooks(books.map(b => b.id === book.id ? { ...b, current_page: val } : b));
                        }}
                        onBlur={(e) => handleProgressChange(book.id, e.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default ReadingProgress;