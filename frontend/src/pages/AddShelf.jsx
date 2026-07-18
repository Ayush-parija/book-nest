import { useState } from "react";
import { useNavigate } from "react-router-dom";

import ShelfForm from "../components/ShelfForm";
import { createShelf } from "../services/shelfService";

function AddShelf() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleCreateShelf = async (data) => {
    try {
      setLoading(true);

      await createShelf(data);

      alert("Shelf created successfully!");

      navigate("/shelves");
    } catch (error) {
      console.error(error);
      alert("Failed to create shelf.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">

      <div className="row justify-content-center">

        <div className="col-md-8">

          <div className="card shadow">

            <div className="card-header bg-primary text-white">
              <h3 className="mb-0">📚 Create New Shelf</h3>
            </div>

            <div className="card-body">

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