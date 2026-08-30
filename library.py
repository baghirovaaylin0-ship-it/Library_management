from models import Book, Member


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def add_book(self, book):
        self.books.append(book)

    def delete_book(self, book_id):
        book = self.find_book(book_id)

        if book:
            self.books.remove(book)
            return True

        return False

    def edit_book(self, book_id, title, author, year, category):
        book = self.find_book(book_id)

        if not book:
            return False

        book.title = title
        book.author = author
        book.year = year
        book.category = category
        return True

    def view_books(self):
        return self.books

    def add_member(self, member):
        self.members.append(member)

    def delete_member(self, member_id):
        member = self.find_member(member_id)

        if member:
            self.members.remove(member)
            return True

        return False

    def edit_member(self, member_id, name, phone, email):
        member = self.find_member(member_id)

        if not member:
            return False

        member.name = name
        member.phone = phone

        return True

    def view_members(self):
        return self.members

    def borrow_book(self, member_id, book_id):
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        if not member or not book:
            return False

        if not book.available:
            return False

        book.available = False
        member.borrowed_books.append(book_id)
        return True

    def return_book(self, member_id, book_id):
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        if not member or not book:
            return False

        if book_id not in member.borrowed_books:
            return False

        member.borrowed_books.remove(book_id)
        book.available = True
        return True

    def statistics(self):
        available = 0
        categories = {}

        for book in self.books:
            if book.available:
                available += 1
                categories[book.category] = categories.get(book.category, 0) + 1

        most_category = None

        if categories:
            most_category = max(categories, key=categories.get)

        return {
            "Total Books": len(self.books),
            "Available Books": available,
            "Borrowed Books": len(self.books) - available,
            "Total Members": len(self.members),
            "Most Category": most_category
        }