# Finance Manager

A personal finance and investment portfolio management web application built with Python and Flask. It helps users manage investments, track market prices, view portfolio performance, and generate financial reports.

## Features

* User registration and login
* Portfolio and investment management
* Stock price tracking using yfinance
* Gold price tracking
* Portfolio value and performance calculation
* Dashboard with financial statistics and charts
* SQLite database for storing user and portfolio data
* PDF financial report generation
* Simple and responsive web interface

## Tech Stack

### Backend

* Python
* Flask
* SQLite

### Data and Finance

* yfinance
* Pandas
* NumPy

### Visualization

* Matplotlib

### PDF Generation

* ReportLab

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2

## Project Structure

```text
Finance-Manager/
|
├── app.py
├── requirements.txt
├── README.md
|
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── portfolio.html
│   └── ...
|
├── static/
│   ├── css/
│   ├── js/
│   └── images/
|
├── database/
│   └── finance.db
|
└── reports/
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/finance-manager.git
cd finance-manager
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open the application at:

```text
http://127.0.0.1:5000
```

## Application Workflow

```text
Register / Login
       |
       v
Dashboard
       |
       v
Add Investments
       |
       v
Fetch Market Data
       |
       v
Calculate Portfolio Value
       |
       v
View Charts and Statistics
       |
       v
Generate PDF Report
```

## Use Cases

The application can be used to:

* Track personal investments
* Monitor stock prices
* Track gold prices
* View portfolio performance
* Maintain investment records
* Generate financial reports

## Future Improvements

* Mutual fund integration
* Advanced portfolio analytics
* Machine learning based predictions
* Profit and loss alerts
* Email notifications
* Multiple portfolio support
* Cloud database integration
* Online deployment

## Security

The application uses authentication and session management for user accounts and portfolio data.

For production use, additional security features such as password hashing, CSRF protection, HTTPS, secure cookies, and environment variables should be implemented.

## Developer

**Krishna Mehta**

Computer Science Undergraduate
Python | Machine Learning | Data Science

## Project Highlights

Finance Manager combines Flask web development, financial data analysis, database management, data visualization, and PDF report generation into one practical application.

It was developed as a project to apply Python and machine learning related skills to a real-world finance use case.

---

If you find the project useful, consider giving the repository a star.
