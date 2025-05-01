from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    cart_items = db.relationship('CartItem', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    books = db.relationship('Book', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    cover_url = db.Column(db.String(500))  # URL to book cover image
    isbn = db.Column(db.String(20), unique=True)
    publisher = db.Column(db.String(100))
    publication_date = db.Column(db.Date)
    price = db.Column(db.Float, nullable=False)
    rental_price = db.Column(db.Float)  # Price for renting
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    views = db.Column(db.Integer, default=0)  # For popularity tracking
    sales = db.Column(db.Integer, default=0)  # Number of times sold
    rentals = db.Column(db.Integer, default=0)  # Number of times rented
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.title}>'
    
    @property
    def popularity_score(self):
        # Calculate popularity based on views, sales, and rentals
        return (self.views * 0.3) + (self.sales * 0.5) + (self.rentals * 0.2)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    is_rental = db.Column(db.Boolean, default=False)  # True if rental, False if purchase
    book = db.relationship('Book', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem book_id={self.book_id} quantity={self.quantity}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, completed, cancelled
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def __repr__(self):
        return f'<Order id={self.id} status={self.status}>'


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)  # Price at time of order
    is_rental = db.Column(db.Boolean, default=False)
    rental_days = db.Column(db.Integer, default=0)  # Only applicable if is_rental is True
    book = db.relationship('Book', backref='order_items')
    
    def __repr__(self):
        return f'<OrderItem book_id={self.book_id} quantity={self.quantity}>'
