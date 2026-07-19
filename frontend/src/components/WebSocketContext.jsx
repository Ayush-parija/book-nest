import React, { createContext, useContext, useEffect, useState } from 'react';
import webSocketService from '../services/websocketService';

// Create a context for sharing WebSocket data across the application
const WebSocketContext = createContext();

// Custom hook for accessing WebSocket context values
export const useWebSocket = () => {
  return useContext(WebSocketContext);
};

// Provides WebSocket connection and message state to child components
export const WebSocketProvider = ({ children }) => {
  // Track the current WebSocket connection status
  const [status, setStatus] = useState('disconnected');

  // Store the latest received WebSocket message
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    // Connect to the WebSocket server when the provider is mounted
    webSocketService.connect();

    // Listen for WebSocket events
    const unsubscribe = webSocketService.subscribe((message) => {
      // Update connection status events
      if (message.type === 'CONNECTION_STATUS') {
        setStatus(message.status);

      // Store incoming notification messages
      } else if (message.type === 'MESSAGE') {
        setLastMessage(message.data);
      }
    });

    // Clean up the WebSocket connection when the provider is unmounted
    return () => {
      unsubscribe();
      webSocketService.disconnect();
    };
  }, []);

  return (
    // Make WebSocket state available throughout the application
    <WebSocketContext.Provider value={{ status, lastMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
};