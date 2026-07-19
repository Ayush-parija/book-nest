import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getBooks } from "../services/bookService";
import { lendBook } from "../services/lendingService";

// Form component for lending a book to another user
function LendingForm() {
  const navigate = useNavigate();

  // Store the list of available books
  const [books, setBooks] = useState([]);

  // Track form submission state
  const [loading, setLoading] = useState(false);

  // Store form input values
  const [formData, setFormData] = useState({
    book_id: "",
    borrower_email: "",
  });

  // Load books when the component is mounted
  useEffect(() => {
    fetchBooks();
  }, []);

  // Fetch available books from the backend
  const fetchBooks = async () => {
    try {
      const data = await getBooks();

      if (Array.isArray(data)) {
        setBooks(data);
      } else if (Array.isArray(data.items)) {
        setBooks(data.items);
      } else {
        setBooks([]);
      }
    } catch (error) {
      console.error("Error loading books:", error);
      alert("Failed to load books.");
    }
  };

  // Update form fields as the user enters data
  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  // Submit the lending request
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Ensure a book is selected
    if (!formData.book_id) {
      alert("Please select a book.");
      return;
    }

    // Validate borrower email
    if (!formData.borrower_email.trim()) {
      alert("Please enter borrower email.");
      return;
    }

    try {
      setLoading(true);

      // Send the lending request to the backend
      const response = await lendBook(
        Number(formData.book_id),
        {
          email: formData.borrower_email.trim(),
        }
      );

      console.log("Success:", response);

      alert("Book lent successfully!");

      // Redirect to the lent books page
      navigate("/lending/lent");
    } catch (error) {
      // Log detailed error information for debugging
      console.error("========== LENDING ERROR ==========");
      console.error("Full Error:", error);
      console.error("Response:", error.response);
      console.error("Status:", error.response?.status);
      console.error("Data:", error.response?.data);
      console.error("==================================");

      alert(
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Failed to lend book."
      );
    } finally {
      // Reset loading state
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <div
        className="card shadow-lg border-0"
        style={{
          background: "#1f1f1f",
          color: "#fff",
          borderRadius: "15px",
        }}
      >
        {/* Form header */}
        <div className="card-header bg-primary text-white">
          <h3 className="mb-0">📚 Lend a Book</h3>
        </div>

        <div className="card-body">
          <form onSubmit={handleSubmit}>

            {/* Book selection dropdown */}
            <div className="mb-3">
              <label className="form-label">
                Select Book
              </label>

              <select
                className="form-select"
                name="book_id"
                value={formData.book_id}
                onChange={handleChange}
              >
                <option value="">
                  -- Select Book --
                </option>

                {books.map((book) => (
                  <option
                    key={book.id}
                    value={book.id}
                  >
                    {book.title}
                  </option>
                ))}
              </select>
            </div>

            {/* Borrower email input */}
            <div className="mb-3">
              <label className="form-label">
                Borrower Email
              </label>

              <input
                type="email"
                className="form-control"
                name="borrower_email"
                placeholder="Enter borrower email"
                value={formData.borrower_email}
                onChange={handleChange}
              />
            </div>

            {/* Submit button */}
            <button
              type="submit"
              className="btn btn-success me-2"
              disabled={loading}
            >
              {loading ? "Lending..." : "Lend Book"}
            </button>

            {/* Cancel and return to lending page */}
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate("/lending")}
            >
              Cancel
            </button>

          </form>
        </div>
      </div>
    </div>
  );
}

export default LendingForm;