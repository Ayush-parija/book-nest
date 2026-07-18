import { useEffect, useState } from "react";

function BookForm({ initialData = {}, onSubmit, buttonText }) {
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [status, setStatus] = useState("Want to Read");
  const [totalPages, setTotalPages] = useState("");
  const [rating, setRating] = useState("");
  const [notes, setNotes] = useState("");

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
      <h2 className="mb-4 text-center">{buttonText}</h2>

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

      <button type="submit" className="btn btn-success">
        {buttonText}
      </button>
    </form>
  );
}

export default BookForm;