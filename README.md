# Todo App

This is a simple Todo app built with Django REST framework to manage todo lists and their items. It provides a set of API endpoints to create, retrieve, update, and delete todo lists and items.

## Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [Environment Variables](#environment-variables)
3. [API Endpoints](#api-endpoints)
4. [Test Cases](#test-cases)
5. [Running Tests](#running-tests)

---

## Setup Instructions

### 1. Clone the Repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/django-todo-app.git
cd todoserver
```

### 2. Set Up a Virtual Environment
It's a good practice to use a virtual environment to isolate your dependencies. You can create and activate it as follows:

#### For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install all the required dependencies from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Setup Database
Run the following commands to set up the database and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Environment Variables

The application requires database configuration, which are convieniently set using environment variables. You can create a `.env` file in the root directory of the project to store these variables.

### Example `.env` file:

```env
DB_USER=YOUR_DB_USER
DB_PASSWORD=YOUR_DB_PASSWORD
DB_HOST=YOUR_DB_HOST
DB_NAME=YOUR_DB_NAME
DB_PORT=YOUR_DB_PORT
```
---

## API Endpoints

### 1. **GET /lists/**
   - **Description**: Retrieve all todo lists.
   - **Response**:
     ```json
     {
       "lists": [
         {"id": 1, "name": "Test List"}
       ]
     }
     ```

### 2. **POST /lists/**
   - **Description**: Create a new todo list.
   - **Request Body**:
     ```json
     {
       "name": "New List"
     }
     ```
   - **Response**:
     ```json
     {
       "id": 1
     }
     ```

### 3. **GET /lists/<int:pk>/**
   - **Description**: Retrieve details of a specific todo list.
   - **Response**:
     ```json
     {
       "id": 1,
       "name": "Test List",
       "items": [
         {"id": 1, "title": "Test Item", "completed": false, "deadline": null}
       ]
     }
     ```

### 4. **DELETE /lists/<int:pk>/**
   - **Description**: Delete a specific todo list.
   - **Response**: No content (status 204).

### 5. **GET /lists/<int:pk>/items/**
   - **Description**: Retrieve all items in a specific todo list.
   - **Response**:
     ```json
     {
       "items": [
         {"id": 1, "title": "Test Item", "completed": false, "deadline": null}
       ]
     }
     ```

### 6. **POST /lists/<int:pk>/items/**
   - **Description**: Add a new item to a specific todo list.
   - **Request Body**:
     ```json
     {
       "title": "New Item",
       "completed": false,
       "deadline": "2025-01-01"
     }
     ```
   - **Response**:
     ```json
     {
       "id": 2
     }
     ```

### 7. **PATCH /lists/<int:pk>/items/<int:li>/**
   - **Description**: Update an existing todo item.
   - **Request Body**:
     ```json
     {
       "title": "Updated Title",
       "completed": true
     }
     ```
   - **Response**:
     ```json
     {
       "id": 2
     }
     ```

### 8. **DELETE /lists/<int:pk>/items/<int:li>/**
   - **Description**: Delete a specific todo item.
   - **Response**: No content (status 204).

### 9. **DELETE /lists/delete/**
   - **Description**: Delete all todo items across all lists.
   - **Response**: No content (status 204).

---

## Test Cases

Here are the main test cases included in the project to validate the API functionality:

### 1. **Create Todo List**
   - Validates the creation of a new todo list.
   - Checks if the correct response is returned when a valid name is provided.

### 2. **Create Todo List with Missing Name**
   - Ensures that the API returns an error when no name is provided in the request body.

### 3. **Get All Todo Lists**
   - Verifies that the API correctly returns a list of all existing todo lists.

### 4. **Get Todo List Detail**
   - Validates the retrieval of details for a specific todo list, including all its items.

### 5. **Delete Todo List**
   - Ensures the deletion of a todo list and confirms that it no longer exists.

### 6. **Add Item to Todo List**
   - Tests the creation of a new todo item under a specific todo list.

### 7. **Get Items in List**
   - Confirms that all items in a specific todo list can be retrieved.

### 8. **Update Todo Item**
   - Verifies that an existing item can be updated (e.g., title, completed status).

### 9. **Delete Todo Item**
   - Tests that a specific item in a todo list can be deleted.

### 10. **Delete All Todo Items**
   - Ensures that the `/lists/delete` endpoint deletes all items across all lists.

### 11. **Todo List Duplicate Name**
   - Ensures that the API prevents the creation of a todo list with a duplicate name.

---

## Running Tests

To run the test cases for this project, you can use Django's test suite. Run the following command:

```bash
python manage.py test
```

This will automatically discover and run all the tests defined in the `tests.py` file, providing output on the success or failure of each test.
