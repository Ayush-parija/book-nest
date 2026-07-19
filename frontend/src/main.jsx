import React from "react";
import ReactDOM from "react-dom/client";

// Import Bootstrap styles
import "bootstrap/dist/css/bootstrap.min.css";

// Import Bootstrap JavaScript components
import "bootstrap/dist/js/bootstrap.bundle.min.js";

// Import global application styles
import "./index.css";

// Import the root application component
import App from "./App";

// Render the React application into the root DOM element
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);