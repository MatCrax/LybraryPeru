from app import app  # noqa: F401
from utils import populate_initial_data

with app.app_context():
    # Initialize the database with sample data
    populate_initial_data()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
