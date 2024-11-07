from app import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
app = create_app()
migrate = Migrate()
app.init_app()

print(app.extensions)

if __name__ == "__main__":
    app.run(debug=True)
