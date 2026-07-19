import { useEffect, useState } from "react";
import FavoriteBookCard from "../components/FavoriteBookCard";
import { getFavoriteBooks } from "../services/bookService";

// Displays all books marked as favorites
function Favorites() {
  // Store the list of favorite books
  const [favorites, setFavorites] = useState([]);

  // Track loading state
  const [loading, setLoading] = useState(true);

  // Fetch favorite books from the backend
  const fetchFavorites = async () => {
    try {
      const data = await getFavoriteBooks();
      setFavorites(data);
    } catch (error) {
      console.error("Error loading favorites:", error);
      alert("Failed to load favorite books.");
    } finally {
      // Stop the loading indicator
      setLoading(false);
    }
  };

  // Load favorite books when the page opens
  useEffect(() => {
    fetchFavorites();
  }, []);

  // Display a loading message while fetching data
  if (loading) {
    return (
      <div style={{ padding: "30px" }}>
        <h2>⭐ Favorite Books</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: "30px" }}>

      {/* Page heading */}
      <h2>⭐ Favorite Books</h2>

      {/* Display a message if no favorite books exist */}
      {favorites.length === 0 ? (
        <p>No favorite books found.</p>
      ) : (
        // Render each favorite book
        favorites.map((book) => (
          <FavoriteBookCard
            key={book.id}
            book={book}
            refreshFavorites={fetchFavorites}
          />
        ))
      )}

    </div>
  );
}

export default Favorites;