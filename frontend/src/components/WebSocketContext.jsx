import React, { createContext, useContext, useEffect, useState } from 'react';
import webSocketService from '../services/websocketService';

const WebSocketContext = createContext();

export const useWebSocket = () => {
  return useContext(WebSocketContext);
};

export const WebSocketProvider = ({ children }) => {
  const [status, setStatus] = useState('disconnected');
  const [lastMessage, setLastMessage] = useState(null);

  useEffect(() => {
    // Connect to WebSocket when the provider is mounted
    webSocketService.connect();

    // Subscribe to WebSocket events
    const unsubscribe = webSocketService.subscribe((message) => {
      if (message.type === 'CONNECTION_STATUS') {
        setStatus(message.status);
      } else if (message.type === 'MESSAGE') {
        setLastMessage(message.data);
      }
    });

    // Cleanup on unmount
    return () => {
      unsubscribe();
      webSocketService.disconnect();
    };
  }, []);

  return (
    <WebSocketContext.Provider value={{ status, lastMessage }}>
      {children}
    </WebSocketContext.Provider>
  );
};
