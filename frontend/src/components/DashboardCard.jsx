function DashboardCard({ title, value }) {
  return (
    <div className="col-md-4 mb-4">
      <div className="card shadow-sm text-center h-100">
        <div className="card-body">
          <h6 className="text-muted">{title}</h6>
          <h2>{value}</h2>
        </div>
      </div>
    </div>
  );
}

export default DashboardCard;