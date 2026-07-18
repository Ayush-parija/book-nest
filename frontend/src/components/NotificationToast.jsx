import React, { useEffect, useState } from 'react';
import { useWebSocket } from './WebSocketContext';
import 'bootstrap/dist/css/bootstrap.min.css';

const NotificationToast = () => {
  const { lastMessage } = useWebSocket();
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    if (lastMessage) {
      const newToast = {
        id: Date.now(),
        message: lastMessage,
      };
      
      setToasts((prev) => [...prev, newToast]);

      // Auto-remove toast after 5 seconds
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== newToast.id));
      }, 5000);
    }
  }, [lastMessage]);

  if (toasts.length === 0) return null;

  return (
    <div
      aria-live="polite"
      aria-atomic="true"
      style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: 1050,
      }}
    >
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className="toast show align-items-center text-white bg-primary border-0 mb-2"
          role="alert"
          aria-live="assertive"
          aria-atomic="true"
          style={{ minWidth: '250px' }}
        >
          <div className="d-flex">
            <div className="toast-body">
              {toast.message}
            </div>
            <button
              type="button"
              className="btn-close btn-close-white me-2 m-auto"
              onClick={() => setToasts((prev) => prev.filter((t) => t.id !== toast.id))}
              aria-label="Close"
            ></button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default NotificationToast;
