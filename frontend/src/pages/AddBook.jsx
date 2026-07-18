import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createBook } from "../services/bookService";

function AddBook() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    title: "",
    author: "",
    status: "Want to Read",
    total_pages: "",
    rating: "",
    notes: "",
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      alert("Title is required");
      return;
    }

    if (!formData.author.trim()) {
      alert("Author is required");
      return;
    }

    try {
      setLoading(true);

      await createBook({
        title: formData.title.trim(),
        author: formData.author.trim(),
        status: formData.status,
        total_pages: formData.total_pages
          ? Number(formData.total_pages)
          : null,
        rating: formData.rating
          ? Number(formData.rating)
          : null,
        notes: formData.notes.trim(),
      });

      alert("Book added successfully!");

      navigate("/books");
    } catch (error) {
      console.error(error);

      if (error.response) {
        alert(
          error.response.data?.detail
            ? JSON.stringify(error.response.data.detail, null, 2)
            : "Failed to add book."
        );
      } else {
        alert(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <div className="card shadow">
        <div className="card-header bg-primary text-white">
          <h3>Add New Book</h3>
        </div>

        <div className="card-body">
          <form onSubmit={handleSubmit}>

            <div className="mb-3">
              <label className="form-label">Title</label>
              <input
                type="text"
                className="form-control"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Author</label>
              <input
                type="text"
                className="form-control"
                name="author"
                value={formData.author}
                onChange={handleChange}
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Status</label>
              <select
                className="form-select"
                name="status"
                value={formData.status}
                onChange={handleChange}
              >
                <option value="Want to Read">Want to Read</option>
                <option value="Reading">Reading</option>
                <option value="Finished">Finished</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">Total Pages</label>
              <input
                type="number"
                className="form-control"
                name="total_pages"
                value={formData.total_pages}
                onChange={handleChange}
                min="1"
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Rating</label>
              <input
                type="number"
                className="form-control"
                name="rating"
                value={formData.rating}
                onChange={handleChange}
                min="1"
                max="5"
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Notes</label>
              <textarea
                className="form-control"
                rows="4"
                name="notes"
                value={formData.notes}
                onChange={handleChange}
              />
            </div>

            <button
              type="submit"
              className="btn btn-success me-2"
              disabled={loading}
            >
              {loading ? "Saving..." : "Save Book"}
            </button>

            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate("/books")}
            >
              Cancel
            </button>

          </form>
        </div>
      </div>
    </div>
  );
}

export default AddBook;