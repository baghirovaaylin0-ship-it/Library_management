class Book:
    def __init__(self, book_id, title, author, year, category):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.available = True


class Member:
    def __init__(self, member_id, name, phone, email):
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.email = email
        self.borrowed_books = []