import api from "../api/axios";

// ==========================
// Lending
// ==========================

// Lend a book
export const lendBook = async (bookId, data) => {
  const response = await api.post(
    `/lending/books/${bookId}/lend`,
    data
  );

  return response.data;
};

// Borrowed books
export const getBorrowedBooks = async () => {
  const response = await api.get("/lending/borrowed");
  return response.data;
};

// Lent books
export const getLentBooks = async () => {
  const response = await api.get("/lending/lent");
  return response.data;
};

// Return a book
export const returnBook = async (bookId) => {
  const response = await api.post(
    `/lending/books/${bookId}/return`
  );

  return response.data;
};