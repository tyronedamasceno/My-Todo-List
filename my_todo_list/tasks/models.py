from datetime import datetime

from my_todo_list import db


class Task(db.Model):
    """
    Model to represent a task at todo-list. A task has a title, a status
    and possibly a description
    """
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )
    date_posted = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow  # give the function as argument
    )
    status = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )
    description = db.Column(
        db.Text,
        nullable=True
    )

    def __repr__(self):
        return f'Task({self.title}, {self.status})'

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            date_posted=self.date_posted.isoformat(),
            status=self.status,
            description=self.description if self.description else ''
        )
