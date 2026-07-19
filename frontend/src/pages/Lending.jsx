import { Link } from "react-router-dom";

// Main page for managing book lending activities
function Lending() {
  return (
    <div className="container mt-4">

      <div className="d-flex justify-content-between align-items-center mb-4">

        {/* Page heading */}
        <h2>📚 Lending</h2>

        {/* Navigate to the create lending page */}
        <Link
          to="/lending/new"
          className="btn btn-primary"
        >
          ➕ Lend Book
        </Link>

      </div>

      <div className="row">

        {/* Borrowed books section */}
        <div className="col-md-6 mb-3">
          <div className="card shadow-sm">
            <div className="card-body">

              <h4>📖 Borrowed Books</h4>

              <p>
                View books you have borrowed.
              </p>

              <Link
                to="/lending/borrowed"
                className="btn btn-success"
              >
                View Borrowed Books
              </Link>

            </div>
          </div>
        </div>

        {/* Lent books section */}
        <div className="col-md-6 mb-3">
          <div className="card shadow-sm">
            <div className="card-body">

              <h4>📚 Lent Books</h4>

              <p>
                View books you have lent.
              </p>

              <Link
                to="/lending/lent"
                className="btn btn-warning"
              >
                View Lent Books
              </Link>

            </div>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Lending;