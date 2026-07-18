import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";
import { WebSocketProvider } from "./components/WebSocketContext";
import NotificationToast from "./components/NotificationToast";

function App() {
  return (
    <WebSocketProvider>
      <BrowserRouter>
        <NotificationToast />
        <AppRoutes />
      </BrowserRouter>
    </WebSocketProvider>
  );
}

export default App;