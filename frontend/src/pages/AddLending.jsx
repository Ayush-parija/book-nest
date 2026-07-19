import LendingForm from "../components/LendingForm";

// Page for creating a new book lending record
function AddLending() {
  return (
    <div className="container mt-4">

      {/* Reusable lending form component */}
      <LendingForm />

    </div>
  );
}

export default AddLending;