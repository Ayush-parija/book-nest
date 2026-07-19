import { useState } from "react";

// Reusable form component for creating and editing shelves
function ShelfForm({
  initialData = {},
  onSubmit,
  loading = false,
  submitText = "Save Shelf",
}) {
  // Store the shelf name
  const [name, setName] = useState(initialData.name || "");

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    const shelfName = name.trim();

    // Validate that the shelf name is provided
    if (!shelfName) {
      alert("Shelf name is required.");
      return;
    }

    // Send the form data to the parent component
    onSubmit({
      name: shelfName,
    });
  };

  return (
    <form onSubmit={handleSubmit}>

      {/* Shelf name input */}
      <div className="mb-3">
        <label className="form-label">
          Shelf Name
        </label>

        <input
          type="text"
          className="form-control"
          placeholder="Enter shelf name"
          value={name}
          autoFocus
          maxLength={100}
          onChange={(e) => setName(e.target.value)}
          disabled={loading}
          required
        />
      </div>

      {/* Submit button */}
      <button
        type="submit"
        className="btn btn-primary"
        disabled={loading}
      >
        {loading ? "Saving..." : submitText}
      </button>

    </form>
  );
}

export default ShelfForm;