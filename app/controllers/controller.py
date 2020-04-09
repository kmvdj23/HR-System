from app.config import hr_main
from app.controllers.main import main
from app.controllers.hr import hr
from app.controllers.it import it
from app.controllers.admin import admin
from app.controllers.api import api_v1
from flask import redirect, url_for

# =========== BLUEPRINTS ======================
hr_main.register_blueprint(main)
hr_main.register_blueprint(hr)
hr_main.register_blueprint(it)
hr_main.register_blueprint(admin)
hr_main.register_blueprint(api_v1)


# =========== START ROUTE =====================
@hr_main.route('/')
def start():
	return redirect(url_for('main.login_page'))