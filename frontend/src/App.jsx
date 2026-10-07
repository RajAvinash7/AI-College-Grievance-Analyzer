import { useState } from "react";
import "./App.css";
import AdminDashboard from "./AdminDashboard";


function StudentPortal() {

  const [complaint, setComplaint] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);


  // ==========================================================
  // SUBMIT COMPLAINT
  // ==========================================================

  const submitComplaint = async (e) => {

    e.preventDefault();

    if (!complaint.trim()) {
      return;
    }

    setLoading(true);
    setResult(null);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            complaint: complaint,
          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail || "Something went wrong"
        );

      }


      setResult(data);

    } catch (error) {

      setResult({
        valid: false,
        message: error.message,
      });

    } finally {

      setLoading(false);

    }
  };


  // ==========================================================
  // SUBMIT ANOTHER GRIEVANCE
  // ==========================================================

  const submitAnother = () => {

    setComplaint("");
    setResult(null);

  };


  // ==========================================================
  // FORMAT SIMILARITY
  // ==========================================================

  const formatSimilarity = (similarity) => {

    return `${(similarity * 100).toFixed(2)}%`;

  };


  return (
    <>

      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="header">

        <div className="header-content">

          <h1>
            AI College Grievance Analyzer
          </h1>

          <p>
            Submit your grievance and let AI analyze and route it.
          </p>

        </div>

      </header>


      {/* =====================================================
          MAIN CONTENT
      ===================================================== */}

      <main className="container">


        {/* ===================================================
            SUBMISSION FORM
        =================================================== */}

        {!result || !result.valid ? (

          <section className="card">

            <h2>
              Submit a Grievance
            </h2>


            <p className="description">

              Describe your issue clearly. Our AI will identify
              the category, severity, and responsible department.

            </p>


            <form onSubmit={submitComplaint}>


              <textarea

                value={complaint}

                onChange={(e) =>
                  setComplaint(e.target.value)
                }

                placeholder="Example: The WiFi in our college library is not working..."

                rows="7"

                maxLength="1000"

              />


              <div className="character-count">

                {complaint.length}/1000

              </div>


              <button

                type="submit"

                disabled={
                  loading ||
                  !complaint.trim()
                }

              >

                {loading
                  ? "Analyzing..."
                  : "Analyze Grievance"}

              </button>


            </form>


            {/* ==============================================
                ERROR MESSAGE
            ============================================== */}

            {result && !result.valid && (

              <p className="error">

                {result.message}

              </p>

            )}

          </section>


        ) : (


          /* =================================================
             SUCCESS SCREEN
          ================================================= */

          <section className="card success-card">


            {/* ==============================================
                SUCCESS ICON
            ============================================== */}

            <div className="success-icon">

              ✓

            </div>


            <h2>

              Grievance Submitted Successfully

            </h2>


            <p className="success-message">

              Your grievance has been analyzed and recorded.

            </p>


            {/* ==============================================
                GRIEVANCE ID
            ============================================== */}

            <div className="grievance-id">

              Grievance ID

              <strong>

                #{result.grievance_id}

              </strong>

            </div>


            {/* ==============================================
                AI CLASSIFICATION RESULTS
            ============================================== */}

            <div className="result-details">


              <div className="result-row">

                <span>
                  Category
                </span>

                <strong>
                  {result.category}
                </strong>

              </div>


              <div className="result-row">

                <span>
                  Severity
                </span>

                <strong>
                  {result.severity}
                </strong>

              </div>


              <div className="result-row">

                <span>
                  Responsible Department
                </span>

                <strong>
                  {result.department}
                </strong>

              </div>


            </div>


            {/* =================================================
                SIMILAR GRIEVANCES
            ================================================= */}

            <div className="similar-grievances">


              <div className="similar-header">

                <div>

                  <h3>
                    Similar Grievances
                  </h3>

                  <p>
                    Previously submitted grievances that are
                    semantically similar to yours.
                  </p>

                </div>


                <div className="similar-count">

                  {result.similar_grievances?.length || 0}

                </div>

              </div>


              {/* ==============================================
                  SIMILAR GRIEVANCE LIST
              ============================================== */}

              {result.similar_grievances &&
              result.similar_grievances.length > 0 ? (

                <div className="similar-list">

                  {result.similar_grievances.map(
                    (grievance) => (

                      <div
                        className="similar-item"
                        key={grievance.id}
                      >


                        {/* ----------------------------------
                            TOP ROW
                        ---------------------------------- */}

                        <div className="similar-item-header">

                          <span className="similar-id">

                            Grievance #{grievance.id}

                          </span>


                          <span className="similarity-badge">

                            {formatSimilarity(
                              grievance.similarity
                            )}

                            {" "}similar

                          </span>

                        </div>


                        {/* ----------------------------------
                            COMPLAINT
                        ---------------------------------- */}

                        <p className="similar-complaint">

                          {grievance.complaint}

                        </p>


                        {/* ----------------------------------
                            CLASSIFICATION
                        ---------------------------------- */}

                        <div className="similar-meta">


                          <span>

                            <strong>
                              Category:
                            </strong>{" "}

                            {grievance.category}

                          </span>


                          <span>

                            <strong>
                              Severity:
                            </strong>{" "}

                            {grievance.severity}

                          </span>


                          <span>

                            <strong>
                              Department:
                            </strong>{" "}

                            {grievance.department}

                          </span>


                        </div>


                      </div>

                    )
                  )}

                </div>


              ) : (


                /* ============================================
                   NO SIMILAR GRIEVANCES
                ============================================ */

                <div className="no-similar">

                  <div className="no-similar-icon">

                    ✓

                  </div>

                  <div>

                    <strong>
                      No similar grievances found
                    </strong>

                    <p>
                      No previous grievance matched this issue
                      closely enough.
                    </p>

                  </div>

                </div>

              )}

            </div>


            {/* =================================================
                SUBMIT ANOTHER
            ================================================= */}

            <button

              className="secondary-button"

              onClick={submitAnother}

            >

              Submit Another Grievance

            </button>


          </section>

        )}

      </main>

    </>

  );

}


// ============================================================
// MAIN APPLICATION
// ============================================================

function App() {

  const [page, setPage] = useState("student");


  return (

    <div className="app">


      {/* =====================================================
          NAVIGATION
      ===================================================== */}

      <nav className="navigation">


        <div className="nav-title">

          Grievance Portal

        </div>


        <div className="nav-buttons">


          <button

            className={
              page === "student"
                ? "nav-active"
                : ""
            }

            onClick={() =>
              setPage("student")
            }

          >

            Student Portal

          </button>


          <button

            className={
              page === "admin"
                ? "nav-active"
                : ""
            }

            onClick={() =>
              setPage("admin")
            }

          >

            Admin Dashboard

          </button>


        </div>


      </nav>


      {/* =====================================================
          PAGE CONTENT
      ===================================================== */}

      {page === "student" ? (

        <StudentPortal />

      ) : (

        <AdminDashboard />

      )}

    </div>

  );

}


export default App;