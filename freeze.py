# freeze.py
from flask_frozen import Freezer
from main import app

freezer = Freezer(app)

@freezer.register_generator
def search():
    for keyword in ["python", "typescript", "javascript", "rust"]:
        yield {'keyword': keyword}

if __name__ == '__main__':
    freezer.freeze()