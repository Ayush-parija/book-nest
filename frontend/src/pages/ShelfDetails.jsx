import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import {
  getShelf,
  getShelfBooks,
  removeBookFromShelf,
  getShelfCollaborators,
  updateCollaboratorRole,
  removeCollaborator,
} from "../services/shelfService";
import { getCurrentUser } from "../services/authService";

// Displays shelf details, books, and collaborator management
function ShelfDetails() {
  // Get the shelf ID from the route
  const { id } = useParams();

  // Store shelf information
  const [shelf, setShelf] = useState(null);

  // Store books available in the shelf
  const [books, setBooks] = useState([]);

  // Store shelf collaborators
  const [collaborators, setCollaborators] = useState([]);

  // Store the currently logged-in user
  const [currentUser, setCurrentUser] = useState(null);

  // Track loading state
  const [loading, setLoading] = useState(true);

  // Load shelf details, books, collaborators, and current user
  const fetchShelf = async () => {
    try {
      setLoading(true);

      const shelfData = await getShelf(id);
      const booksData = await getShelfBooks(id);
      const user = await getCurrentUser();

      setShelf(shelfData);
      setBooks(Array.isArray(booksData) ? booksData : []);
      setCurrentUser(user);

      // Load collaborator information
      try {
        const collabData = await getShelfCollaborators(id);
        setCollaborators(Array.isArray(collabData) ? collabData : []);
      } catch (err) {
        console.error("Load Collaborators Error:", err);
      }
    } catch (error) {
      console.error("Load Shelf Error:", error);

      alert(
        error.response?.data?.detail ||
        "Failed to load shelf."
      );
    } finally {
      // Stop the loading indicator
      setLoading(false);
    }
  };

  // Load shelf data whenever the shelf ID changes
  useEffect(() => {
    fetchShelf();
  }, [id]);

  // Remove a book from the shelf
  const handleRemove = async (bookId) => {
    const confirmRemove = window.confirm(
      "Are you sure you want to remove this book from the shelf?"
    );

    if (!confirmRemove) return;

    try {
      await removeBookFromShelf(id, bookId);

      alert("Book removed successfully.");

      // Refresh shelf data
      fetchShelf();
    } catch (error) {
      console.error("Remove Book Error:", error);

      alert(
        error.response?.data?.detail ||
        "Failed to remove book."
      );
    }
  };

  // Update a collaborator's permission
  const handleRoleChange = async (collaboratorId, newRole) => {
    try {
      await updateCollaboratorRole(id, collaboratorId, newRole);

      alert("Role updated successfully.");

      // Refresh collaborator data
      fetchShelf();
    } catch (error) {
      console.error("Update Role Error:", error);

      const detail = error.response?.data?.detail;
      const msg = Array.isArray(detail) ? detail[0].msg : (detail || "Failed to update role.");

      alert(msg);
    }
  };

  // Remove a collaborator from the shelf
  const handleRemoveCollaborator = async (collaboratorId) => {
    if (!window.confirm("Are you sure you want to remove this collaborator?")) return;

    try {
      await removeCollaborator(id, collaboratorId);

      alert("Collaborator removed successfully.");

      // Refresh collaborator list
      fetchShelf();
    } catch (error) {
      console.error("Remove Collaborator Error:", error);

      const detail = error.response?.data?.detail;
      const msg = Array.isArray(detail) ? detail[0].msg : (detail || "Failed to remove collaborator.");

      alert(msg);
    }
  };

  // Display a loading spinner while data is being fetched
  if (loading) {
    return (
      <div className="container text-center mt-5">
        <div
          className="spinner-border text-primary"
          role="status"
        >
          <span className="visually-hidden">
            Loading...
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">

      <div className="d-flex justify-content-between align-items-center mb-4">

        {/* Shelf information */}
        <div>
          <h2 className="text-white">
            📚 {shelf?.name}
          </h2>

          <p className="text-light">
            {books.length} Book(s)
          </p>
        </div>

        {/* Shelf actions */}
        <div className="d-flex gap-2">

          <Link
            to={`/shelves/${id}/add-book`}
            className="btn btn-primary"
          >
            ➕ Add Book
          </Link>

          <Link
            to={`/shelves/${id}/share`}
            className="btn btn-success"
          >
            👥 Share Shelf
          </Link>

        </div>

      </div>

      {/* Collaborator management section */}
      {collaborators.length > 0 && (
        <div className="mb-4">
          <h4 className="text-white">Collaborators</h4>

          <ul className="list-group list-group-flush bg-transparent">

            {collaborators.map((collab) => (
              <li
                key={collab.id}
                className="list-group-item bg-dark text-white d-flex justify-content-between align-items-center mb-2"
                style={{ borderRadius: '8px' }}
              >
                <div>
                  <strong>{collab.name}</strong> ({collab.email})
                  <span className="badge bg-secondary ms-2">{collab.role}</span>
                </div>

                {/* Only the shelf owner can manage collaborators */}
                {currentUser?.id === shelf?.owner_id && (
                  <div className="d-flex gap-2">

                    <select
                      className="form-select form-select-sm"
                      value={collab.role}
                      onChange={(e) => handleRoleChange(collab.id, e.target.value)}
                      style={{ width: 'auto' }}
                    >
                      <option value="viewer">Viewer</option>
                      <option value="editor">Editor</option>
                    </select>

                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleRemoveCollaborator(collab.id)}
                    >
                      Remove
                    </button>

                  </div>
                )}

              </li>
            ))}

          </ul>
        </div>
      )}

      {/* Display a message if the shelf is empty */}
      {books.length === 0 ? (
        <div className="alert alert-info">
          No books found in this shelf.
        </div>
      ) : (
        <div className="row">

          {/* Display all books in the shelf */}
          {books.map((book) => (
            <div
              key={book.id}
              className="col-md-6 col-lg-4 mb-4"
            >
              <div
                className="card shadow-lg h-100 border-0"
                style={{
                  background: "#1f1f1f",
                  color: "#fff",
                  borderRadius: "15px",
                }}
              >
                <div className="card-body">

                  {/* Book title */}
                  <h4 className="text-primary">
                    📖 {book.title}
                  </h4>

                  <hr className="border-secondary" />

                  <p>
                    <strong>Author:</strong>{" "}
                    {book.author}
                  </p>

                  <p>
                    <strong>Status:</strong>{" "}
                    <span className="badge bg-info">
                      {book.status}
                    </span>
                  </p>

                  <p>
                    <strong>Progress:</strong>{" "}
                    {book.current_page || 0} /{" "}
                    {book.total_pages || 0}
                  </p>

                </div>

                <div
                  className="card-footer"
                  style={{
                    background: "#2b2b2b",
                    borderTop: "1px solid #444",
                  }}
                >
                  {/* Remove the selected book from the shelf */}
                  <button
                    className="btn btn-danger w-100"
                    onClick={() => handleRemove(book.id)}
                  >
                    🗑 Remove Book
                  </button>
                </div>

              </div>
            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default ShelfDetails;