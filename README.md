# Delivery-System-Generator

## Repository Description: Python Script for Data Generation

This repository contains Python code for generating large synthetic datasets and configuring a local PostgreSQL database.  
The script automatically creates database tables, generates realistic sample data (100,000+ records per table), and loads them into PostgreSQL using SQLAlchemy.

The generated data can be used for:
- Business Intelligence (BI) tool testing  
- ETL pipeline prototyping  
- SQL practice on realistic datasets  
- Performance benchmarking
  
---


## Features
### Automatic table creation
The script creates the following tables (with suffix `3`):
- **Customers3**
- **Lockers3**
- **Items3**
- **Orders3**
- **ItemToOrder3**
- **WaybillsToOrder3**
- **StatusToWaybills3**

All tables are dropped and recreated on each run.

### Large-scale synthetic data generation
The script generates:

| Table | Rows | Description |
|-------|------|-------------|
| Customers3 | 100,000 | Random Polish names, cities, phones, emails |
| Lockers3 | 100,000 | Random locker locations |
| Items3 | 100,000 | Random item names |
| Orders3 | 100,000 | Random customer–locker assignments |
| ItemToOrder3 | ~300,000–500,000 | 1 order → 1–4 items |
| WaybillsToOrder3 | variable | 1 order → 1–N waybills |
| StatusToWaybills3 | variable | Shipment statuses with timestamps |

### Realistic shipment lifecycle simulation
Waybill statuses follow a realistic timeline:
- `waybill wygenerowany`
- `nadano`
- `w drodze`
- `dostarczono`
- `odebrano`

With logic such as:
- 95% of old shipments end with "odebrano"
- Random delays between stages
- Occasional long delays (up to 20 days)


## Requirements
- Python 3.9+
- PostgreSQL (local or remote)
- Required Python packages:
  - `psycopg2`
  - `sqlalchemy`
  - `pandas`
  - `faker`
  - `barnum`


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
The script will:
- Generate all datasets
- Create all tables
- Insert all generated data into PostgreSQL


## Repository Structur
- create_sql_tables.py  (Main script for data generation and table creation)
- README.md (Project documentation)
- requirements.txt (Python dependencies)








