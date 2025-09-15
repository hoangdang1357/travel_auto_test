
import os
from flask import Flask, render_template
from auth.routes import auth_bp
from services.routes import services_bp
from admin.routes import admin_bp
from booking.routes import booking_bp
from profile.routes import profile_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(services_bp, url_prefix='/services')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(booking_bp, url_prefix='/booking')
app.register_blueprint(profile_bp, url_prefix='/profile')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Bind to 0.0.0.0 so Render (and other PaaS) can detect the listening port
    app.run(host='0.0.0.0', port=port, debug=False)
