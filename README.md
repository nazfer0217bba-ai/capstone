# AI-Driven Automated Test Case Generator for Web Applications

An intelligent web application and library that automatically analyzes web application interfaces (DOM scanning) and parses user stories using Natural Language Processing (NLP) to generate functional, negative, and boundary test cases. 

The system leverages rule-based engines for boundary and logic parsing, coupled with a Machine Learning classifier to automatically prioritize generated test cases based on critical actions and input types.

---

## 🚀 Key Features

*   **DOM Scanner**: Extract forms, inputs, validations (`required`, `minlength`, `maxlength`, types like `email`, `number`), buttons, and dropdowns directly from raw HTML code.
*   **NLP Requirements Parser**: Enter raw user stories (e.g., *"As a user, I want to login with my email and password..."*) to extract roles, actions, target inputs, and validation criteria.
*   **Rule-Based Test Case Engine**: Applies Equivalence Partitioning (EP) and Boundary Value Analysis (BVA) to generate validation, negative, and edge-case test suites.
*   **ML-Based Priority Classifier**: An in-memory Random Forest model that automatically categorizes test cases into `Critical`, `High`, `Medium`, or `Low` priority based on keyword severity and field vulnerability (e.g., payment, authentication, data deletion).
*   **Interactive Streamlit Dashboard**: A dashboard to review element structures, run NLP extraction, view generated tests, and trace test coverage maps.
*   **Multi-Format Exporter**: Download ready-to-use test cases in formatted Excel, CSV, or structured JSON.

---

## 🏗️ Project Architecture

```text
Capstone/
├── README.md                  # Project overview and setup documentation
├── requirements.txt           # Python library requirements
├── .gitignore                 # Standard Git ignored files
├── app.py                     # Streamlit dashboard and UI entrypoint
├── src/
│   ├── __init__.py
│   ├── dom_parser.py          # BeautifulSoup-based DOM analyzer
│   ├── nlp_engine.py          # NLTK / Regex-based User Story parsing
│   ├── testcase_generator.py  # Test case generation logic & ML priority training
│   └── exporter.py            # Pandas & OpenPyXL exporter for Excel/CSV/JSON
└── data/
    └── sample_data.py         # Standard HTML/User story samples for demo purposes
```

---

## 🛠️ Tech Stack

*   **Core Logic**: Python 3.8+
*   **DOM Parsing**: BeautifulSoup4
*   **NLP & Parsing**: NLTK, Regular Expressions
*   **Machine Learning**: Scikit-learn
*   **Data Analysis & Export**: Pandas, OpenPyXL
*   **User Interface**: Streamlit
*   **Visualization**: Plotly

---

## ⚙️ Installation & Usage

1.  **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd Capstone
    ```

2.  **Create and Activate a Virtual Environment (Optional but Recommended)**:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Dashboard**:
    ```bash
    streamlit run app.py
    ```

---

## 🤖 Algorithms & Models

### DOM Parsing Algorithm
Scans raw HTML and compiles metadata for all target fields, matching fields to form boundaries and tracking standard validation rules.

### NLP Model
Tokenizes user stories, detects intent keywords (e.g., "login", "register", "submit"), and extracts noun phrases representing form inputs.

### Machine Learning Classification
Trained on a synthetic benchmark of 100+ standard web test scenarios. The Random Forest classifier scores test descriptions, steps, and target elements to predict priority levels:
-   **Critical**: Operations impacting security (passwords, sessions) or financial actions.
-   **High**: Critical functional paths (form submission, main buttons).
-   **Medium**: Standard field inputs, optional parameters.
-   **Low**: Text readouts, static navigation links, cosmetic validation checks.
