import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { shareShelf } from "../services/shelfService";

// Page for sharing a shelf with another user
function ShareShelf() {
  // Get the shelf ID from the route
  const { id } = useParams();

  // Used for page navigation
  const navigate = useNavigate();

  // Store the recipient's email
  const [email, setEmail] = useState("");

  // Store the selected permission level
  const [role, setRole] = useState("viewer");

  // Track the sharing request state
  const [loading, setLoading] = useState(false);

  // Share the selected shelf with another user
  const handleShare = async (e) => {
    e.preventDefault();

    // Validate that an email has been entered
    if (!email.trim()) {
      alert("Please enter an email address.");
      return;
    }

    try {
      setLoading(true);

      // Send the sharing request to the backend
      await shareShelf(id, {
        email: email.trim(),
        role,
      });

      alert("Shelf shared successfully!");

      // Return to the shelf details page
      navigate(`/shelves/${id}`);
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.detail ||
          "Failed to share shelf."
      );
    } finally {
      // Reset the loading state
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">

      <div className="row justify-content-center">

        <div className="col-md-6">

          <div className="card shadow">

            {/* Page header */}
            <div className="card-header bg-success text-white">
              <h3 className="mb-0">
                👥 Share Shelf
              </h3>
            </div>

            <div className="card-body">

              {/* Shelf sharing form */}
              <form onSubmit={handleShare}>

                <div className="mb-3">

                  <label className="form-label">
                    User Email
                  </label>

                  <input
                    type="email"
                    className="form-control"
                    placeholder="Enter email"
                    value={email}
                    onChange={(e) =>
                      setEmail(e.target.value)
                    }
                    required
                  />

                </div>

                <div className="mb-4">

                  <label className="form-label">
                    Permission
                  </label>

                  <select
                    className="form-select"
                    value={role}
                    onChange={(e) =>
                      setRole(e.target.value)
                    }
                  >
                    <option value="viewer">
                      Viewer
                    </option>

                    <option value="editor">
                      Editor
                    </option>

                  </select>

                </div>

                <div className="d-flex justify-content-between">

                  {/* Cancel and return to the shelf page */}
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() =>
                      navigate(`/shelves/${id}`)
                    }
                    disabled={loading}
                  >
                    Cancel
                  </button>

                  {/* Submit the sharing request */}
                  <button
                    type="submit"
                    className="btn btn-success"
                    disabled={loading}
                  >
                    {loading
                      ? "Sharing..."
                      : "Share Shelf"}
                  </button>

                </div>

              </form>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default ShareShelf;