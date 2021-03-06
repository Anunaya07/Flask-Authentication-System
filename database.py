# Creating a list of numbers from 0 to 9.
# =============================================================================
# import necessary libraries
# =============================================================================
from flask_sqlalchemy import SQLAlchemy


# =============================================================================
# initailising database
# =============================================================================
db = SQLAlchemy()


# =================================================================================
# initialising database with app and create the tables in case tables don't exists
# =================================================================================
def db_init(app):
     db.init_app(app)

     with app.app_context():
         db.create_all()