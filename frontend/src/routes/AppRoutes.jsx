import { Routes, Route, Navigate } from "react-router-dom";

import Layout from "../components/Layout";

import Login from "../pages/Login";
import Signup from "../pages/Signup";
import Dashboard from "../pages/Dashboard";

import Books from "../pages/Books";
import AddBook from "../pages/AddBook";
import EditBook from "../pages/EditBook";

import Favorites from "../pages/Favorites";

import Shelves from "../pages/Shelves";
import AddShelf from "../pages/AddShelf";
import EditShelf from "../pages/EditShelf";
import ShelfDetails from "../pages/ShelfDetails";
import AddBookToShelf from "../pages/AddBookToShelf";
import ShareShelf from "../pages/ShareShelf";

// Lending page imports
import Lending from "../pages/Lending";
import AddLending from "../pages/AddLending";
import BorrowedBooks from "../pages/BorrowedBooks";
import LentBooks from "../pages/LentBooks";

import Activity from "../pages/Activity";
import ReadingProgress from "../pages/ReadingProgress";

// Defines all application routes
function AppRoutes() {
  return (
    <Routes>

      {/* Authentication routes */}
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      {/* Dashboard route */}
      <Route
        path="/dashboard"
        element={
          <Layout>
            <Dashboard />
          </Layout>
        }
      />

      {/* Book management routes */}
      <Route
        path="/books"
        element={
          <Layout>
            <Books />
          </Layout>
        }
      />

      <Route
        path="/books/add"
        element={
          <Layout>
            <AddBook />
          </Layout>
        }
      />

      <Route
        path="/books/edit/:id"
        element={
          <Layout>
            <EditBook />
          </Layout>
        }
      />

      {/* Favorite books route */}
      <Route
        path="/favorites"
        element={
          <Layout>
            <Favorites />
          </Layout>
        }
      />

      {/* ========================= */}
      {/* Shelf management routes */}
      {/* ========================= */}

      <Route
        path="/shelves"
        element={
          <Layout>
            <Shelves />
          </Layout>
        }
      />

      <Route
        path="/shelves/add"
        element={
          <Layout>
            <AddShelf />
          </Layout>
        }
      />

      <Route
        path="/shelves/:id"
        element={
          <Layout>
            <ShelfDetails />
          </Layout>
        }
      />

      <Route
        path="/shelves/:id/add-book"
        element={
          <Layout>
            <AddBookToShelf />
          </Layout>
        }
      />

      <Route
        path="/shelves/:id/share"
        element={
          <Layout>
            <ShareShelf />
          </Layout>
        }
      />

      <Route
        path="/shelves/edit/:id"
        element={
          <Layout>
            <EditShelf />
          </Layout>
        }
      />

      {/* ========================= */}
      {/* Book lending routes */}
      {/* ========================= */}

      <Route
        path="/lending"
        element={
          <Layout>
            <Lending />
          </Layout>
        }
      />

      <Route
        path="/lending/new"
        element={
          <Layout>
            <AddLending />
          </Layout>
        }
      />

      <Route
        path="/lending/borrowed"
        element={
          <Layout>
            <BorrowedBooks />
          </Layout>
        }
      />

      <Route
        path="/lending/lent"
        element={
          <Layout>
            <LentBooks />
          </Layout>
        }
      />

      {/* Activity history route */}
      <Route
        path="/activity"
        element={
          <Layout>
            <Activity />
          </Layout>
        }
      />

      {/* Reading progress tracking route */}
      <Route
        path="/reading-progress"
        element={
          <Layout>
            <ReadingProgress />
          </Layout>
        }
      />

      {/* Redirect all unknown routes to the login page */}
      <Route path="*" element={<Navigate to="/" replace />} />

    </Routes>
  );
}

export default AppRoutes;