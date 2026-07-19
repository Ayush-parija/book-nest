import api from "../api/axios";

// Service for managing book lending operations

// ==========================
// Lending
// ==========================

// Lend a book to another user
export const lendBook = async (bookId, data) => {
  const response = await api.post(
    `/lending/books/${bookId}/lend`,
    data
  );

  return response.data;
};

// Fetch books currently borrowed by the logged-in user
export const getBorrowedBooks = async () => {
  const response = await api.get("/lending/borrowed");
  return response.data;
};

// Fetch books currently lent by the logged-in user
export const getLentBooks = async () => {
  const response = await api.get("/lending/lent");
  return response.data;
};

// Mark a lent book as returned
export const returnBook = async (bookId) => {
  const response = await api.post(
    `/lending/books/${bookId}/return`
  );

  return response.data;
};