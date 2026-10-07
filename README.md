# AI College Grievance Analyzer

An AI-powered college grievance management system that automatically analyzes student complaints, classifies them by category, severity, and responsible department, and identifies semantically similar previous grievances.

The system combines **NLP, Machine Learning, Semantic Similarity, FastAPI, React, and PostgreSQL** into an end-to-end grievance analysis platform.

---

## 🚀 Features

### 🤖 AI-Powered Grievance Classification

The system automatically predicts:

- **Complaint Category**
- **Severity / Priority**
- **Responsible Department**

Example:

> "The WiFi in our college library is not working."

```text
Category    : Technical
Severity    : Urgent
Department  : IT

🔍 Semantic Similarity Detection
Each valid grievance is converted into a 384-dimensional Sentence Transformer embedding.
The system compares the new complaint against previously submitted grievances and identifies semantically similar complaints.
Example:
New Complaint:
"The hostel drinking water supply has stopped and students cannot get water."

Similar Previous Complaint:
"The drinking water supply in the hostel is not working properly."

Similarity:
77.03%

This helps administrators identify:
- Duplicate complaints
- Recurring problems
- Related grievances
- Potential systemic issues
✅ Input Validation
The system prevents meaningless or irrelevant submissions using semantic similarity-based validation.
Examples:
"WiFi is down"                  → Valid
"WiFi in the library is broken" → Valid
"asdfghjkl"                     → Invalid
"capital of France"             → Invalid
"buy a new phone"               → Invalid

📊 Admin Dashboard
Administrators can:
- View submitted grievances
- Search complaints
- Filter by category
- Filter by severity
- Filter by responsible department
- View complete grievance details
- Inspect similar grievances
🗄️ PostgreSQL Database
Grievances are persisted in PostgreSQL along with:
- Complaint text
- Category
- Severity
- Responsible department
- Similarity information
- Semantic embedding
- Timestamp
🧠 Machine Learning Pipeline
The project uses different approaches for different prediction tasks.
                    Student Complaint
                           │
                           ▼
                  Input Validation
                           │
                           ▼
                 Sentence Transformer
                           │
                    384-D Embedding
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
       Category       Department      Similarity
       Classifier      Classifier       Search
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    Category + Complaint
                           │
                           ▼
                    TF-IDF Features
                           │
                           ▼
                 Severity Classifier
                           │
                           ▼
                  Grievance Result
                           │
                           ▼
                    PostgreSQL

📈 Model Performance
Experiments were performed using the University Students Complaints Dataset.
The reported results are measured on the project's fixed test split of 59 samples and should not be interpreted as generalization performance on unseen real-world data.

Task	Model	Accuracy
Category	TF-IDF + Logistic Regression	79.66%
Category	TF-IDF + Linear SVM	86.44%
Category	MiniLM Embeddings + Linear SVM	91.53%
Department	MiniLM Embeddings + Linear SVM	81.36%
Severity	MiniLM Embeddings + Linear SVM	49.15%
Severity	TF-IDF + Logistic Regression	59.32%
Severity	TF-IDF + Linear SVM	55.93%
Severity	Category + Complaint + TF-IDF + Logistic Regression	61.02%
Severity	Category + Complaint + Aspects	57.63%


Best-performing models
Category Classification
Sentence Transformer:
all-MiniLM-L6-v2

↓

Linear SVM

↓

Accuracy: 91.53%

Department Classification
Sentence Transformer:
all-MiniLM-L6-v2

↓

Linear SVM

↓

Accuracy: 81.36%

Severity Classification
Category + Complaint

↓

TF-IDF

↓

Logistic Regression

↓

Accuracy: 61.02%

Severity prediction is intentionally treated as a more difficult task because severity is highly context-dependent and the available dataset is relatively small and imbalanced.
🧪 Dataset
The project uses the:
University Students Complaints Dataset
Source:
https://huggingface.co/datasets/alaminxpro/university-students-complaints
The dataset contains 332 complaint records:
Training samples : 273
Testing samples  : 59

Original dataset fields include:
ID
Timestamp
Gender
Semester
Student_Dept
Complaint_Description
Category
Responsible_Departments
Primary_Department
Aspects
Severity
Complaint_Group_ID

Category Distribution
The training dataset contains:
Category	Samples
Infrastructure	114
Technical	58
Academic	48
Finance	29
Administrative	24


Severity Distribution
Severity	Samples
Urgent	97
Medium	79
High	75
Low	22


The dataset is used for research and experimentation. Dataset attribution and licensing information should be preserved when redistributing the dataset.
🏗️ System Architecture
┌───────────────────────────┐
│       React Frontend      │
│                           │
│  Student Portal           │
│  Admin Dashboard          │
└─────────────┬─────────────┘
              │
              │ HTTP / REST
              ▼
┌───────────────────────────┐
│       FastAPI Backend     │
│                           │
│  /predict                 │
│  /grievances              │
└─────────────┬─────────────┘
              │
      ┌───────┴────────┐
      ▼                ▼
┌──────────────┐ ┌─────────────────┐
│ ML Pipeline  │ │ PostgreSQL      │
│              │ │                 │
│ MiniLM       │ │ Grievances      │
│ Linear SVM   │ │ Embeddings      │
│ TF-IDF       │ │ Metadata        │
│ Logistic Reg │ │ Timestamps      │
└──────────────┘ └─────────────────┘

🛠️ Technology Stack
Frontend
- React
- Vite
- JavaScript
- CSS
Backend
- Python
- FastAPI
- Uvicorn
Machine Learning
- scikit-learn
- Sentence Transformers
- NumPy
- Pandas
- Joblib
NLP
- sentence-transformers/all-MiniLM-L6-v2
- TF-IDF
- Linear SVM
- Logistic Regression
- Cosine Similarity
Database
- PostgreSQL
Development
- VS Code
- Git
- GitHub
📁 Project Structure
AI-College-Grievance-Analyzer/
│
├── ai/
│   ├── dataset/
│   │   ├── raw/
│   │   ├── processed/
│   │   ├── categories.json
│   │   └── grievances.csv
│   │
│   ├── preprocessing/
│   │   ├── inspect_dataset.py
│   │   ├── analyze_dataset.py
│   │   ├── check_duplicates.py
│   │   └── prepare_dataset.py
│   │
│   ├── training/
│   │   ├── train_category_baseline.py
│   │   ├── train_category_svm.py
│   │   ├── train_category_embeddings.py
│   │   ├── train_department_embeddings.py
│   │   ├── train_severity_embeddings.py
│   │   ├── train_severity_context.py
│   │   └── ...
│   │
│   ├── models/
│   │   ├── category_embedding_classifier.joblib
│   │   ├── department_embedding_classifier.joblib
│   │   ├── severity_context_classifier.joblib
│   │   └── ...
│   │
│   └── prediction/
│       ├── embedding_model.py
│       ├── predict.py
│       ├── input_validator.py
│       └── similarity.py
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── grievance_repository.py
│   ├── backfill_embeddings.py
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── AdminDashboard.jsx
│   ├── package.json
│   └── ...
│
├── docs/
├── tests/
├── .gitignore
└── README.md

⚙️ Installation
1. Clone the repository
git clone https://github.com/RajAvinash7/AI-College-Grievance-Analyzer.git
cd AI-College-Grievance-Analyzer

2. Create a Python virtual environment
Windows:
python -m venv .venv

Activate it:
.venv\Scripts\activate

3. Install Python dependencies
If a requirements.txt file is present:
pip install -r requirements.txt

Otherwise install the required packages:
pip install fastapi uvicorn pandas numpy scikit-learn sentence-transformers joblib psycopg2-binary

🗄️ PostgreSQL Setup
Install PostgreSQL and create the database:
CREATE DATABASE college_grievance;

The backend expects PostgreSQL to be available on:
Host: localhost
Port: 5432
Database: college_grievance

Configure your local database credentials in:
backend/database.py

Never commit your actual database password or other credentials to GitHub.
For production, environment variables should be used instead.
▶️ Running the Backend
From the project root:
uvicorn backend.main:app --reload

The API will be available at:
http://127.0.0.1:8000

FastAPI documentation:
http://127.0.0.1:8000/docs

▶️ Running the Frontend
Open another terminal:
cd frontend
npm install
npm run dev

The frontend will normally be available at:
http://localhost:5173

🔌 API Endpoints
Predict Grievance
POST /predict

Example request:
{
  "complaint": "The WiFi in our college library is not working."
}

Example response:
{
  "valid": true,
  "complaint": "The WiFi in our college library is not working.",
  "category": "Technical",
  "severity": "Urgent",
  "department": "IT",
  "grievance_id": 7
}

The response can also contain semantically similar previous grievances.
Get Grievances
GET /grievances

Returns stored grievances for the administrative dashboard.
🔍 Semantic Similarity
The system uses:
sentence-transformers/all-MiniLM-L6-v2

to generate a 384-dimensional semantic embedding for each valid grievance.
Similarity is calculated using cosine similarity.
Conceptually:
Complaint A
     │
     ▼
MiniLM
     │
384-dimensional vector
     │
     ▼
Cosine Similarity
     ▲
     │
384-dimensional vector
     │
     MiniLM
     ▲
     │
Complaint B

The current similarity search uses a threshold of:
0.60

and returns up to the top 3 similar grievances.
🎯 Example Workflow
Step 1 — Student submits complaint
"The WiFi in our college library is not working."

Step 2 — Input validation
Valid Complaint ✓
Similarity: 0.88

Step 3 — AI classification
Category:
Technical

Severity:
Urgent

Department:
IT

Step 4 — Semantic similarity search
The system searches previous grievances for related complaints.
Step 5 — Store grievance
The complaint and its embedding are stored in PostgreSQL.
Step 6 — Admin dashboard
Administrators can view and analyze the grievance.
📊 Current Results
The current prototype demonstrates:
- 91.53% category classification accuracy
- 81.36% department classification accuracy
- 61.02% severity classification accuracy
- Semantic similarity for recurring/related complaints
- PostgreSQL persistence
- FastAPI REST API
- React student portal
- React administrative dashboard
- Input validation for irrelevant complaints
⚠️ Limitations
The current system is a research/prototype implementation.
Dataset Size
The available dataset contains only 332 records, which limits the reliability of model evaluation and real-world generalization.
Severity Classification
Severity is significantly harder to classify than category because urgency often depends on contextual information.
The current severity model achieves:
61.02%

on the fixed test split.
Department Classification
Some departments have very few examples, which makes reliable classification difficult for rare classes.
Similarity Threshold
The current duplicate/related grievance threshold is manually configured at:
0.60

A larger dataset would allow more rigorous threshold calibration and evaluation.
Authentication
The current prototype does not yet implement a complete production-grade authentication and authorization system.
Production Scalability
Large-scale deployment would require additional work around:
- Authentication
- Authorization
- Database indexing
- Embedding storage/search optimization
- Monitoring
- Logging
- Rate limiting
- Security
- Model versioning
🔮 Future Work
Potential improvements include:
- Fine-tuning transformer models on college grievance data
- Increasing the size and diversity of the training dataset
- Better severity classification
- Automatic duplicate detection
- Recurring issue detection
- Grievance clustering
- Department-wise analytics
- Trend analysis
- Admin override and feedback loops
- Human-in-the-loop classification
- Authentication and role-based access control
- Vector database integration
- Automated grievance routing
- LLM-powered grievance summarization
- Analytics dashboard
- Production deployment
📚 Dataset Reference
University Students Complaints Dataset:
https://huggingface.co/datasets/alaminxpro/university-students-complaints
The dataset is licensed under CC BY 4.0. Appropriate attribution should be retained when using or redistributing the dataset.
👨‍💻 Author
Avinash Raj
B.Tech Information Technology
Bharati Vidyapeeth College of Engineering, Pune
GitHub:
https://github.com/RajAvinash7
📄 License
This project is currently intended for academic and research purposes.
See the repository for applicable project and dataset licensing information.
⭐ If you find this project useful
Consider giving the repository a ⭐ on GitHub!
