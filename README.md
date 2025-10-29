# ToDo - Task Management Application

ToDo is a simple yet effective task management application that helps users keep track of their tasks and receive timely email reminders for upcoming deadlines. The application is built with a FastAPI backend and a React frontend, making it a robust and scalable solution.

## Features

*   User authentication (signup, login)
*   Create, view, update, and delete tasks
*   Set due dates and descriptions for tasks
*   Mark tasks as completed
*   Automated email reminders for upcoming tasks (configurable via environment variables)
*   Modern and responsive user interface

## Project Structure

The project is divided into two main parts:

*   `backend/`: Contains the FastAPI application, database models, authentication logic, emailer, and scheduler.
*   `frontend/`: Contains the React application for the user interface.

## Setup Instructions

Follow these steps to set up and run the todo application locally.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd ziedler
```

### 2. Backend Setup

Navigate to the `backend` directory:

```bash
cd backend
```

#### Create a Python Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

#### Activate the Virtual Environment

*   **On Windows (Command Prompt):**
    ```bash
    .\venv\Scripts\activate
    ```
*   **On Windows (PowerShell):**
    ```bash
    .\venv\Scripts\Activate.ps1
    ```
*   **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Database Setup

The application uses SQLite by default. A `todo.db` file will be created automatically in the `backend/` directory when the application runs for the first time.

#### Environment Variables

Create a `.env` file in the `backend/` directory with the following variables. (If you don't want to use `.env` files, you can set these as system environment variables).

```
DATABASE_URL=sqlite:///./todo.db
JWT_SECRET=super-secret-change-me
REMINDER_MINUTES=30
EMAIL_MODE=email

# Only required if EMAIL_MODE is "email"
SMTP_SERVER="smtp.example.com" # e.g., smtp.gmail.com
SMTP_PORT=587 # or 465 for SSL
SMTP_USER="your_email@example.com"
SMTP_PASSWORD="your_email_password_or_app_password"
EMAIL_FROM="your_email@example.com"
```

**How to get SMTP values:**

*   **Gmail:**
    *   `SMTP_SERVER`: `smtp.gmail.com`
    *   `SMTP_PORT`: `587` (TLS) or `465` (SSL)
    *   `SMTP_USER`: Your Gmail address.
    *   `SMTP_PASSWORD`: You'll likely need to generate an **App Password** for your Google account. Go to your Google Account -> Security -> App passwords.

*   **Outlook/Hotmail:**
    *   `SMTP_SERVER`: `smtp-mail.outlook.com`
    *   `SMTP_PORT`: `587`
    *   `SMTP_USER`: Your Outlook email address.
    *   `SMTP_PASSWORD`: Your Outlook password.

#### Run the Backend Server

Ensure your virtual environment is active, then run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at `http://0.0.0.0:8000`.

### 3. Frontend Setup

Open a new terminal, navigate to the `frontend/frontend` directory:

```bash
cd frontend
```

#### Install Dependencies

```bash
npm install
```

#### Run the Frontend Development Server

```bash
npm run dev
```

The frontend application will be available at `http://localhost:5173` (or another port if 5173 is in use).

## Usage

1.  **Register/Login:** Navigate to `http://localhost:5173` and register a new user or log in with existing credentials.
2.  **Manage Tasks:** Create new tasks with titles, descriptions, and due dates. Mark them as complete or delete them.
3.  **Email Reminders:** If `EMAIL_MODE` is set to `email` and SMTP settings are correct, you will receive email reminders for tasks approaching their `due_at` time.

## Technologies Used

*   **Backend:** FastAPI, SQLAlchemy, APScheduler, python-dotenv
*   **Frontend:** React.js, React Router, Axios
*   **Database:** SQLite
*   **Styling:** CSS3

## Contributing

Feel free to fork the repository and contribute! Pull requests are welcome.

## License

This project is open-source and available under the MIT License.
