import api from "../api/axios";

// Service for managing book-related API requests

// Fetch all books with optional query parameters
export const getBooks = async (params = {}) => {
  const response = await api.get("/books", { params });
  return response.data;
};

// Fetch details of a single book by its ID
export const getBook = async (id) => {
  const response = await api.get(`/books/${id}`);
  return response.data;
};

// Create a new book
export const createBook = async (book) => {
  const response = await api.post("/books", book);
  return response.data;
};

// Update an existing book
export const updateBook = async (id, book) => {
  const response = await api.patch(`/books/${id}`, book);
  return response.data;
};

// Delete a book from the library
export const deleteBook = async (id) => {
  const response = await api.delete(`/books/${id}`);
  return response.data;
};

// Mark or unmark a book as a favorite
export const toggleFavorite = async (id) => {
  const response = await api.patch(`/books/${id}/favorite`, {});
  return response.data;
};

// Update the current reading progress of a book
export const updateReadingProgress = async (id, progress) => {
  const response = await api.patch(`/books/${id}/progress`, progress);
  return response.data;
};

// Fetch all books marked as favorites
export const getFavoriteBooks = async () => {
  const response = await api.get("/books/favorites");
  return response.data;
};