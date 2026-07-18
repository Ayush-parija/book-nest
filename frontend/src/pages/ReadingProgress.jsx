import { useEffect, useState } from "react";
import { getBooks, updateReadingProgress } from "../services/bookService";
import { Link } from "react-router-dom";

function ReadingProgress() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      // Fetch books that the user wants to read or is currently reading
      // We'll fetch all books for now and filter locally for simplicity, 
      // or we can just show all of them as they did before.
      const data = await getBooks({ page_size: 100 }); 
      setBooks(data);
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
      await updateReadingProgress(bookId, {
        current_page: Number(currentPage),
      });
      // Optionally just update the local state instead of refetching all books
      // to avoid jumping inputs
      setBooks(books.map(b => 
        b.id === bookId ? { ...b, current_page: Number(currentPage) } : b
      ));
    } catch (error) {
      console.error(error);
      alert("Failed to update progress.");
    }
  };

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <h4>Loading...</h4>
      </div>
    );
  }

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
                    <h6 className="card-subtitle mb-3 text-muted">by {book.author}</h6>

                    <div className="mb-2 d-flex justify-content-between align-items-center">
                      <small>Progress: {currentPage} / {totalPages || '?'} pages</small>
                      <small className="fw-bold text-success">{percentage}%</small>
                    </div>

                    <div className="progress mb-4" style={{ height: "10px", backgroundColor: "#3a3a3a" }}>
                      <div 
                        className="progress-bar bg-success" 
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