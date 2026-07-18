import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import BookForm from "../components/BookForm";
import { getBook, updateBook } from "../services/bookService";

function EditBook() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBook();
  }, []);

  const fetchBook = async () => {
    try {
      const data = await getBook(id);
      setBook(data);
    } catch (error) {
      console.error("Error loading book:", error);
      alert("Failed to load book.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateBook = async (bookData) => {
    try {
      await updateBook(id, bookData);

      alert("Book updated successfully!");

      navigate("/books");
    } catch (error) {
      console.error("Update Error:", error);

      if (error.response) {
        console.log("Status:", error.response.status);
        console.log("Response:", error.response.data);

        alert(
          JSON.stringify(
            error.response.data,
            null,
            2
          )
        );
      } else {
        alert(error.message);
      }
    }
  };

  if (loading) {
    return (
      <h2 style={{ textAlign: "center" }}>
        Loading...
      </h2>
    );
  }

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "40px auto",
        padding: "20px",
      }}
    >
      <h2>Edit Book</h2>

      <BookForm
        initialData={book}
        onSubmit={handleUpdateBook}
        buttonText="Update Book"
      />
    </div>
  );
}

export default EditBook;