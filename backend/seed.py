from app.models.user import User
from app.models.book import Book, BookStatus
from app.models.shelf import Shelf
from app.models.shelf_share import ShelfShare
from app.models.share_role import ShelfRole
from app.models.lending import Lending
from app.models.activity import Activity

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.core.security import hash_password


db: Session = SessionLocal()


def get_or_create_user(name: str, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if user:
        return user

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print(f"✅ Created user: {email}")

    return user


def create_books(owner: User):
    books = [
        {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "status": BookStatus.READING,
            "pages": 464,
            "rating": 5,
        },
        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "status": BookStatus.WANT_TO_READ,
            "pages": 320,
            "rating": 5,
        },
        {
            "title": "Deep Work",
            "author": "Cal Newport",
            "status": BookStatus.FINISHED,
            "pages": 296,
            "rating": 4,
        },
    ]

    for item in books:
        exists = (
            db.query(Book)
            .filter(
                Book.owner_id == owner.id,
                Book.title == item["title"],
            )
            .first()
        )

        if exists:
            continue

        book = Book(
            title=item["title"],
            author=item["author"],
            status=item["status"],
            total_pages=item["pages"],
            rating=item["rating"],
            owner_id=owner.id,
        )

        db.add(book)

    db.commit()

    print(f"✅ Books created for {owner.email}")

def create_shelves_and_lendings(alice: User, bob: User):
    # 1. Create Shelves for Alice
    shelf_fav = db.query(Shelf).filter(Shelf.name == "Alice's Favorites", Shelf.owner_id == alice.id).first()
    if not shelf_fav:
        shelf_fav = Shelf(name="Alice's Favorites", owner_id=alice.id)
        db.add(shelf_fav)
        
    shelf_read = db.query(Shelf).filter(Shelf.name == "Alice's Reading List", Shelf.owner_id == alice.id).first()
    if not shelf_read:
        shelf_read = Shelf(name="Alice's Reading List", owner_id=alice.id)
        db.add(shelf_read)
        
    db.commit()
    db.refresh(shelf_fav)
    db.refresh(shelf_read)

    # 2. Add some books to Alice's Favorites
    alice_books = db.query(Book).filter(Book.owner_id == alice.id).all()
    if alice_books:
        if alice_books[0] not in shelf_fav.books:
            shelf_fav.books.append(alice_books[0])
            db.commit()

    # 3. Create Shelf Shares (Share with Bob)
    # Share 'Alice's Favorites' with Bob as VIEWER
    share_viewer = db.query(ShelfShare).filter(ShelfShare.shelf_id == shelf_fav.id, ShelfShare.user_id == bob.id).first()
    if not share_viewer:
        share_viewer = ShelfShare(shelf_id=shelf_fav.id, user_id=bob.id, role=ShelfRole.VIEWER)
        db.add(share_viewer)

    # Share 'Alice's Reading List' with Bob as EDITOR
    share_editor = db.query(ShelfShare).filter(ShelfShare.shelf_id == shelf_read.id, ShelfShare.user_id == bob.id).first()
    if not share_editor:
        share_editor = ShelfShare(shelf_id=shelf_read.id, user_id=bob.id, role=ShelfRole.EDITOR)
        db.add(share_editor)
        
    db.commit()
    print("✅ Shelves and Shelf Shares created")

    # 4. Create an active lending: Alice lends a book to Bob
    if len(alice_books) > 1:
        book_to_lend = alice_books[1]
        active_lending = db.query(Lending).filter(Lending.book_id == book_to_lend.id, Lending.returned_at == None).first()
        if not active_lending:
            lending = Lending(
                book_id=book_to_lend.id,
                owner_id=alice.id,
                borrower_id=bob.id
            )
            db.add(lending)
            db.commit()
            print("✅ Lending created (Alice lent a book to Bob)")


def seed():
    print("🌱 Seeding BookNest...")

    alice = get_or_create_user(
        "Alice",
        "alice@example.com",
        "Password@123",
    )

    bob = get_or_create_user(
        "Bob",
        "bob@example.com",
        "Password@123",
    )

    create_books(alice)
    create_books(bob)
    
    create_shelves_and_lendings(alice, bob)

    print("🎉 Users & Books seeded successfully!")


if __name__ == "__main__":
    seed()