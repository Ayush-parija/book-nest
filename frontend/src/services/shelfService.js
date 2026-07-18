import api from "../api/axios";

// ==============================
// Shelf CRUD
// ==============================

// Get all shelves
export const getShelves = async () => {
  const response = await api.get("/shelves");
  return response.data;
};

// Get one shelf
export const getShelf = async (id) => {
  const response = await api.get(`/shelves/${id}`);
  return response.data;
};

// Create shelf
export const createShelf = async (data) => {
  const response = await api.post("/shelves", data);
  return response.data;
};

// Update shelf
export const updateShelf = async (id, data) => {
  const response = await api.patch(`/shelves/${id}`, data);
  return response.data;
};

// Delete shelf
export const deleteShelf = async (id) => {
  const response = await api.delete(`/shelves/${id}`);
  return response.data;
};

// ==============================
// Shelf Books
// ==============================

// Get books in a shelf
export const getShelfBooks = async (shelfId) => {
  const response = await api.get(`/shelves/${shelfId}/books`);
  return response.data;
};

// Add a book to a shelf
export const addBookToShelf = async (shelfId, bookId) => {
  const response = await api.post(
    `/shelves/${shelfId}/books/${bookId}`
  );
  return response.data;
};

// Remove a book from a shelf
export const removeBookFromShelf = async (shelfId, bookId) => {
  const response = await api.delete(
    `/shelves/${shelfId}/books/${bookId}`
  );
  return response.data;
};

// ==============================
// Shelf Sharing
// ==============================

// Share a shelf
export const shareShelf = async (shelfId, data) => {
  const response = await api.post(
    `/shelves/${shelfId}/share`,
    data
  );
  return response.data;
};