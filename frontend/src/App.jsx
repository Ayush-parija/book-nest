import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";
import { WebSocketProvider } from "./components/WebSocketContext";
import NotificationToast from "./components/NotificationToast";

// Root application component
function App() {
  return (
    // Provide WebSocket functionality throughout the application
    <WebSocketProvider>

      {/* Enable client-side routing */}
      <BrowserRouter>

        {/* Display real-time notifications */}
        <NotificationToast />

        {/* Render all application routes */}
        <AppRoutes />

      </BrowserRouter>

    </WebSocketProvider>
  );
}

export default App;