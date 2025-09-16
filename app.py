
from flask import Flask, render_template
from auth.routes import auth_bp
from services.routes import services_bp
from admin.routes import admin_bp
from booking.routes import booking_bp
from profile.routes import profile_bp
import database

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['DATABASE'] = 'travel.db'
database.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(services_bp, url_prefix='/services')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(booking_bp, url_prefix='/booking')
app.register_blueprint(profile_bp, url_prefix='/profile')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
