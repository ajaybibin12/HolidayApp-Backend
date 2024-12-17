# Holiday Management Application - Backend

This is the **Django Backend** for the Holiday Management Application. It fetches holiday data from the Calendarific API, caches results, and serves responses via a RESTful API built using Django REST Framework (DRF).

## Features
1. Fetch holiday data from the Calendarific API.
2. Custom API endpoint to search holidays by name.
3. Caching to reduce redundant API calls.
4. SQLite for database storage.

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Django
- Django REST Framework
- python virtual env ( python -m venv 'env')

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-repo/holiday-management-app.git

```
### Step 2: Create a Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### Step 3: Install Dependencies
```
pip install -r requirements.txt 
```

### Step 4: Set Up Environment Variables

```
    Create a .env file in the backend/ directory and add the following:

    CALENDARIFIC_API_KEY=your_calendarific_api_key_here
````

### Step 5: Apply Migrations
 ```
python manage.py makemigrations
python manage.py migrate

```
### Step 6: Run the Server

you can start the server using following command
``` python manage.py runserver 9000 ```
