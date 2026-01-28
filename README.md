# Student Study Portal

A Django-based student study portal for organizing notes, homework, todos, course assignments, announcements, and study tools (dictionary, wiki, books search, YouTube search, unit & currency conversion).

This README is tailored to the repository structure and settings in this project (Django 5.x, dotenv, dj-database-url, Whitenoise, Crispy Forms).

---

## Features

- User registration, login, and profile (Django auth)
- Notes grouped into named collections (image upload supported)
- Homework and todo tracking per user
- User profiles (one-to-one UserProfile)
- Assignments app for lecturers and students:
  - Lecturers (is_staff) can create assignments & announcements and grade submissions
  - Students can view assignments and submit text/files
- Small study tools: Google Books search, dictionary lookup, Wikipedia summaries, YouTube metadata search (yt-dlp), unit & currency conversion (ExchangeRate API)
- Admin site enabled
- Static file handling via WhiteNoise for production

---

## Repo layout (key files)

- manage.py
- requirements.txt
- render.yaml (Render deployment config)
- studentstudyportal/
  - settings.py
  - urls.py
- dashboard/ (main app)
  - apps.py, models.py, forms.py, views.py, urls.py, admin.py
- assignments/ (assignments app)
  - models.py, forms.py, views.py, urls.py
- static/ (static assets)
- media/ (uploaded files — configured as MEDIA_ROOT)

---

## Quick start (development)

1. Clone the repo

   git clone https://github.com/nuraddeen2014/student-study-portal.git
   cd student-study-portal

2. Create and activate a virtual environment

   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1

3. Install dependencies

   pip install -r requirements.txt

4. Create a .env file at the project root with the required environment variables (example below).

5. Apply migrations and create a superuser

   python manage.py migrate
   python manage.py createsuperuser

6. (Optional) Collect static files for production testing

   python manage.py collectstatic --noinput

7. Run the development server

   python manage.py runserver
   Open http://127.0.0.1:8000/

---

## Environment variables (.env.example)

Create a .env file with at least the following keys:

SECRET_KEY=replace-with-secret
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key_here

Notes:
- settings.py uses python-dotenv to load environment variables and dj-database-url for DATABASE_URL.
- For production set DEBUG=False and configure ALLOWED_HOSTS and a production database (eg. Postgres).

---

## Important commands

- Run migrations: python manage.py migrate
- Create admin: python manage.py createsuperuser
- Run server: python manage.py runserver
- Collect static files: python manage.py collectstatic
- Run tests (if tests exist): pytest or python manage.py test

---

## Deployment notes

- The project contains a render.yaml for deploying to Render. Configure environment variables there.
- Whitenoise is configured in settings.py to serve static files in production; STATICFILES_STORAGE is set to CompressedManifestStaticFilesStorage.
- For media files in production, consider using cloud storage (S3, etc.).
- Use a production-ready DB (Postgres) and set DATABASE_URL accordingly.

---

## Security & permissions

- Lecturers are represented by is_staff=True; assign staff status carefully via the admin.
- Keep SECRET_KEY and API keys out of version control (.env should be ignored).
- Validate uploaded files and consider file size/type limits.

---

## Extending the project

- Add Enrollment and Course models to tie assignments and notes to courses and students.
- Add pagination, search, and filtering for large lists.
- Add Django REST Framework API endpoints for a SPA or mobile client.
- Add tests and CI (GitHub Actions) for better reliability.

---

## Contributing

1. Fork the repository
2. Create a feature branch: git checkout -b feature/my-feature
3. Commit your changes and push
4. Open a pull request with a clear description and tests when applicable

---

## License

Add a LICENSE file to the repository. MIT is a common choice.

---

Maintainer

https://github.com/nuraddeen2014

---