import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import ShelfForm from "../components/ShelfForm";
import {
  getShelf,
  updateShelf,
} from "../services/shelfService";

const EditShelf = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [shelf, setShelf] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchShelf();
  }, []);

  const fetchShelf = async () => {
    try {
      const data = await getShelf(id);
      setShelf(data);
    } catch (error) {
      console.error(error);
      alert("Failed to load shelf.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateShelf = async (data) => {
    try {
      await updateShelf(id, data);

      alert("Shelf updated successfully!");

      navigate("/shelves");
    } catch (error) {
      console.error(error);
      alert("Failed to update shelf.");
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className="container mt-4">
      <h2>Edit Shelf</h2>

      <ShelfForm
        initialData={shelf}
        onSubmit={handleUpdateShelf}
      />
    </div>
  );
};

export default EditShelf;