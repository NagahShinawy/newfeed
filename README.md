# newfeed# Flask Blog API

A simple RESTful API built with Flask to manage blog posts. The API allows users to create, read, update, and delete posts. It connects to a MySQL database to store post data.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)

## Features

- Create a new post
- Retrieve a post by ID
- Update a post
- Delete a post
- List all posts

## Technologies Used

- Flask: A lightweight WSGI web application framework in Python.
- MySQL: A popular relational database management system.
- `mysql-connector-python`: MySQL driver for Python.

## Setup Instructions

Follow these steps to set up the project locally:

### Prerequisites

- Python 3.x installed on your machine.
- MySQL Server installed and running.
- A virtual environment (recommended).

### Step 1: Clone the Repository

```bash
git clone https://github.com/NagahShinawy/newfeed

```

### Step 2: Create and Activate a Virtual Environment

```commandline
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```commandline
pip install -r requirements.txt

```

### Step 4: Configure Database
1- Create a MySQL database and user.

2- Update the config.py file with your MySQL credentials.

```python
class Config:
    MYSQL_USER = 'your_mysql_user'
    MYSQL_PASSWORD = 'your_mysql_password'
    MYSQL_HOST = 'localhost'
    MYSQL_DATABASE = 'your_database_name'
    MYSQL_PORT = 3306

```

3- Create the necessary tables in your MySQL database. Here’s a sample SQL statement to create the posts table `newfeed.sql`
```sql
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

```
### 5- Step 5: Run the Application
```commandline
python app.py
```
The API will be accessible at http://127.0.0.1:5000. 
