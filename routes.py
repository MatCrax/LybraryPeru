from flask import render_template, request, redirect, url_for, flash, session, abort, jsonify
from app import app, db
from models import Book, Category, CartItem, Order, OrderItem, User
from sqlalchemy import desc
import logging
from datetime import datetime

# Make some functions available to all templates
@app.context_processor
def utility_processor():
    def get_categories():
        return Category.query.all()

    return dict(get_categories=get_categories)

# Home page
@app.route('/')
def index():
    # Get featured books (most popular based on views, sales, and rentals)
    featured_books = Book.query.order_by(desc(Book.sales + Book.rentals)).limit(6).all()

    # Get bestsellers category
    bestsellers_category = Category.query.filter_by(name="Los más vendidos").first()
    bestsellers = []
    if bestsellers_category:
        bestsellers = Book.query.filter_by(category_id=bestsellers_category.id).order_by(desc(Book.sales)).limit(8).all()

    # Get some categories for the homepage
    categories = Category.query.limit(5).all()

    # Books by category for display
    category_books = {}
    for category in categories:
        category_books[category.name] = Book.query.filter_by(category_id=category.id).limit(4).all()

    return render_template('index.html', 
                           featured_books=featured_books,
                           bestsellers=bestsellers,
                           categories=categories,
                           category_books=category_books)

# Category page
@app.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    books = Book.query.filter_by(category_id=category_id).all()
    return render_template('category.html', category=category, books=books)

# Book detail page
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)

    # Increment view count
    book.views += 1
    db.session.commit()

    # Get related books from the same category
    related_books = Book.query.filter(
        Book.category_id == book.category_id,
        Book.id != book.id
    ).limit(4).all()

    return render_template('book_detail.html', book=book, related_books=related_books)

# Ranking page
@app.route('/ranking')
def ranking():
    # Get top books by sales
    top_sold = Book.query.order_by(desc(Book.sales)).limit(10).all()

    # Get top books by rentals
    top_rented = Book.query.order_by(desc(Book.rentals)).limit(10).all()

    # Get top books by popularity (views, sales, rentals combined)
    books = Book.query.all()
    # Sort by popularity_score property
    popular_books = sorted(books, key=lambda x: x.popularity_score, reverse=True)[:10]

    return render_template('ranking.html', 
                           top_sold=top_sold,
                           top_rented=top_rented,
                           popular_books=popular_books)

# Add to cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    book_id = request.form.get('book_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    is_rental = request.form.get('is_rental') == 'true'

    if not book_id:
        flash('Invalid book selection', 'danger')
        return redirect(request.referrer or url_for('index'))

    # Check if book exists
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found', 'danger')
        return redirect(request.referrer or url_for('index'))

    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []

    # Check if item already in cart
    found = False
    for item in session['cart']:
        if item['book_id'] == book_id and item['is_rental'] == is_rental:
            item['quantity'] += quantity
            found = True
            break

    if not found:
        session['cart'].append({
            'book_id': book_id,
            'quantity': quantity,
            'is_rental': is_rental
        })

    session.modified = True
    flash(f'"{book.title}" added to cart!', 'success')
    return redirect(request.referrer or url_for('index'))

# View cart
@app.route('/cart')
def cart():
    cart_items = []
    total = 0

    if 'cart' in session:
        for item in session['cart']:
            book = Book.query.get(item['book_id'])
            if book:
                price = book.rental_price if item['is_rental'] else book.price
                item_total = price * item['quantity']
                total += item_total

                cart_items.append({
                    'book': book,
                    'quantity': item['quantity'],
                    'is_rental': item['is_rental'],
                    'price': price,
                    'total': item_total
                })

    return render_template('cart.html', cart_items=cart_items, total=total)

# Remove from cart
@app.route('/remove_from_cart/<int:book_id>/<int:is_rental>')
def remove_from_cart(book_id, is_rental):
    is_rental = bool(is_rental)

    if 'cart' in session:
        for i, item in enumerate(session['cart']):
            if item['book_id'] == book_id and item['is_rental'] == is_rental:
                session['cart'].pop(i)
                session.modified = True
                break

    return redirect(url_for('cart'))

# Update cart
@app.route('/update_cart', methods=['POST'])
def update_cart():
    book_id = request.form.get('book_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    is_rental = request.form.get('is_rental') == 'true'

    if 'cart' in session:
        for item in session['cart']:
            if item['book_id'] == book_id and item['is_rental'] == is_rental:
                item['quantity'] = quantity
                session.modified = True
                break

    return redirect(url_for('cart'))

# Checkout page
@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('index'))

    cart_items = []
    total = 0

    for item in session['cart']:
        book = Book.query.get(item['book_id'])
        if book:
            price = book.rental_price if item['is_rental'] else book.price
            item_total = price * item['quantity']
            total += item_total

            cart_items.append({
                'book': book,
                'quantity': item['quantity'],
                'is_rental': item['is_rental'],
                'price': price,
                'total': item_total
            })

    return render_template('checkout.html', cart_items=cart_items, total=total)

# Process order
@app.route('/place_order', methods=['POST'])
def place_order():
    # This would typically involve payment processing, user authentication, etc.
    # For simplicity, we'll just create the order and clear the cart

    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('index'))

    # Calculate total
    total = 0
    cart_items = []

    for item in session['cart']:
        book = Book.query.get(item['book_id'])
        if book:
            price = book.rental_price if item['is_rental'] else book.price
            item_total = price * item['quantity']
            total += item_total

            cart_items.append({
                'book': book,
                'quantity': item['quantity'],
                'is_rental': item['is_rental'],
                'price': price
            })

    # In a real application, we would associate the order with the logged-in user
    # For demo purposes, we'll create a guest order
    order = Order(
        user_id=1,  # Guest user ID (would be current_user.id in a real app)
        total_amount=total,
        status='completed'
    )
    db.session.add(order)
    db.session.flush()  # Get the order ID without committing

    # Create order items
    for item in cart_items:
        book = item['book']

        # Update book sales/rentals count
        if item['is_rental']:
            book.rentals += item['quantity']
        else:
            book.sales += item['quantity']

        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            book_id=book.id,
            quantity=item['quantity'],
            price=item['price'],
            is_rental=item['is_rental'],
            rental_days=30 if item['is_rental'] else 0  # Default rental period
        )
        db.session.add(order_item)

    # Commit all changes
    db.session.commit()

    # Clear cart
    session.pop('cart', None)

    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('index'))

# Search functionality
@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))

    # Search books by title or author
    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) | 
        (Book.author.ilike(f'%{query}%')) |
        (Book.description.ilike(f'%{query}%'))
    ).all()

    return render_template('category.html', 
                           category={'name': f'Search Results for "{query}"'},
                           books=books,
                           query=query)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server error: {e}")
    return render_template('500.html'), 500

# La función para agregar nuevos libros ha sido eliminada según lo solicitado