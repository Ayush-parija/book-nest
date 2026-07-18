import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { shareShelf } from "../services/shelfService";

function ShareShelf() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [role, setRole] = useState("viewer");
  const [loading, setLoading] = useState(false);

  const handleShare = async (e) => {
    e.preventDefault();

    if (!email.trim()) {
      alert("Please enter an email address.");
      return;
    }

    try {
      setLoading(true);

      await shareShelf(id, {
        email: email.trim(),
        role,
      });

      alert("Shelf shared successfully!");

      navigate(`/shelves/${id}`);
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.detail ||
          "Failed to share shelf."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5">

      <div className="row justify-content-center">

        <div className="col-md-6">

          <div className="card shadow">

            <div className="card-header bg-success text-white">
              <h3 className="mb-0">
                👥 Share Shelf
              </h3>
            </div>

            <div className="card-body">

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