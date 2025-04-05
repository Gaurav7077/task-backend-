# Task Backend 
## Overview 
This is a Task Management Backend built with Flask, PostgreSQL, Redis, Celery, and Docker. It allows users to manage tasks, upload tasks via CSV, and log task activities. 
## Tech Stack 
- Flask: Backend framework 
- PostgreSQL: Database 
- Redis: Message broker for Celery 
- Celery: Background task processing 
- Docker: Containerization 
## Setup Instructions 
1. Clone the repository: `git clone https://github.com/Gaurav7077/task-backend-.git` 
2. Run `docker-compose up -d --build` to start the services. 
3. Use Postman to test APIs (e.g., `http://localhost:5000/api/task`). 
