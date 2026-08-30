import json
from models import Book, Member


def save_books(books):
    data = [
        {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "category": book.category,
            "available": book.available
        }
        for book in books
    ]

    with open("books.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_books():
    try:
        with open("books.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    books = []

    for item in data:
        book = Book(
            item["book_id"],
            item["title"],
            item["author"],
            item["year"],
            item["category"]
        )

        book.available = item.get("available", True)
        books.append(book)

    return books


def save_members(members):
    data = [
        {
            "member_id": member.member_id,
            "name": member.name,
            "phone": member.phone,
            "email": member.email,
            "borrowed_books": member.borrowed_books
        }
        for member in members
    ]

    with open("members.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_members():
    try:
        with open("members.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []

    members = []

    for item in data:
        member = Member(
            item["member_id"],
            item["name"],
            item["phone"],
            item["email"]
        )

        member.borrowed_books = item.get("borrowed_books", [])
        members.append(member)

    return members