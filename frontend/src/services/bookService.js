import api from "../api/axios";

// Get all books
export const getBooks = async (params = {}) => {
  const response = await api.get("/books", { params });
  return response.data;
};

// Get single book
export const getBook = async (id) => {
  const response = await api.get(`/books/${id}`);
  return response.data;
};

// Add new book
export const createBook = async (book) => {
  const response = await api.post("/books", book);
  return response.data;
};

// Update book
export const updateBook = async (id, book) => {
  const response = await api.patch(`/books/${id}`, book);
  return response.data;
};

// Delete book
export const deleteBook = async (id) => {
  const response = await api.delete(`/books/${id}`);
  return response.data;
};

// Toggle favorite
export const toggleFavorite = async (id) => {
  const response = await api.patch(`/books/${id}/favorite`, {});
  return response.data;
};

// Update reading progress
export const updateReadingProgress = async (id, progress) => {
  const response = await api.patch(`/books/${id}/progress`, progress);
  return response.data;
};

// Get favorite books
export const getFavoriteBooks = async () => {
  const response = await api.get("/books/favorites");
  return response.data;
};