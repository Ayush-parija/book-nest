import { useState } from "react";

function ShelfForm({
  initialData = {},
  onSubmit,
  loading = false,
  submitText = "Save Shelf",
}) {
  const [name, setName] = useState(initialData.name || "");

  const handleSubmit = (e) => {
    e.preventDefault();

    const shelfName = name.trim();

    if (!shelfName) {
      alert("Shelf name is required.");
      return;
    }

    onSubmit({
      name: shelfName,
    });
  };

  return (
    <form onSubmit={handleSubmit}>

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