import { useState } from "react";
import { useNavigate } from "react-router-dom";

import ShelfForm from "../components/ShelfForm";
import { createShelf } from "../services/shelfService";

// Page for creating a new bookshelf
function AddShelf() {
  const navigate = useNavigate();

  // Track the form submission state
  const [loading, setLoading] = useState(false);

  // Create a new shelf
  const handleCreateShelf = async (data) => {
    try {
      setLoading(true);

      // Send shelf data to the backend
      await createShelf(data);

      alert("Shelf created successfully!");

      // Redirect to the shelves page
      navigate("/shelves");
    } catch (error) {
      console.error(error);
      alert("Failed to create shelf.");
    } finally {
      // Reset the loading state
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">

      <div className="row justify-content-center">

        <div className="col-md-8">

          <div className="card shadow">

            {/* Page header */}
            <div className="card-header bg-primary text-white">
              <h3 className="mb-0">📚 Create New Shelf</h3>
            </div>

            <div className="card-body">

              {/* Reusable shelf form component */}
              <ShelfForm
                onSubmit={handleCreateShelf}
                loading={loading}
              />

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default AddShelf;