# Travel Auto Test - Flask App

This is a simple **Flask + SQLite** travel booking web application.

## 🚀 How to run locally

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd travel_auto_test-gemini
   ```

2. Create virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python app.py
   ```
   Open browser at `http://127.0.0.1:5000`

---

## 🌐 Deploy on Railway

1. Push this repo to GitHub.
2. Go to [Railway](https://railway.app) → New Project → Deploy from GitHub Repo.
3. Add environment variable:
   ```
   PORT = 8000
   ```
4. Railway will build and run using:
   ```
   gunicorn app:app
   ```
5. After deploy, Railway gives you a public URL like:
   ```
   https://your-app.up.railway.app
   ```

---

## 📂 Project Structure

- `app.py` → main Flask app
- `database.py` → database connection
- `travel.db` → SQLite database
- `templates/` → HTML templates
- `static/` → CSS/JS/Assets
- `requirements.txt` → dependencies
- `Procfile` → for deployment
- `.gitignore` → ignore files

---

✅ Ready to run locally or deploy online!
