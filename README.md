# MedMate: Secure Personal Medication & Health Concierge Agent

MedMate is a production-quality AI-powered concierge agent that helps users safely manage their medications, identify drug interactions, schedule reminders, and simplify medical prescriptions. Built with the **Google Agent Development Kit (ADK)**, **Gemini 2.5 Flash**, **Streamlit**, and **SQLite**, MedMate focuses on security, privacy, and safety.

## Architecture

```
                       +---------------------------+
                       |       Streamlit UI        |
                       +-------------+-------------+
                                     |
                                     v
                       +-------------+-------------+
                       |   Google ADK Root Agent   |
                       +-------------+-------------+
                                     |
                                     v
                       +-------------+-------------+
                       |    Gemini 2.5 Flash       |
                       +-------------+-------------+
                                     |
                 +-------------------+-------------------+
                 |                   |                   |
                 v                   v                   v
        +--------+--------+ +--------+--------+ +--------+--------+
        | Medication Tool | | Interaction Tool| |  Reminder Tool  |
        +--------+--------+ +--------+--------+ +--------+--------+
                 |                   |                   |
                 +-------------------+-------------------+
                                     |
                                     v
                       +-------------+-------------+
                       |          SQLite           |
                       +---------------------------+
```

## Folder Structure

```
medmate/
│   .env.example
│   .gitignore
│   README.md
│   requirements.txt
│   SPEC.md
│
├───agent/
│   │   instructions.md
│   │   root_agent.py
│   │
│   ├───skills/
│   │       check_interactions.md
│   │       schedule_reminder.md
│   │       summarize_prescription.md
│   │
│   └───tools/
│           add_medication.py
│           database.py
│           interaction_checker.py
│           prescription_summary.py
│           reminder_tool.py
│
├───app/
│       streamlit_app.py
│
├───data/
│       sample_medications.json
│
├───docs/
│       architecture.md
│       security.md
│
└───eval/
        evaluator.py
        results.md
        test_cases.json
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd CapstoneProject/medmate
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and fill in your Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSy...
   ```

## Running the Application

Launch the Streamlit interface:
```bash
streamlit run app/streamlit_app.py
```

## Features

1. **Medication Manager**: Add, list, and remove medications. Uses parameterized queries to store data in a local SQLite file.
2. **Drug Interaction Checker**: Checks interactions via the RxNav API, with a local JSON fallback (`data/sample_medications.json`).
3. **Prescription Summarizer**: Automatically extracts drug details, purposes, dosages, and warnings, simplifying the text into plain language.
4. **Reminder Tool**: Saves reminders for medications, which are displayed in the UI sidebar.
5. **Prompt Injection Protection**: Detects malicious system override prompts, database modification statements, and shell commands, responding with polite refusal.

## Security

MedMate is built on secure design principles:
- **No Unsafe Execution**: No `eval`, `exec`, or `pickle`.
- **SQL Injection Defense**: Every SQLite query is parameterized.
- **Strict Delimiters**: Formats user messages securely inside clean text wrappers.
- **Privacy Minimization**: Minimizes PII; stores only the necessary medication lists.

## Evaluation

Run the evaluation suite to run all 10 test scenarios and automatically generate a results report:
```bash
python eval/evaluator.py
```
This updates the [results.md](path/to/file/medmate/eval/<RESULTS_FILE>.md) file.
