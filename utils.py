from app import db
from models import Book, Category, User
from werkzeug.security import generate_password_hash
from datetime import datetime
import logging
import random

def populate_initial_data():
    """Populate the database with initial data if it's empty"""
    
    # Check if we already have categories
    if Category.query.count() > 0:
        return
    
    logging.info("Populating initial data...")
    
    # Lista de URLs de libros que funcionan
    book_covers = [
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1612969308146-066015efc293?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1589998059171-988d887df646?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1467951591042-f388365db261?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1541963463532-d68292c34b19?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1543782248-03e26d5d6e85?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1581856769392-c6d0f48ab98f?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1576504473326-616f4e503bcf?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1617806099500-7dea2ba781d4?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1551029506-0807df4e2031?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1565246029799-f3d562fc5be3?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&h=600&crop=faces",
        "https://images.unsplash.com/photo-1531494391841-6ac2ef3859b8?w=400&h=600&crop=faces"
    ]
    
    # Create categories
    categories = [
        {"name": "Los más vendidos", "description": "Los libros más populares de nuestra tienda"},
        {"name": "Acción", "description": "Libros llenos de aventuras y emociones"},
        {"name": "Novelas", "description": "Las mejores novelas literarias"},
        {"name": "Ciencia Ficción", "description": "Historias futuristas y mundos imaginarios"},
        {"name": "Fantasía", "description": "Mundos mágicos y criaturas fantásticas"},
        {"name": "Románticos", "description": "Historias de amor y romance"},
        {"name": "Historia", "description": "Libros sobre eventos históricos"},
        {"name": "Biografías", "description": "Historias de vida de personas inspiradoras"}
    ]
    
    for cat_data in categories:
        category = Category(name=cat_data["name"], description=cat_data["description"])
        db.session.add(category)
    
    db.session.commit()
    
    # Create fictional books
    books = [
        # Categoría: Los más vendidos (1)
        {
            "title": "El Misterio de la Luna Azul",
            "author": "Carlos Mendoza",
            "description": "Una intrigante historia sobre un fenómeno lunar que cambia la vida de un pequeño pueblo costero en el norte de Perú.",
            "cover_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=400&h=600&auto=format&fit=crop",
            "isbn": "9781234567890",
            "publisher": "Editorial Andina",
            "publication_date": datetime(2023, 5, 15),
            "price": 45.90,
            "rental_price": 15.00,
            "stock": 25,
            "category_id": 1,
            "views": 180,
            "sales": 65,
            "rentals": 28
        },
        {
            "title": "Memorias de un Taxi Limeño",
            "author": "Roberto Sánchez",
            "description": "Relatos divertidos y conmovedores sobre las experiencias de un taxista en las calles de Lima, donde cada pasajero tiene una historia que contar.",
            "cover_url": "https://picsum.photos/seed/book2/400/600",
            "isbn": "9782345678901",
            "publisher": "Perú Literario",
            "publication_date": datetime(2022, 8, 10),
            "price": 38.50,
            "rental_price": 12.00,
            "stock": 30,
            "category_id": 1,
            "views": 160,
            "sales": 58,
            "rentals": 25
        },
        
        # Categoría: Acción (2)
        {
            "title": "El Tesoro de Pachacámac",
            "author": "Miguel Torres",
            "description": "Una trepidante aventura donde un arqueólogo y una periodista deben encontrar un antiguo tesoro inca antes que una peligrosa organización criminal.",
            "cover_url": "https://picsum.photos/seed/book3/400/600",
            "isbn": "9783456789012",
            "publisher": "Aventuras SA",
            "publication_date": datetime(2023, 2, 20),
            "price": 42.90,
            "rental_price": 14.00,
            "stock": 20,
            "category_id": 2,
            "views": 145,
            "sales": 50,
            "rentals": 22
        },
        {
            "title": "Código Andes",
            "author": "Patricia Rojas",
            "description": "Un ex-militar debe desactivar un complot terrorista en las alturas de los Andes peruanos, utilizando su conocimiento del terreno y las culturas locales.",
            "cover_url": "https://picsum.photos/seed/book4/400/600",
            "isbn": "9784567890123",
            "publisher": "Editorial Impacto",
            "publication_date": datetime(2021, 11, 5),
            "price": 40.00,
            "rental_price": 13.50,
            "stock": 18,
            "category_id": 2,
            "views": 130,
            "sales": 45,
            "rentals": 20
        },
        
        # Categoría: Novelas (3)
        {
            "title": "Las Voces del Huascarán",
            "author": "Ana María Gutiérrez",
            "description": "Una conmovedora historia sobre tres generaciones de una familia de la sierra peruana y cómo sus vidas son transformadas por los cambios sociales y políticos del país.",
            "cover_url": "https://picsum.photos/seed/book5/400/600",
            "isbn": "9785678901234",
            "publisher": "Letras Peruanas",
            "publication_date": datetime(2022, 4, 8),
            "price": 39.90,
            "rental_price": 12.50,
            "stock": 22,
            "category_id": 3,
            "views": 150,
            "sales": 49,
            "rentals": 23
        },
        {
            "title": "El Café de los Sueños",
            "author": "Isabel Prado",
            "description": "En un pequeño café del centro histórico de Arequipa, se entrelazan las historias de diversos personajes que buscan cumplir sus sueños más profundos.",
            "cover_url": "https://picsum.photos/seed/book6/400/600",
            "isbn": "9786789012345",
            "publisher": "Sur Editores",
            "publication_date": datetime(2023, 1, 12),
            "price": 36.50,
            "rental_price": 11.00,
            "stock": 25,
            "category_id": 3,
            "views": 135,
            "sales": 42,
            "rentals": 19
        },
        
        # Categoría: Ciencia Ficción (4)
        {
            "title": "Línea Nazca: Contacto Final",
            "author": "Diego Ferrer",
            "description": "En un futuro cercano, las líneas de Nazca revelan ser un mapa para el contacto con una civilización extraterrestre que regresa a la Tierra después de milenios.",
            "cover_url": "https://picsum.photos/seed/book7/400/600",
            "isbn": "9787890123456",
            "publisher": "Órbita Libros",
            "publication_date": datetime(2024, 3, 25),
            "price": 44.90,
            "rental_price": 15.00,
            "stock": 18,
            "category_id": 4,
            "views": 140,
            "sales": 48,
            "rentals": 21
        },
        {
            "title": "Lima 2090",
            "author": "Fernando Castro",
            "description": "En una Lima futurista controlada por inteligencias artificiales, un grupo de rebeldes busca devolver el control a los humanos y descubre un secreto que cambiará la historia de la humanidad.",
            "cover_url": "https://picsum.photos/seed/book8/400/600",
            "isbn": "9788901234567",
            "publisher": "Futuro Presente",
            "publication_date": datetime(2022, 6, 30),
            "price": 43.50,
            "rental_price": 14.50,
            "stock": 20,
            "category_id": 4,
            "views": 125,
            "sales": 40,
            "rentals": 18
        },
        
        # Categoría: Fantasía (5)
        {
            "title": "El Guardián del Amazonas",
            "author": "Lucía Campos",
            "description": "Un joven descubre que es el último de un linaje ancestral de guardianes mágicos cuya misión es proteger los secretos místicos de la selva amazónica de fuerzas oscuras.",
            "cover_url": "https://picsum.photos/seed/book9/400/600",
            "isbn": "9789012345678",
            "publisher": "Magia Andina",
            "publication_date": datetime(2023, 9, 15),
            "price": 41.90,
            "rental_price": 13.00,
            "stock": 25,
            "category_id": 5,
            "views": 155,
            "sales": 52,
            "rentals": 24
        },
        {
            "title": "La Leyenda de Manco Cápac",
            "author": "María Elena Quispe",
            "description": "Una reinterpretación fantasiosa de la leyenda inca, donde Manco Cápac debe enfrentarse a criaturas míticas y dioses antiguos para fundar la ciudad del Cusco.",
            "cover_url": "https://picsum.photos/seed/book10/400/600",
            "isbn": "9780123456789",
            "publisher": "Mitos y Leyendas",
            "publication_date": datetime(2022, 10, 18),
            "price": 39.90,
            "rental_price": 12.00,
            "stock": 20,
            "category_id": 5,
            "views": 130,
            "sales": 45,
            "rentals": 20
        },
        
        # Categoría: Románticos (6)
        {
            "title": "Cartas desde Barranco",
            "author": "Valeria Vega",
            "description": "Una historia de amor que transcurre en el bohemio distrito de Barranco, a través de cartas entre dos jóvenes que nunca se han visto en persona.",
            "cover_url": "https://picsum.photos/seed/book11/400/600",
            "isbn": "9781234509876",
            "publisher": "Corazón Literario",
            "publication_date": datetime(2023, 7, 10),
            "price": 35.90,
            "rental_price": 11.00,
            "stock": 28,
            "category_id": 6,
            "views": 145,
            "sales": 55,
            "rentals": 22
        },
        {
            "title": "El Amor en Tiempos del Café",
            "author": "Javier Martínez",
            "description": "Un barista de Miraflores y una ejecutiva adicta al café desarrollan una conexión especial que les lleva a replantear sus prioridades en la vida.",
            "cover_url": "https://picsum.photos/seed/book12/400/600",
            "isbn": "9782345098765",
            "publisher": "Romántica Peruana",
            "publication_date": datetime(2021, 12, 5),
            "price": 34.50,
            "rental_price": 10.50,
            "stock": 22,
            "category_id": 6,
            "views": 120,
            "sales": 40,
            "rentals": 18
        },
        
        # Categoría: Historia (7)
        {
            "title": "La Guerra del Pacífico: Héroes Olvidados",
            "author": "Eduardo Ramírez",
            "description": "Un recorrido detallado por las historias menos conocidas de los héroes peruanos durante la Guerra del Pacífico y su impacto en la formación de la identidad nacional.",
            "cover_url": "https://picsum.photos/seed/book13/400/600",
            "isbn": "9783456098765",
            "publisher": "Historia Peruana",
            "publication_date": datetime(2022, 11, 22),
            "price": 48.90,
            "rental_price": 16.00,
            "stock": 15,
            "category_id": 7,
            "views": 110,
            "sales": 35,
            "rentals": 14
        },
        {
            "title": "El Virreinato Desconocido",
            "author": "Carmen Delgado",
            "description": "Un análisis de aspectos poco explorados del Virreinato del Perú, revelando la vida cotidiana, las costumbres y el mestizaje cultural que forjaron el Perú moderno.",
            "cover_url": "https://picsum.photos/seed/book14/400/600",
            "isbn": "9784567098765",
            "publisher": "Anales Históricos",
            "publication_date": datetime(2023, 4, 8),
            "price": 46.50,
            "rental_price": 15.50,
            "stock": 18,
            "category_id": 7,
            "views": 105,
            "sales": 32,
            "rentals": 13
        },
        
        # Categoría: Biografías (8)
        {
            "title": "Mario Vargas Llosa: El Hacedor de Mundos",
            "author": "Guillermo Pérez",
            "description": "Biografía no autorizada que explora la vida y obra del Premio Nobel peruano, sus contradicciones, logros literarios y su impacto en la cultura latinoamericana.",
            "cover_url": "https://picsum.photos/seed/book15/400/600",
            "isbn": "9785678098765",
            "publisher": "Biografías Ilustres",
            "publication_date": datetime(2022, 3, 15),
            "price": 49.90,
            "rental_price": 16.50,
            "stock": 20,
            "category_id": 8,
            "views": 130,
            "sales": 42,
            "rentals": 15
        },
        {
            "title": "Gastón Acurio: La Revolución Culinaria",
            "author": "Sofía Torres",
            "description": "Recorrido por la vida del famoso chef peruano, desde sus inicios hasta cómo logró llevar la gastronomía peruana al reconocimiento mundial.",
            "cover_url": "https://picsum.photos/seed/book16/400/600",
            "isbn": "9786789098765",
            "publisher": "Sabor y Letras",
            "publication_date": datetime(2023, 8, 20),
            "price": 44.90,
            "rental_price": 14.50,
            "stock": 22,
            "category_id": 8,
            "views": 125,
            "sales": 38,
            "rentals": 16
        },
        
        # Más libros para categoría Los más vendidos
        {
            "title": "Caminando por Lima",
            "author": "Jorge Bastidas",
            "description": "Un recorrido visual y literario por los rincones más emblemáticos y desconocidos de la capital peruana, con historias de sus habitantes.",
            "cover_url": "https://picsum.photos/seed/book17/400/600",
            "isbn": "9787890098765",
            "publisher": "Lima Cultural",
            "publication_date": datetime(2023, 6, 5),
            "price": 39.90,
            "rental_price": 12.50,
            "stock": 25,
            "category_id": 1,
            "views": 150,
            "sales": 56,
            "rentals": 23
        },
        {
            "title": "Cocina Moderna Peruana",
            "author": "Claudia Rengifo",
            "description": "Un libro de recetas que reinventa los clásicos platos peruanos con técnicas contemporáneas, perfecto para cocineros aficionados y profesionales.",
            "cover_url": "https://picsum.photos/seed/book18/400/600",
            "isbn": "9788901098765",
            "publisher": "Fogón Editorial",
            "publication_date": datetime(2022, 9, 15),
            "price": 52.90,
            "rental_price": 17.00,
            "stock": 18,
            "category_id": 1,
            "views": 165,
            "sales": 60,
            "rentals": 25
        },
        {
            "title": "Emprendimiento Peruano",
            "author": "Ricardo Morales",
            "description": "Guía práctica para emprendedores peruanos con casos de éxito locales, estrategias adaptadas al mercado nacional y consejos para superar obstáculos.",
            "cover_url": "https://picsum.photos/seed/book19/400/600",
            "isbn": "9789012098765",
            "publisher": "Éxito Empresarial",
            "publication_date": datetime(2023, 11, 10),
            "price": 47.90,
            "rental_price": 15.50,
            "stock": 20,
            "category_id": 1,
            "views": 140,
            "sales": 52,
            "rentals": 19
        },
        
        # Más libros de diferentes categorías
        {
            "title": "La Ruta del Pisco",
            "author": "Martín Valdivia",
            "description": "Un recorrido histórico y cultural por las regiones productoras de pisco, con información sobre cómo se elabora y las mejores formas de disfrutarlo.",
            "cover_url": "https://picsum.photos/seed/book20/400/600",
            "isbn": "9780123098765",
            "publisher": "Tradiciones Peruanas",
            "publication_date": datetime(2022, 7, 28),
            "price": 43.90,
            "rental_price": 14.00,
            "stock": 22,
            "category_id": 7,
            "views": 120,
            "sales": 38,
            "rentals": 15
        }
    ]
    
    # Add books to database
    for i, book_data in enumerate(books):
        # Usar URL de portada de la lista predefinida
        book_data["cover_url"] = book_covers[i % len(book_covers)]
        book = Book(**book_data)
        db.session.add(book)
    
    # Create a default guest user
    if User.query.filter_by(username="guest").first() is None:
        guest_user = User(
            username="guest",
            email="guest@libraryperu.com",
            password_hash=generate_password_hash("guest123")
        )
        db.session.add(guest_user)
    
    db.session.commit()
    logging.info("Initial data populated successfully")
