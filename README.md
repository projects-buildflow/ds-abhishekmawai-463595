# Cartly - Data Science Virtual Internship

Welcome to **Cartly**, a fast-growing D2C e-commerce company! Over the next 4 weeks, you'll work on real data challenges as a Data Analyst intern, learning Python, pandas, SQL, and data pipeline development.

## Your Mission

Cartly is experiencing rapid growth and their data is a mess. As a new data intern on Priya's team, you'll clean messy datasets, investigate why revenue dropped, write SQL queries, and build data pipelines that the company will actually use.

## Project Structure

```
cartly-data/
├── data/                   # Sample datasets (orders, customers, products)
├── scripts/                # Utility scripts
│   └── verify_setup.py     # Task 1.1 verification
├── src/                    # Source code modules
├── tests/                  # Automated tests for your submissions
├── submissions/            # Your work goes here
└── requirements.txt        # Python dependencies
```

## Prerequisites

- **Python** 3.8+ ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/))
- **VS Code** (recommended) with Python extension

## Quick Start

### 1. Clone Your Repository

```bash
git clone <your-repo-url>
cd cartly-<your-username>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Setup (Task 1.1)

```bash
python scripts/verify_setup.py
```

If successful, you'll receive a verification token. Submit it on your dashboard.

## Tech Stack

- **Python 3.11** - Primary language
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **pytest** - Testing framework
- **pandera** - Data validation
- **matplotlib/seaborn** - Visualization

## Weekly Overview

### Week 1: Onboarding (150 XP)
Set up your environment, fix a data deduplication bug, fix a date parsing bug, and write documentation.

### Week 2: Data Quality (300 XP)
Profile messy marketing data, write validation schemas with Pandera, build a cleaning pipeline.

### Week 3: Analysis (350 XP)
Investigate why October revenue dropped 15%, write SQL cohort queries, optimize slow queries, build dashboards.

### Week 4: Capstone (450 XP)
Design and implement an end-to-end data pipeline, debug AI-generated code, present your work.

## Team Contacts (AI Personas)

Your team members will guide you through the internship:

- **Priya Sharma** (Data Lead) - Code reviews, best practices, technical mentorship
- **Vikram Nair** (Product Manager) - Business context, requirements, stakeholder needs

## Submitting Your Work

### Token Tasks (Task 1.1)
1. Run the verification script
2. Copy the token from the output
3. Submit the token on your dashboard

### Code Tasks (Most Tasks)
1. Create a new branch: `git checkout -b task-1.2`
2. Make your changes in the `submissions/` folder
3. Commit: `git commit -m "Complete task 1.2: Fix deduplication bug"`
4. Push: `git push -u origin task-1.2`
5. Create a Pull Request on GitHub
6. Tests run automatically - AI review provides feedback

### Branch Naming
Your branch should include the task number:
- `task-1.2` (simple)
- `task-1.2-fix-dedup` (with description)
- `feature/1.2-deduplication` (alternative format)

## Available Commands

| Command | Description |
|---------|-------------|
| `python scripts/verify_setup.py` | Verify environment setup |
| `pytest tests/test_X_Y.py -v` | Run tests for task X.Y |
| `ruff check .` | Check code style |
| `black .` | Format code |

## Troubleshooting

### Virtual environment issues
```bash
# Recreate the environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Module not found" errors
```bash
# Make sure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Tests failing locally
```bash
# Run specific test with verbose output
pytest tests/test_1_2.py -v -s
```

## Resources

- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
- [Real Python Tutorials](https://realpython.com/)

---

**Ready to start?** Run `python scripts/verify_setup.py` to complete Task 1.1!

Good luck, and welcome to Cartly!
