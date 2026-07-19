import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  getBooks,
  deleteBook,
  toggleFavorite,
} from "../services/bookService";

// Displays the user's book collection with search, filter, sorting, and pagination
function Books() {
  // Store the list of books
  const [books, setBooks] = useState([]);

  // Track loading state
  const [loading, setLoading] = useState(true);

  // Search keyword
  const [search, setSearch] = useState("");

  // Selected book status filter
  const [status, setStatus] = useState("");

  // Selected sorting field
  const [sortBy, setSortBy] = useState("created_at");

  // Sorting order
  const [order, setOrder] = useState("desc");

  // Current page number
  const [page, setPage] = useState(1);

  // Number of books displayed per page
  const pageSize = 10;

  // Reload books whenever filters or pagination change
  useEffect(() => {
    loadBooks();
  }, [page, search, status, sortBy, order]);

  // Fetch books from the backend
  const loadBooks = async () => {
    try {
      setLoading(true);

      const data = await getBooks({
        page,
        page_size: pageSize,
        search: search || undefined,
        status: status || undefined,
        sort_by: sortBy,
        order,
      });

      setBooks(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load books");
    } finally {
      // Stop the loading indicator
      setLoading(false);
    }
  };

  // Delete a selected book
  const handleDelete = async (id) => {
    if (!window.confirm("Delete this book?")) return;

    try {
      await deleteBook(id);

      // Refresh the book list
      loadBooks();
    } catch (error) {
      console.error(error);
      alert("Delete failed");
    }
  };

  // Toggle the favorite status of a book
  const handleFavorite = async (id) => {
    try {
      await toggleFavorite(id);

      // Refresh the updated list
      loadBooks();
    } catch (error) {
      console.error(error);
      alert("Favorite update failed");
    }
  };

  return (
    <div className="container mt-4">

      <div className="d-flex justify-content-between align-items-center mb-4">

        {/* Page title */}
        <h2>📚 My Books</h2>

        {/* Navigate to the Add Book page */}
        <Link to="/books/add" className="btn btn-primary">
          + Add Book
        </Link>
      </div>

      {/* Search, filter, and sorting controls */}
      <div className="row mb-4">

        {/* Search by title or author */}
        <div className="col-md-4">
          <input
            className="form-control"
            placeholder="Search..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </div>

        {/* Filter books by reading status */}
        <div className="col-md-3">
          <select
            className="form-select"
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setPage(1);
            }}
          >
            <option value="">All Status</option>
            <option value="Want to Read">Want To Read</option>
            <option value="Reading">Reading</option>
            <option value="Finished">Finished</option>
          </select>
        </div>

        {/* Select the sorting field */}
        <div className="col-md-3">
          <select
            className="form-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="created_at">Created Date</option>
            <option value="title">Title</option>
            <option value="rating">Rating</option>
          </select>
        </div>

        {/* Toggle sorting order */}
        <div className="col-md-2">
          <button
            className="btn btn-outline-secondary w-100"
            onClick={() =>
              setOrder(order === "asc" ? "desc" : "asc")
            }
          >
            {order.toUpperCase()}
          </button>
        </div>

      </div>

      {/* Display loading state or book list */}
      {loading ? (
        <h4>Loading...</h4>
      ) : (
        <table className="table table-bordered table-hover">

          <thead className="table-dark">
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>Status</th>
              <th>Pages</th>
              <th>Rating</th>
              <th>Favorite</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            {/* Show a message if no books are available */}
            {books.length === 0 ? (
              <tr>
                <td colSpan="7" className="text-center">
                  No books found
                </td>
              </tr>
            ) : (
              // Display each book
              books.map((book) => (
                <tr key={book.id}>

                  <td>{book.title}</td>

                  <td>{book.author}</td>

                  <td>{book.status}</td>

                  <td>
                    {book.current_page ?? 0}/{book.total_pages ?? 0}
                  </td>

                  <td>
                    {book.rating ? `⭐ ${book.rating}` : "-"}
                  </td>

                  <td>
                    {/* Toggle favorite status */}
                    <button
                      className="btn btn-sm"
                      onClick={() => handleFavorite(book.id)}
                    >
                      {book.is_favorite ? "❤️" : "🤍"}
                    </button>
                  </td>

                  <td>

                    {/* Edit the selected book */}
                    <Link
                      to={`/books/edit/${book.id}`}
                      className="btn btn-warning btn-sm me-2"
                    >
                      Edit
                    </Link>

                    {/* Delete the selected book */}
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(book.id)}
                    >
                      Delete
                    </button>

                  </td>

                </tr>
              ))
            )}

          </tbody>

        </table>
      )}

      {/* Pagination controls */}
      <div className="d-flex justify-content-center">

        <button
          className="btn btn-outline-primary me-3"
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
        >
          Previous
        </button>

        <span className="align-self-center">
          Page {page}
        </span>

        <button
          className="btn btn-outline-primary ms-3"
          disabled={books.length < pageSize}
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>

      </div>

    </div>
  );
}

export default Books;