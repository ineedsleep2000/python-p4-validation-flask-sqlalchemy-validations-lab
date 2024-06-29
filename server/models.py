from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Must have a name')
        if Author.query.filter_by(name=name).first():
            raise ValueError('Name already exists')
        return name
    
    @validates('phone_number')
    def validates_phone_number(self, key, phone_number):
        if phone_number and not phone_number.isdigit() or len(phone_number) !=10:
            raise ValueError('phone number must be 10 digits')
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError("No clickbait found")
        return title
     
    @validates('content')
    def validates_content(self, key, content):
        if content and not len(content) >= 250 :
            raise ValueError('content must be 250 characters or over')
        return content
    
    @validates('summary')
    def validates_summary(self, key, summary):
        if summary and not len(summary) <= 250 :
            raise ValueError('summary must be 250 characters or under')
        return summary
    
    @validates('category')
    def validates_category(self, key, category):
        if category and category not in['Fiction', "Non-Fiction"] :
            raise ValueError('category must be Fiction or Non-Fiction')
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
