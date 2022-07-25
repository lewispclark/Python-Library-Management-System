"""
    A Python module which contains the functions that allow the librarian to
    search for a book based on its title, isbn or author. Since user commonly
    make mistakes in their input it will search for books that closely match
    their search, rather than checking for exact matches.
"""
from database import get_lines, DB_FILE, test
import difflib


def get_book_dicts():
    """ Gets all the books from the database

    Gets all lines from the database and converts them into dictionaries
    with each each value being a property of the book (e.g title, isbn, etc..)

    :return: All books in the database (List of Dictionaries)
    """
    books = get_lines(DB_FILE)
    # Convert each book (list) into a dictionary
    dicts = []
    for book in books:
        bk = {
            "id": book[0],
            "isbn": book[1],
            "title": book[2],
            "author": book[3],
            "purchase_date": book[4],
            "member_id": book[5].strip("\n")
        }
        dicts.append(bk)
    return dicts


def book_search(fltr, search):
    """ Gets all books from the database that are similar to the search

    Checks each book in the database to see if the user input is similar to
    the book property they are filtering the results by.

    :param fltr: Attribute to compare (String)
    :param search: User input to compare to book attribute (String)
    :return: List of books that match search (List of Dictionaries)
    """
    books = get_book_dicts()
    # Add difference ratio attribute to each book to compare input to attribute
    for book in books:
        book["ratio"] = str(difflib.SequenceMatcher(None, book[fltr].lower(),
                                                    search.lower()).ratio())
    # Sort searches by highest ratio, then by member_id to show available books
    sorted_search = reversed(sorted(books, key=lambda k: (k["ratio"],
                             -int(k["member_id"]))))
    # Remove results from list with ratio lower than 0.5
    output = []
    for result in sorted_search:
        if float(result["ratio"]) >= 0.5:
            output.append(result)
    # Turn each dictionary into list then return all lists
    return [list(r.values()) for r in output]


# Runs a series of tests on the functions of the module
if __name__ == "__main__":
    tests = []
    # Tests get_book_dicts (only part of return selected to be concise)
    tests.append(["1", get_book_dicts()[0]["id"]])
    tests.append(["The Gruffalo", get_book_dicts()[0]["title"]])
    tests.append(["3810280135779", get_book_dicts()[0]["isbn"]])
    tests.append(["Julia Donaldson", get_book_dicts()[0]["author"]])
    tests.append(["02/04/2018", get_book_dicts()[0]["purchase_date"]])
    # Tests book_search (only part of return selected to be concise)
    tests.append(["The Gruffalo", book_search("id", "1")[0][2]])
    tests.append(["[]", book_search("id", "str")])
    tests.append(["The Gruffalo", book_search("title", "The Gruffalo")[0][2]])
    tests.append(["The Gruffalo", book_search("title", "Gruff")[0][2]])
    tests.append(["[]", book_search("title", "akakakakkakaka")])
    tests.append(["Julia Donaldson",
                  book_search("author", "Julia Donaldson")[0][3]])
    tests.append(["Julia Donaldson",
                  book_search("author", "Julia")[0][3]])
    tests.append(["Julia Donaldson",
                  book_search("author", "Donaldson")[0][3]])
    tests.append(["[]",
                  book_search("author", "akakakakkaka")])
    # Run tests
    test(tests)
