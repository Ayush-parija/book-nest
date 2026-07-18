import api from "../api/axios";

const getAuthHeader = () => ({
  headers: {
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  },
});

// Get all books
export const getBooks = async () => {
  const response = await api.get("/books", getAuthHeader());
  return response.data;
};

// Get single book
export const getBook = async (id) => {
  const response = await api.get(`/books/${id}`, getAuthHeader());
  return response.data;
};

// Add new book
export const createBook = async (book) => {
  const response = await api.post("/books", book, getAuthHeader());
  return response.data;
};

// Update book
export const updateBook = async (id, book) => {
  const response = await api.patch(
    `/books/${id}`,
    book,
    getAuthHeader()
  );
  return response.data;
};

// Delete book
export const deleteBook = async (id) => {
  const response = await api.delete(
    `/books/${id}`,
    getAuthHeader()
  );
  return response.data;
};

// Toggle favorite
export const toggleFavorite = async (id) => {
  const response = await api.patch(
    `/books/${id}/favorite`,
    {},
    getAuthHeader()
  );
  return response.data;
};

// Update reading progress
export const updateReadingProgress = async (id, progress) => {
  const response = await api.patch(
    `/books/${id}/progress`,
    progress,
    getAuthHeader()
  );
  return response.data;
};

// Get favorite books
export const getFavoriteBooks = async () => {
  const response = await api.get(
    "/books/favorites",
    getAuthHeader()
  );
  return response.data;
};