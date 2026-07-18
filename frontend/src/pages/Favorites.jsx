import { useEffect, useState } from "react";
import FavoriteBookCard from "../components/FavoriteBookCard";
import { getFavoriteBooks } from "../services/bookService";

function Favorites() {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchFavorites = async () => {
    try {
      const data = await getFavoriteBooks();
      setFavorites(data);
    } catch (error) {
      console.error("Error loading favorites:", error);
      alert("Failed to load favorite books.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFavorites();
  }, []);

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
      <h2>⭐ Favorite Books</h2>

      {favorites.length === 0 ? (
        <p>No favorite books found.</p>
      ) : (
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