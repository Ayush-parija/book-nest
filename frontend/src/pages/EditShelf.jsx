import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import ShelfForm from "../components/ShelfForm";
import {
  getShelf,
  updateShelf,
} from "../services/shelfService";

// Page for editing an existing shelf
const EditShelf = () => {
  // Get the shelf ID from the route
  const { id } = useParams();

  // Used for page navigation
  const navigate = useNavigate();

  // Store the selected shelf details
  const [shelf, setShelf] = useState(null);

  // Track loading state
  const [loading, setLoading] = useState(true);

  // Load shelf details when the page opens
  useEffect(() => {
    fetchShelf();
  }, []);

  // Fetch shelf information from the backend
  const fetchShelf = async () => {
    try {
      const data = await getShelf(id);
      setShelf(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load shelf.");
    } finally {
      // Stop the loading indicator
      setLoading(false);
    }
  };

  // Update the selected shelf
  const handleUpdateShelf = async (data) => {
    try {
      await updateShelf(id, data);

      alert("Shelf updated successfully!");

      // Navigate back to the shelves page
      navigate("/shelves");
    } catch (error) {
      console.error(error);
      alert("Failed to update shelf.");
    }
  };

  // Display a loading message while fetching shelf details
  if (loading) return <p>Loading...</p>;

  return (
    <div className="container mt-4">

      {/* Page heading */}
      <h2>Edit Shelf</h2>

      {/* Reusable shelf form pre-filled with existing data */}
      <ShelfForm
        initialData={shelf}
        onSubmit={handleUpdateShelf}
      />

    </div>
  );
};

export default EditShelf;