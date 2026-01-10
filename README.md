# Delivery-System-Generator

## Repository Description: Python Script for Data Generation

This repository contains Python code used for generating data and configuring a local PostgreSQL database. The script enables the creation of tables such as Customers, Items, Lockers, Orders, OrderToWaybills, Waybills, and Statuses, along with populating them with randomly generated data. These data can be utilized for testing and comparative analysis of selected Business Intelligence (BI) tools.

## Features

- Automatic creation of PostgreSQL tables:
  - **Customers**
  - **Items**
  - **Lockers**
  - **Orders**
  - **OrderToWaybills**
  - **Waybills**
  - **Statuses**
- Randomized data generation for each table
- Easy setup for local development and BI tool testing
- Fully configurable connection parameters

---

## Requirements

- Python 3.9+
- PostgreSQL (local instance)
- Required Python packages (install via `pip install -r requirements.txt`):
  - `psycopg2`
  - `faker`
  - `random`
  - any additional dependencies used in the script

---
## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure database connection
Update connection parameters inside create_sql_tables.py:
```Pyhton
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "your_database"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
```

### 4. Run the script
``` bash
python create_sql_tables.py
```
This will:
- Create all required tables
- Populate them with randomly generated data


## Use Cases
- Testing BI tools (Power BI, Tableau, Metabase, etc.)
- Prototyping ETL processes
- Practicing SQL queries on realistic datasets
- Benchmarking database performance



## Repository Structure
├── create_sql_tables.py   # Main script for table creation and data generation
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies







