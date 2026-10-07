import { useEffect, useState } from "react";

function AdminDashboard() {
  const [grievances, setGrievances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ============================================================
  // FILTER STATES
  // ============================================================

  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [severityFilter, setSeverityFilter] = useState("All");
  const [departmentFilter, setDepartmentFilter] = useState("All");

  // Selected grievance for details modal
  const [selectedGrievance, setSelectedGrievance] = useState(null);


  // ============================================================
  // FETCH GRIEVANCES
  // ============================================================

  const fetchGrievances = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/grievances"
      );

      if (!response.ok) {
        throw new Error("Failed to fetch grievances");
      }

      const data = await response.json();

      setGrievances(data.grievances);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };


  // ============================================================
  // LOAD DATA
  // ============================================================

  useEffect(() => {
    fetchGrievances();
  }, []);


  // ============================================================
  // STATISTICS
  // ============================================================

  const urgentCount = grievances.filter(
    (grievance) => grievance.severity === "Urgent"
  ).length;

  const highCount = grievances.filter(
    (grievance) => grievance.severity === "High"
  ).length;

  const mediumCount = grievances.filter(
    (grievance) => grievance.severity === "Medium"
  ).length;

  const lowCount = grievances.filter(
    (grievance) => grievance.severity === "Low"
  ).length;


  // ============================================================
  // FILTER GRIEVANCES
  // ============================================================

  const filteredGrievances = grievances.filter((grievance) => {
    const searchText = search.toLowerCase().trim();

    const matchesSearch =
      grievance.complaint.toLowerCase().includes(searchText) ||
      grievance.category.toLowerCase().includes(searchText) ||
      grievance.department.toLowerCase().includes(searchText);

    const matchesCategory =
      categoryFilter === "All" ||
      grievance.category === categoryFilter;

    const matchesSeverity =
      severityFilter === "All" ||
      grievance.severity === severityFilter;

    const matchesDepartment =
      departmentFilter === "All" ||
      grievance.department === departmentFilter;

    return (
      matchesSearch &&
      matchesCategory &&
      matchesSeverity &&
      matchesDepartment
    );
  });


  // ============================================================
  // UNIQUE FILTER OPTIONS
  // ============================================================

  const categories = [
    "All",
    ...new Set(
      grievances.map((grievance) => grievance.category)
    ),
  ];

  const severities = [
    "All",
    "Urgent",
    "High",
    "Medium",
    "Low",
  ];

  const departments = [
    "All",
    ...new Set(
      grievances.map((grievance) => grievance.department)
    ),
  ];


  // ============================================================
  // RESET FILTERS
  // ============================================================

  const resetFilters = () => {
    setSearch("");
    setCategoryFilter("All");
    setSeverityFilter("All");
    setDepartmentFilter("All");
  };


  // ============================================================
  // UI
  // ============================================================

  return (
    <div className="admin-dashboard">

      {/* ======================================================
          HEADER
          ====================================================== */}

      <div className="admin-header">

        <div>
          <h1>Admin Dashboard</h1>

          <p>
            AI College Grievance Analyzer
          </p>
        </div>

        <button onClick={fetchGrievances}>
          Refresh
        </button>

      </div>


      {/* ======================================================
          LOADING
          ====================================================== */}

      {loading && (
        <div className="admin-message">
          Loading grievances...
        </div>
      )}


      {/* ======================================================
          ERROR
          ====================================================== */}

      {error && (
        <div className="admin-error">
          {error}
        </div>
      )}


      {/* ======================================================
          DASHBOARD CONTENT
          ====================================================== */}

      {!loading && !error && (
        <>

          {/* ==================================================
              STATISTICS
              ================================================== */}

          <div className="stats-grid">

            <div className="stat-card">
              <span>
                Total Grievances
              </span>

              <strong>
                {grievances.length}
              </strong>
            </div>


            <div className="stat-card urgent">
              <span>
                Urgent
              </span>

              <strong>
                {urgentCount}
              </strong>
            </div>


            <div className="stat-card high">
              <span>
                High
              </span>

              <strong>
                {highCount}
              </strong>
            </div>


            <div className="stat-card medium">
              <span>
                Medium
              </span>

              <strong>
                {mediumCount}
              </strong>
            </div>


            <div className="stat-card low">
              <span>
                Low
              </span>

              <strong>
                {lowCount}
              </strong>
            </div>

          </div>


          {/* ==================================================
              GRIEVANCE TABLE CARD
              ================================================== */}

          <div className="admin-card">

            <div className="table-header">

              <div>

                <h2>
                  All Grievances
                </h2>

                <p className="result-count">
                  Showing{" "}
                  <strong>
                    {filteredGrievances.length}
                  </strong>{" "}
                  of{" "}
                  <strong>
                    {grievances.length}
                  </strong>{" "}
                  grievances
                </p>

              </div>

            </div>


            {/* ==================================================
                FILTERS
                ================================================== */}

            <div className="filters">

              {/* Search */}

              <div className="filter-group search-group">

                <label>
                  Search
                </label>

                <input
                  type="text"
                  value={search}
                  onChange={(e) =>
                    setSearch(e.target.value)
                  }
                  placeholder="Search complaints, category, department..."
                />

              </div>


              {/* Category */}

              <div className="filter-group">

                <label>
                  Category
                </label>

                <select
                  value={categoryFilter}
                  onChange={(e) =>
                    setCategoryFilter(e.target.value)
                  }
                >

                  {categories.map((category) => (
                    <option
                      key={category}
                      value={category}
                    >
                      {category}
                    </option>
                  ))}

                </select>

              </div>


              {/* Severity */}

              <div className="filter-group">

                <label>
                  Severity
                </label>

                <select
                  value={severityFilter}
                  onChange={(e) =>
                    setSeverityFilter(e.target.value)
                  }
                >

                  {severities.map((severity) => (
                    <option
                      key={severity}
                      value={severity}
                    >
                      {severity}
                    </option>
                  ))}

                </select>

              </div>


              {/* Department */}

              <div className="filter-group">

                <label>
                  Department
                </label>

                <select
                  value={departmentFilter}
                  onChange={(e) =>
                    setDepartmentFilter(e.target.value)
                  }
                >

                  {departments.map((department) => (
                    <option
                      key={department}
                      value={department}
                    >
                      {department}
                    </option>
                  ))}

                </select>

              </div>


              {/* Reset */}

              <button
                className="reset-button"
                onClick={resetFilters}
              >
                Reset
              </button>

            </div>


            {/* ==================================================
                TABLE
                ================================================== */}

            {filteredGrievances.length === 0 ? (

              <div className="no-results">

                <h3>
                  No grievances found
                </h3>

                <p>
                  Try changing your search or filters.
                </p>

              </div>

            ) : (

              <div className="table-container">

                <table>

                  <thead>

                    <tr>

                      <th>
                        ID
                      </th>

                      <th>
                        Complaint
                      </th>

                      <th>
                        Category
                      </th>

                      <th>
                        Severity
                      </th>

                      <th>
                        Department
                      </th>

                      <th>
                        Date
                      </th>

                    </tr>

                  </thead>


                  <tbody>

                    {filteredGrievances.map(
                      (grievance) => (

                        <tr
                          key={grievance.id}
                          className="grievance-row"
                          onClick={() =>
                            setSelectedGrievance(grievance)
                          }
                        >

                          <td>
                            #{grievance.id}
                          </td>


                          <td className="complaint-cell">
                            {grievance.complaint}
                          </td>


                          <td>
                            {grievance.category}
                          </td>


                          <td>

                            <span
                              className={`severity-badge ${grievance.severity.toLowerCase()}`}
                            >
                              {grievance.severity}
                            </span>

                          </td>


                          <td>
                            {grievance.department}
                          </td>


                          <td>
                            {new Date(
                              grievance.created_at
                            ).toLocaleString()}
                          </td>

                        </tr>

                      )
                    )}

                  </tbody>

                </table>

              </div>

            )}

          </div>


          {/* ==================================================
              GRIEVANCE DETAILS MODAL
              ================================================== */}

          {selectedGrievance && (

            <div
              className="modal-overlay"
              onClick={() =>
                setSelectedGrievance(null)
              }
            >

              <div
                className="grievance-modal"
                onClick={(e) =>
                  e.stopPropagation()
                }
              >

                {/* Modal Header */}

                <div className="modal-header">

                  <div>

                    <h2>
                      Grievance #{selectedGrievance.id}
                    </h2>

                    <p>
                      Submitted grievance details
                    </p>

                  </div>


                  <button
                    className="modal-close"
                    onClick={() =>
                      setSelectedGrievance(null)
                    }
                  >
                    ×
                  </button>

                </div>


                {/* Complaint */}

                <div className="modal-complaint">

                  <span>
                    Complaint
                  </span>

                  <p>
                    {selectedGrievance.complaint}
                  </p>

                </div>


                {/* Details */}

                <div className="modal-details">

                  <div className="modal-detail">

                    <span>
                      Category
                    </span>

                    <strong>
                      {selectedGrievance.category}
                    </strong>

                  </div>


                  <div className="modal-detail">

                    <span>
                      Severity
                    </span>

                    <strong>

                      <span
                        className={`severity-badge ${selectedGrievance.severity.toLowerCase()}`}
                      >
                        {selectedGrievance.severity}
                      </span>

                    </strong>

                  </div>


                  <div className="modal-detail">

                    <span>
                      Responsible Department
                    </span>

                    <strong>
                      {selectedGrievance.department}
                    </strong>

                  </div>


                  <div className="modal-detail">

                    <span>
                      AI Similarity
                    </span>

                    <strong>
                      {
                        (
                          selectedGrievance.similarity * 100
                        ).toFixed(2)
                      }%
                    </strong>

                  </div>


                  <div className="modal-detail">

                    <span>
                      Submitted At
                    </span>

                    <strong>
                      {new Date(
                        selectedGrievance.created_at
                      ).toLocaleString()}
                    </strong>

                  </div>

                </div>


                {/* Modal Footer */}

                <div className="modal-footer">

                  <button
                    className="modal-secondary-button"
                    onClick={() =>
                      setSelectedGrievance(null)
                    }
                  >
                    Close
                  </button>

                </div>

              </div>

            </div>

          )}

        </>
      )}

    </div>
  );
}

export default AdminDashboard;