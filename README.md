# Task Management Backend

## 📂 File Structure

Here's the structure of the project repository:

```
task-backend/
│
├── app/                      # Flask application code
│   ├── __init__.py           # Initialize the Flask app
│   ├── models.py             # Database models (Task, User, etc.)
│   ├── routes.py             # API routes for tasks
│
├── config/                   # Configuration files
│   ├── config.py             # App configurations (e.g., database URI)
│   └── docker-compose.yml    # Docker compose configuration
│
├── migrations/               # Database migrations
│   ├── versions/             # Migration versions
│
├── screenshots/              # Screenshots folder (place your screenshots here)
│   ├── setup1.png            # Screenshot 1 (Setup instructions)
│   ├── api_example.png       # Screenshot 2 (API example)
│
├── .gitignore                # Git ignore file
├── Dockerfile                # Docker configuration for app container
├── docker-compose.yml        # Docker Compose config file
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```
![Screenshot.png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot.png)

## 🚀 Overview

Welcome to the **Task Management Backend** repository! This project provides a backend system for managing tasks using **Flask**, **PostgreSQL**, **Redis**, **Celery**, and **Docker**. It supports creating tasks, uploading tasks via CSV, logging task activities, and executing long-running background tasks efficiently.

### Features:

- **Task Creation**: Easily create and manage tasks via RESTful APIs.
- **CSV Upload**: Upload tasks in bulk via CSV for efficient task creation.
- **Task Logging**: Real-time logging and tracking of task activities.
- **Background Processing**: Handle long-running tasks asynchronously using **Celery** and **Redis**.
- **Dockerized**: Fully containerized with Docker for easy deployment.

## 🛠 Tech Stack

The application is built with the following technologies:

- **Flask**: Lightweight Python web framework for building APIs
- **PostgreSQL**: Relational database for persistent task storage
- **Redis**: In-memory data store for managing task queues with **Celery**
- **Celery**: Asynchronous task queue for handling background jobs
- **Docker**: Containerization platform to package and deploy the application
- **Gunicorn**: WSGI HTTP Server for serving the Flask app

## 📸 Screenshots

Here are step-by-step screenshots for setting up and using the application. You can check them out from the `screenshots/` folder.

### Step 1: Docker Setup

![Screenshot (11).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(11).png)  

### Step 2: Test API with Postman

![Screenshot (6).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(6).png)
![Screenshot (7).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(7).png)
![Screenshot (8).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(8).png)
![Screenshot (10).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(10).png)  

## 🏗 Setup Instructions

Follow these steps to get the project up and running on your local machine:

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Gaurav7077/task-backend-.git
```

### 2. Install Dependencies

Navigate to the project directory:

```bash
cd task-backend
```

Then, build and start the Docker containers:

```bash
docker-compose up -d --build
```

This will start the required services including Flask, PostgreSQL, Redis, and Celery.

### 3. Running the Application

Once the containers are up and running, you can access the APIs locally:

- **Flask API**: [http://localhost:5050](http://localhost:5050)

### 4. Testing the APIs

Use **Postman** or any other API client to test the following endpoints:

#### Endpoints:

- `POST /api/task`: Create a new task.
- `GET /api/task`: Get a list of all tasks.
- `GET /api/task/{id}`: Get details of a specific task by its ID.
- `POST /api/task/csv`: Upload tasks in bulk via CSV file.

📸 Screenshot:  
![Screenshot (3).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(3).png)
![Screenshot (4).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(4).png)
![Screenshot (5).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(5).png)
![Screenshot (9).png](https://github.com/Gaurav7077/task-backend-/blob/main/Screenshots/Screenshot%20(9).png)


## ⚙️ Usage

Once the application is set up, you can use the following example APIs to interact with the system:

### Task Creation

Create a new task by sending a `POST` request to `/api/task` with the task data.

Example request:

```bash
POST /api/task
Content-Type: application/json

{
  "name": "Sample Task",
  "due_date": "2025-04-15",
  "priority": "high"
}
```

### Task List

Retrieve all tasks with a `GET` request to `/api/task`.

Example request:

```bash
GET /api/task
```

### Task CSV Upload

Upload tasks in bulk using the `POST` request to `/api/task/csv`.

Example request:

```bash
POST /api/task/csv
Content-Type: multipart/form-data

<CSV File>
```

## 🧑‍🤝‍🧑 Contributing

We welcome contributions from everyone! If you’d like to contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Create a new pull request.

## 👨‍💻 Author

**Gaurav [@Gaurav7077](https://github.com/Gaurav7077)**  
---
