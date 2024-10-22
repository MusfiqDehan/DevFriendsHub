<div align="center">

<h1>DevFriendsHub 🚀</h1>

A Collection of Developer Friends

<p>
    <img src="https://img.shields.io/badge/React-18.2.66-blue?style=for-the-badge&logo=react" alt="React">
    <img src="https://img.shields.io/badge/Flask-3.0.3-blue?style=for-the-badge&logo=flask" alt="Flask">
    <img src="https://img.shields.io/badge/PostgreSQL-16.0-blue?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
    <img src="https://img.shields.io/badge/SQLAlchemy-2.0.30-blue?style=for-the-badge&logo=sqlalchemy" alt="SQLAlchemy">
    <img src="https://img.shields.io/badge/Chakra%20UI-2.8.2-blue?style=for-the-badge&logo=chakra-ui" alt="Chakra UI">
    <img src="https://img.shields.io/badge/Docker-25.0.2-blue?style=for-the-badge&logo=docker" alt="Docker">

</p>

<p>
<a href="https://devfriendshub.up.railway.app/api/friends">Live Flask API Server</a>
-
<a href="https://hub.docker.com/r/musfiqdehan/devfriendshub-backend">Docker Image</a>
</p>
<p>
<a href="https://devfriendshub.vercel.app">Live React Frontend</a>
-
<a href="https://hub.docker.com/r/musfiqdehan/devfriendshub-frontend">Docker Image</a>
</p>

</div>



## Table of Contents

- [Technology Used](#technology-used)
- [Folder Structure](#folder-structure)
- [Features](#features)
- [Run the App Locally](#run-the-app-locally)
    - [Run Using Docker](#run-using-docker)
    - [Run Backend API Server](#run-backend-api-server)
    - [Run the Frontend Server](#run-the-frontend-server)


## Technology Used

-   **Frontend**:
    -   **React**: A JavaScript library for building user interfaces.
    -   **Chakra UI**: A simple, modular, and accessible component library that gives you the building blocks you need to build your React applications.
-   **Backend**:
    -   **Python**: A programming language that lets you work quickly and integrate systems more effectively.
    -   **Flask**: A lightweight WSGI web application framework.
    -   **PostgreSQL**: A powerful, open-source object-relational database system.
    -   **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
-   **Containerization**:
    -   **Docker**: A platform for developing, shipping, and running applications in containers.
-   **Deployment**:
    -   **Railway**: A platform that allows you to deploy your apps and databases in the cloud.
    -   **Vercel**: A platform for static sites and Serverless Functions.


## Folder Structure

The project is divided into two main directories: `backend` and `frontend`.

```bash
.
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── routes.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   └── main
│   │       ├── __init__.py
│   │       ├── models.py
│   │       └── routes.py
│   ├── Dockerfile.backend
│   ├── migrations
│   ├── requirements.txt
│   ├── run.py
│   └── tests
│       ├── conftest.py
│       ├── __init__.py
│       ├── test_auth.py
│       └── test_main.py
├── frontend
│   ├── Dockerfile.frontend
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── vite.svg
│   ├── README.md
│   ├── src
│   │   ├── App.jsx
│   │   ├── components
│   │   │   ├── CreateUserModal.jsx
│   │   │   ├── EditModal.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── SearchUser.jsx
│   │   │   ├── UserCard.jsx
│   │   │   └── UserGrid.jsx
│   │   └── main.jsx
│   └── vite.config.js
├── LICENSE
├── docker-compose.yml
├── push_to_dockerhub.sh
└── README.md
```


## Features

-   ✅ CRUD Functionality: Seamlessly create, read, update, and delete friends from your store.
-   🔒 Best Practices: Utilizes best practices such as creating virtual environments (venv) for a clean and isolated development environment.
-   🌐 Deployment: Deployed on Railway.
-   🎨 Stylish UI Components: Enhanced user experience with stylish UI components provided by Chakra UI.
-   🌓 Light and Dark Mode: Enjoy a personalized user interface experience with light and dark mode options.
-   📱 Responsive Design: The app is designed to adapt to various screen sizes, ensuring a consistent experience across devices.

## Run the App Locally

### Run Using Docker

```bash
# Pull the images
docker pull musfiqdehan/devfriendshub-backend:latest
docker pull musfiqdehan/devfriendshub-frontend:latest

# Run the backend container
docker run -d -p 5050:5050 musfiqdehan/devfriendshub-backend:latest

# Run the frontend container
docker run -d -p 3000:80 musfiqdehan/devfriendshub-frontend:latest
```

### Run Backend API Server

1. Clone the repository:

```bash
git clone https://github.com/MusfiqDehan/DevFriendsHub.git
```

2. Navigate to the project directory:

```bash
cd DevFriendsHub
```

3. Navigate to the backend directory:

```bash
cd backend
```

4. Create a virtual environment:

-   On macOS and Linux:

```bash
python3 -m venv venv
```

-   On Windows:

```bash
python -m venv venv
```

5. Activate the virtual environment:

-   On macOS and Linux:

```bash
source venv/bin/activate
```

-   On Windows:

```bash
venv\Scripts\activate
```

6. Install the dependencies:

-   On macOS and Linux:

```bash
pip3 install -r requirements.txt
```

-   On Windows:

```bash
pip install -r requirements.txt
```

7. Create a `.env` file in the `backend` directory and add the following environment variables:

```bash
# Flask settings
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key

# PostgreSQL URL
DATABASE_URL=

# AWS S3 settings for production
AWS_STORAGE_BUCKET_NAME=
AWS_LOCATION=
AWS_S3_ACCESS_KEY_ID=
AWS_S3_SECRET_ACCESS_KEY=
AWS_S3_CUSTOM_DOMAIN=
AWS_S3_ENDPOINT_URL=
AWS_S3_FILE_OVERWRITE=
```

8. Run Backend Server

```bash
flask run
```
or
```bash
python app.py
```
9. The backend server will start running on `http://127.0.0.1:3000` or `http://localhost:3000`.

### Run the Frontend Server

1. Open a new terminal.

2. Navigate to the frontend directory:

```bash
cd ../frontend
```

3. Install the dependencies:

```bash
npm install
```

4. Run the frontend app:

```bash
npm run dev
```

5. Open your browser and go to `http://localhost:3000/` or `http://127.0.0.1:3000` to view and Interact with the app.

6. You can now Interact on the app.
