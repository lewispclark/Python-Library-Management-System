"""
    A Python module which contains the functions that allow the librarian to
    checkout books using the customers unique id and the id of the book.
"""
from database import find_book_by_id, update_db, LOG_FILE, test


import datetime


def is_valid(member_id):
    """ Checks if the member id is a valid 4 digit integer

    :param member_id: id of the member (string)
    :return: true or false (bool)
    """
    # Check if member_id is a valid integer
    try:
        member_id = int(member_id)
    except ValueError:
        return False
    # Check if member id is between 999 and 10000
    if member_id < 1000 or member_id > 9999:
        return False
    return True


def book_checkout(member_id, book_id):
    """ Adds member id to the book in the database to show it is loaned

    Checks if the member is is valid and checks if the book exists in the
    database and checks if it is on loan. If the book is available to be
    loaned, updates the database file with members id.

    :param member_id: unique id of the member (string)
    :param book_id: unique id of the book (string)
    :return: status (string).
    """
    # Search for book in database
    book = find_book_by_id(book_id)
    if not is_valid(member_id):
        return "Error: Invalid member ID"
    if not book:
        return "Error: No book found with ID = {}".format(book_id)
    elif book[5].strip("\n") != "0":
        # If book is in database but has member_id, return loan error
        return "Error: Book {} is already on loan".format(book_id)
    else:
        # Update book in datebase with new member_id
        update_db(book, member_id)
        # Add loan to log file
        with open(LOG_FILE, "a") as logfile:
            d = datetime.date
            logfile.write("{},{},{}\n"
                          .format(book[2], book[0], str(d.today())))
        return "Book successfully checked out"


# Runs a series of tests on the functions of the module
if __name__ == "__main__":
    from bookreturn import book_return
    tests = []
    # Testing the is_valid function
    tests.append(["True", is_valid("1234")])
    tests.append(["False", is_valid("12")])
    tests.append(["False", is_valid("str")])
    tests.append(["False", is_valid("")])
    # Testing the book_checkout function
    tests.append(["Error: Invalid member ID", book_checkout("", "1")])
    tests.append(["Error: Invalid member ID", book_checkout("10", "1")])
    tests.append(["Error: Invalid member ID", book_checkout("10000", "1")])
    tests.append(["Error: No book found with ID = 0",
                  book_checkout("1000", "0")])
    tests.append(["Error: No book found with ID = str",
                  book_checkout("1000", "str")])
    book_return("1")
    tests.append(["Book successfully checked out",
                  book_checkout("1000", "1")])
    tests.append(["Error: Book 1 is already on loan",
                  book_checkout("1000", "1")])
    # Run tests
    test(tests)
    book_return("1")
