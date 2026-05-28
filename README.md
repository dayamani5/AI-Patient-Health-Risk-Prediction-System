# AI-Powered Patient Health Risk Prediction System

## Overview

This project is a Flask-based healthcare web application developed for the Junior AI/ML Developer assessment.

The system manages patient blood-test records and generates AI-style health risk predictions using glucose, haemoglobin, and cholesterol values.

---

## Features

* Create, view, update, and delete patient records
* Input validation for:

  * Email address
  * Date of birth
  * Numeric blood-test values
* Persistent SQLite database storage
* AI-style health risk prediction logic
* Low / Moderate / High risk classification
* Dashboard analytics cards
* Risk badges and remarks
* Search by patient name or email
* Filter records by risk level
* Responsive and professional UI

---

## Tech Stack

* Python
* Flask
* SQLite
* SQLAlchemy
* HTML
* CSS
* Bootstrap

---

## AI Prediction Logic

The application analyzes:

* Glucose
* Haemoglobin
* Cholesterol

Based on these values, the system generates:

* Health remarks
* Risk classification
* AI-style prediction summary

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

## Project Highlights

* CRUD functionality
* Healthcare dashboard
* Rule-based AI prediction system
* Search and filtering
* Professional UI design
* SQLite persistent storage

---

## Disclaimer

This project is developed for educational assessment purposes only and is not intended for real medical diagnosis.
