// Service for managing real-time WebSocket communication

class WebSocketService {
  constructor() {
    // Store the active WebSocket connection
    this.ws = null;

    // Store all subscribed listeners
    this.listeners = new Set();

    // Track the number of reconnect attempts
    this.reconnectAttempts = 0;

    // Maximum reconnect attempts before stopping
    this.maxReconnectAttempts = 5;

    // Track the current connection status
    this.isConnected = false;

    // Backend WebSocket endpoint
    this.url = "ws://localhost:8000/ws"; // Replace with your backend WS URL if different
  }

  // Establish a WebSocket connection
  connect() {
    // Prevent duplicate WebSocket connections
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    // Retrieve the authentication token
    const token = sessionStorage.getItem("access_token");

    // Skip connection if the user is not authenticated
    if (!token) {
      console.warn("WebSocket connection skipped: No access token found.");
      return;
    }

    console.log("Connecting to WebSocket...");

    // Create the authenticated WebSocket URL
    const connectionUrl = `${this.url}?token=${token}`;

    // Initialize the WebSocket connection
    this.ws = new WebSocket(connectionUrl);

    // Handle successful connection
    this.ws.onopen = () => {
      console.log("WebSocket connected!");
      this.isConnected = true;
      this.reconnectAttempts = 0;

      // Notify subscribers about the connection status
      this.notifyListeners({ type: "CONNECTION_STATUS", status: "connected" });
    };

    // Handle incoming messages
    this.ws.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);

      // Forward received messages to all subscribers
      this.notifyListeners({ type: "MESSAGE", data: event.data });
    };

    // Handle connection closure
    this.ws.onclose = () => {
      console.log("WebSocket disconnected.");
      this.isConnected = false;

      // Notify subscribers about the disconnection
      this.notifyListeners({ type: "CONNECTION_STATUS", status: "disconnected" });

      // Attempt to reconnect automatically
      this.attemptReconnect();
    };

    // Handle WebSocket errors
    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);

      // Close the connection to trigger reconnection
      this.ws.close();
    };
  }

  // Retry the connection using exponential backoff
  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;

      const timeout = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);

      console.log(`Attempting reconnect in ${timeout}ms (Attempt ${this.reconnectAttempts})`);

      setTimeout(() => this.connect(), timeout);
    } else {
      console.error("Max reconnect attempts reached.");
    }
  }

  // Close the active WebSocket connection
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  // Register a listener for WebSocket events
  subscribe(listener) {
    this.listeners.add(listener);

    // Return a function to unsubscribe the listener
    return () => this.listeners.delete(listener);
  }

  // Notify all subscribed listeners about an event
  notifyListeners(message) {
    this.listeners.forEach((listener) => listener(message));
  }
}

// Export a single shared WebSocket service instance
const webSocketService = new WebSocketService();

export default webSocketService;