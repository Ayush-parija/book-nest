import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import BookForm from "../components/BookForm";
import { getBook, updateBook } from "../services/bookService";

// Page for editing an existing book
function EditBook() {
  // Get the book ID from the route
  const { id } = useParams();

  // Used for page navigation
  const navigate = useNavigate();

  // Store the selected book details
  const [book, setBook] = useState(null);

  // Track loading state
  const [loading, setLoading] = useState(true);

  // Load the book details when the page opens
  useEffect(() => {
    fetchBook();
  }, []);

  // Fetch book information from the backend
  const fetchBook = async () => {
    try {
      const data = await getBook(id);
      setBook(data);
    } catch (error) {
      console.error("Error loading book:", error);
      alert("Failed to load book.");
    } finally {
      // Stop the loading indicator
      setLoading(false);
    }
  };

  // Update the selected book
  const handleUpdateBook = async (bookData) => {
    try {
      await updateBook(id, bookData);

      alert("Book updated successfully!");

      // Navigate back to the books page
      navigate("/books");
    } catch (error) {
      console.error("Update Error:", error);

      // Display server validation errors if available
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

  // Display a loading message while fetching book details
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
      {/* Page heading */}
      <h2>Edit Book</h2>

      {/* Reusable book form pre-filled with existing data */}
      <BookForm
        initialData={book}
        onSubmit={handleUpdateBook}
        buttonText="Update Book"
      />
    </div>
  );
}

export default EditBook;