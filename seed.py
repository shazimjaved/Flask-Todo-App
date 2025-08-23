from app import create_app, db
from app.models import TODO
from datetime import date, timedelta

app = create_app()

with app.app_context():
    if TODO.query.count() == 0:
        todos = [
            TODO(title='Buy groceries', description='Milk, Bread, Eggs, Cheese', due_date=date.today() + timedelta(days=1), status='Pending'),
            TODO(title='Read a book', description='Finish reading Flask documentation', due_date=date.today() + timedelta(days=3), status='Pending'),
            TODO(title='Workout', description='30 minutes of cardio', due_date=date.today(), status='Completed'),
        ]
        db.session.bulk_save_objects(todos)
        db.session.commit()
        print('Seeded the database with example TODOs.')
    else:
        print('Database already seeded.') 