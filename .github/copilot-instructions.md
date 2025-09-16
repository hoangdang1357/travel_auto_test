# Copilot Instructions for travel_auto_test

## Project Overview
This is a modular Flask web application for travel booking and management. The codebase is organized by feature domains (auth, admin, booking, profile, services) with each domain having its own routes and templates. The app uses a SQLite database (`travel.db`) and supports user authentication, profile management, booking, and admin service management.

## Architecture & Patterns
- **Feature-based structure:**
  - Each major feature (auth, admin, booking, profile, services) is a subdirectory with its own `routes.py` and `__init__.py`.
  - Templates are grouped by feature in `templates/<feature>/`.
- **App entrypoint:**
  - Main Flask app is in `app.py`.
  - Database helpers are in `database.py`.
- **Testing:**
  - Unit tests are in `tests/` and use `unittest`.
  - Tests often create and clean up a test database (`test.db`).
  - Example: `test_auth.py` signs up, signs in, edits profile, and verifies DB changes.
- **Database:**
  - Schema is defined in `database.sql`.
  - Use `init_db()` from `database.py` to initialize DB in tests and app context.

## Developer Workflows
- **Run the app:**
  - `python app.py` (ensure `travel.db` exists or is initialized)
- **Run tests:**
  - `python -m unittest discover tests`
  - Tests will auto-create and delete `test.db`.
- **Database migration:**
  - Use `alter_table.py` for schema changes.
- **Static files:**
  - CSS is in `static/css/style.css`.

## Conventions & Integration
- **Routes:**
  - All routes are defined in `<feature>/routes.py`.
  - Auth routes: `/auth/signup`, `/auth/signin`.
  - Profile edit: `/profile/edit` (expects POST with `full_name`, `phone`, `address`).
- **Templates:**
  - Use Jinja2 templates in `templates/`.
  - Base template: `templates/base.html`.
- **Database access:**
  - Use `get_db_connection()` from `database.py`.
- **Test isolation:**
  - Tests should not affect production DB; always use `test.db`.

## Example Patterns
- **Test pattern:**
  ```python
  def setUp(self):
      app.config['TESTING'] = True
      app.config['DATABASE'] = 'test.db'
      self.app = app.test_client()
      with app.app_context():
          init_db()
  ```
- **Profile update verification:**
  ```python
  response = self.app.post('/profile/edit', data={...}, follow_redirects=True)
  self.assertIn(b'Profile updated successfully!', response.data)
  with app.app_context():
      conn = get_db_connection()
      customer = conn.execute('SELECT * FROM customers WHERE email = ?', (...)).fetchone()
      conn.close()
      self.assertEqual(customer['full_name'], 'New Name')
  ```

## Key Files & Directories
- `app.py`: Main Flask app
- `database.py`: DB helpers
- `database.sql`: Schema
- `alter_table.py`: Migration script
- `tests/`: Unit tests
- `templates/`: Jinja2 templates
- `static/`: Static assets

---
**Feedback requested:** Please review and suggest additions or clarifications for any workflows, conventions, or integration points that are unclear or missing.