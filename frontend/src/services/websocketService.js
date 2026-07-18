class WebSocketService {
  constructor() {
    this.ws = null;
    this.listeners = new Set();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.isConnected = false;
    this.url = "ws://localhost:8000/ws"; // Replace with your backend WS URL if different
  }

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    console.log("Connecting to WebSocket...");
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log("WebSocket connected!");
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.notifyListeners({ type: "CONNECTION_STATUS", status: "connected" });
    };

    this.ws.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      this.notifyListeners({ type: "MESSAGE", data: event.data });
    };

    this.ws.onclose = () => {
      console.log("WebSocket disconnected.");
      this.isConnected = false;
      this.notifyListeners({ type: "CONNECTION_STATUS", status: "disconnected" });
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      this.ws.close();
    };
  }

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

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener); // Return unsubscribe function
  }

  notifyListeners(message) {
    this.listeners.forEach((listener) => listener(message));
  }
}

const webSocketService = new WebSocketService();
export default webSocketService;
