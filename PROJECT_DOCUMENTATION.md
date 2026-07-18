# BookNest Project Documentation

## Folder Structure

```
book-nest/
├── backend/
│   ├── app/
│   │   ├── api/            # Route handlers for all endpoints
│   │   ├── core/           # Configuration and security settings
│   │   ├── db/             # Database connection and session management
│   │   ├── dependencies/   # FastAPI dependencies (auth)
│   │   ├── models/         # SQLAlchemy database models
│   │   ├── repositories/   # Data access layer for database queries
│   │   ├── schemas/        # Pydantic models for request/response validation
│   │   ├── services/       # Business logic layer
│   │   ├── websocket/      # Real-time connection management
│   │   └── main.py         # FastAPI application entry point
│   ├── .env.example        # Environment variable template
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/            # Axios instance and interceptors
│   │   ├── assets/         # Static assets (images, icons)
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Full-page views
│   │   ├── routes/         # React Router configuration
│   │   ├── services/       # API call wrappers
│   │   ├── styles/         # CSS stylesheets
│   │   ├── App.jsx         # Root component
│   │   └── main.jsx        # React entry point
│   └── package.json        # Node dependencies and scripts
└── README.md               # Project overview and setup instructions
```

## Backend Request Flow

1. **Client Request:** The frontend makes an HTTP request to a specific endpoint (e.g., `POST /books`).
2. **API Layer (`app/api/`):** The FastAPI router receives the request. It uses Pydantic schemas for input validation and dependencies (like `get_current_user`) for authentication.
3. **Service Layer (`app/services/`):** The router passes the validated data to a service function. The service handles the business logic (e.g., checking if the user can create a book, formatting data).
4. **Repository Layer (`app/repositories/`):** The service calls repository functions to interact with the database. Repositories encapsulate SQLAlchemy queries.
5. **Database (`app/db/`, `app/models/`):** The repository executes queries against the PostgreSQL/SQLite database using SQLAlchemy models.
6. **Response:** The data flows back up through the repository, service, and API router, where it is serialized into a JSON response (using response schemas) and sent back to the client.

## Frontend Request Flow

1. **User Action:** The user interacts with the UI (e.g., clicks "Save Book").
2. **Component Event:** A React component handles the event and calls a function from a service module (e.g., `createBook()` in `bookService.js`).
3. **API Service (`src/services/`):** The service module uses the configured Axios instance (`src/api/axios.js`) to make the request.
4. **Axios Interceptors:** The request interceptor attaches the JWT `access_token`. If the request fails with a 401 Unauthorized, the response interceptor automatically attempts to refresh the token using the `refresh_token` cookie and retries the request.
5. **State Update:** Once the response is received, the component updates its local state or a global context, triggering a re-render to display the new data.

## Authentication Flow

BookNest uses a JWT-based Refresh Token flow:
1. **Login:** User submits email/password. Backend verifies and returns a short-lived `access_token` (JSON body) and a long-lived `refresh_token` (`HttpOnly` cookie).
2. **Authenticated Requests:** Frontend sends the `access_token` in the `Authorization: Bearer <token>` header for protected routes.
3. **Token Expiration:** When the `access_token` expires, the backend returns 401. The frontend's Axios interceptor automatically calls `POST /auth/refresh`. Since the `refresh_token` is an `HttpOnly` cookie, the browser sends it automatically.
4. **Refresh:** The backend validates the cookie and returns a new `access_token`. The frontend stores it and retries the original failed request.
5. **Logout:** Frontend calls `POST /auth/logout` (backend clears the cookie) and removes the `access_token` from `localStorage`.

## WebSocket Flow

1. **Connection:** When a user logs in, the `WebSocketContext` initializes a connection to `ws://localhost:8000/ws?token=<access_token>`.
2. **Authentication:** The backend `/ws` endpoint intercepts the connection, decodes the JWT token from the query parameter, and registers the WebSocket connection under the user's `user_id` in the `ConnectionManager`.
3. **Targeted Broadcasting:** When an event occurs (e.g., a book is lent), a service (like `lending_service.py`) calls `manager.send_to_user_sync(borrower_id, message)`.
4. **Notification:** The `ConnectionManager` finds the active WebSocket(s) for that `user_id` and sends the message. The frontend receives the message in `websocketService.js` and updates the UI (e.g., showing a toast notification).

## Design Patterns

*   **Repository Pattern (Backend):** Abstracts database interactions. Services don't write SQL/SQLAlchemy queries directly; they call repositories (e.g., `BookRepository.get_by_id`). This makes testing easier and centralizes query logic.
*   **Service Layer (Backend):** Separates business rules from HTTP transport logic (API routers). API routers only handle request validation and response formatting. Services handle the "what" and "why" of the application.
*   **Context API (Frontend):** React's Context API is used for global state that needs to be accessed by many components (e.g., `WebSocketContext` for real-time connection status and messages).

## Future Improvements

*   **Redis Pub/Sub:** Replace the in-memory `ConnectionManager` with Redis Pub/Sub to support horizontal scaling of the backend WebSocket servers.
*   **Pagination & Filtering:** Enhance frontend tables with server-side pagination, sorting, and advanced filtering (currently some filtering is client-side).
*   **State Management Library:** Introduce Redux or Zustand for more complex frontend state management as the application grows.
*   **Unit & Integration Tests:** Add comprehensive test suites for both backend (pytest) and frontend (Jest/React Testing Library).
