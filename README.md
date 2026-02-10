# NBA Statistics Chatbot

This is a personal project I built to experiment with using large language models to answer NBA-related questions. The chatbot allows users to ask questions about NBA players and league statistics using plain English and returns structured results.

---

## What It Does

* Accepts natural language questions about NBA statistics
* Uses an LLM to understand the user’s intent
* Converts the query into a structured format
* Routes the request to backend functions that return the relevant data

Examples of questions:

* "LeBron James 2023 stats"
* "Top 5 scorers in 2011"
* "Assists leader in 2024"

---

## How It Works (High Level)

1. A user enters a question.
2. The LLM parses the question and produces a structured plan.
3. The plan is matched to a backend function.
4. The function retrieves and formats NBA statistics.

The goal was to keep the system simple while avoiding unreliable free-form LLM answers.

---

## Tech Used

* Python
* LLM frameworks
* JSON

---

## Running the Project

```
pip install -r requirements.txt
python main.py
```

---


## Author

Aryan Bhatia
