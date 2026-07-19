import { useEffect, useState } from "react";

// Reusable form component for creating and editing books
function BookForm({ initialData = {}, onSubmit, buttonText }) {
  // Store the book title
  const [title, setTitle] = useState("");

  // Store the author name
  const [author, setAuthor] = useState("");

  // Store the reading status
  const [status, setStatus] = useState("Want to Read");

  // Store the total number of pages
  const [totalPages, setTotalPages] = useState("");

  // Store the user rating
  const [rating, setRating] = useState("");

  // Store additional notes
  const [notes, setNotes] = useState("");

  // Populate the form when editing an existing book
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title || "");
      setAuthor(initialData.author || "");
      setStatus(initialData.status || "Want to Read");
      setTotalPages(initialData.total_pages ?? "");
      setRating(initialData.rating ?? "");
      setNotes(initialData.notes || "");
    }
  }, [initialData]);

  // Submit the form data to the parent component
  const handleSubmit = (e) => {
    e.preventDefault();

    onSubmit({
      title: title.trim(),
      author: author.trim(),
      status,
      total_pages: totalPages === "" ? null : Number(totalPages),
      rating: rating === "" ? null : Number(rating),
      notes: notes.trim(),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="card shadow p-4">

      {/* Form heading */}
      <h2 className="mb-4 text-center">{buttonText}</h2>

      {/* Book title input */}
      <div className="mb-3">
        <label className="form-label">Book Title</label>
        <input
          type="text"
          className="form-control"
          placeholder="Enter book title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>

      {/* Author input */}
      <div className="mb-3">
        <label className="form-label">Author</label>
        <input
          type="text"
          className="form-control"
          placeholder="Enter author name"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          required
        />
      </div>

      {/* Reading status selector */}
      <div className="mb-3">
        <label className="form-label">Status</label>
        <select
          className="form-select"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          <option value="Want to Read">Want to Read</option>
          <option value="Reading">Reading</option>
          <option value="Finished">Finished</option>
        </select>
      </div>

      {/* Total pages input */}
      <div className="mb-3">
        <label className="form-label">Total Pages</label>
        <input
          type="number"
          className="form-control"
          placeholder="Total Pages"
          value={totalPages}
          onChange={(e) => setTotalPages(e.target.value)}
        />
      </div>

      {/* Rating input */}
      <div className="mb-3">
        <label className="form-label">Rating (1-5)</label>
        <input
          type="number"
          min="1"
          max="5"
          className="form-control"
          placeholder="Rating"
          value={rating}
          onChange={(e) => setRating(e.target.value)}
        />
      </div>

      {/* Notes input */}
      <div className="mb-3">
        <label className="form-label">Notes</label>
        <textarea
          className="form-control"
          rows="5"
          placeholder="Write your notes..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </div>

      {/* Submit button */}
      <button type="submit" className="btn btn-success">
        {buttonText}
      </button>

    </form>
  );
}

export default BookForm;