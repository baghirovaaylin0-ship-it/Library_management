import re
from datetime import datetime


def validate_id(value):
    return value is not None and str(value).strip().isdigit()


def validate_book_id(book_id):
    return validate_id(book_id)


def validate_member_id(member_id):
    return validate_id(member_id)


def validate_name(name):
    if not isinstance(name, str):
        return False

    return bool(
        re.fullmatch(
            r"[^\W\d_]+(?:\s+[^\W\d_]+)*",
            name.strip()
        )
    )


def validate_phone(phone):
    phone = str(phone).strip()
    return phone.isdigit() and len(phone) == 10


def validate_email(email):
    if not isinstance(email, str):
        return False

    pattern = r"[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}"
    return bool(re.fullmatch(pattern, email.strip()))


def validate_year(year):
    year = str(year).strip()

    if not year.isdigit():
        return False

    return 1000 <= int(year) <= datetime.now().year + 1


def validate_category(category):
    return isinstance(category, str) and bool(category.strip())