"""
    A Python module which contains common functions that the book search,
    checkout, return and weeding modules use to interact with the database and
    log files.
"""
DB_FILE = "database.txt"
LOG_FILE = "logfile.txt"


def get_lines(filename):
    """ Gets all lines from specified file and converts into a List of Lists

    :return: All lines from file (List of lists)
    """
    # Check if file exists
    try:
        with open(filename, "r") as file:
            # Convert each line into a list
            lines = [line.split(",") for line in file.readlines()]
        return lines
    except FileNotFoundError:
        return []


def find_book_by_id(book_id):
    """ Looks for a book with a certain id in the database

    :param book_id: id of the book to search for (string)
    :return: Information on a book ([String])
    """
    with open(DB_FILE, "r") as search:
        # Cycle through each line in the document
        for line in search:
            # Turn each line into a list
            line = line.split(",")
            if line[0] == book_id:
                # If book exists with id, return book
                return line
        return []


def update_db(book, member_id):
    """ Updates the member id of a specific book in the database

    :param book: book to be changed (List)
    :param member_id: member id to be added (String)
    """
    # Update book member_id
    book[5] = member_id + "\n"
    with open(DB_FILE, "r") as db:
        all_lines = db.readlines()
    # Edit line with chosen book
    all_lines[int(book[0]) - 1] = ",".join(book)
    # Update file
    with open(DB_FILE, "w") as db:
        db.writelines(all_lines)


def update_lf(logs):
    """ Updates logfile with new logs

    :param logs: new logs to write to file (List of strings)
    :return: update status (String)
    """
    with open(LOG_FILE, "w") as logfile:
        logfile.writelines(logs)
    return "Book successfully returned"


def test(all_tests):
    """ Checks the expected value of a function against the actual value

    Used to run tests on the modules of the program

    :param all_tests: actual values and expected values (List of Lists)
    """
    counter = passed = failed = 0
    for t in all_tests:
        print("'{}' should be '{}'".format(t[0], t[1]))
        if str(t[0]) == str(t[1]):
            # If expected value is same as actual value
            passed += 1
            print("Test {} passed".format(counter))
        else:
            failed += 1
            print("Test {} failed".format(counter))
        counter += 1
    print("{} / {} tests passed".format(passed, counter))
    print("{} / {} tests failed".format(failed, counter))


# Runs a series of tests on the functions of the module
if __name__ == "__main__":
    tests = []
    # Test get_lines function (only part of return selected to be concise)
    tests.append(["The Gruffalo", get_lines(DB_FILE)[0][2]])
    tests.append(["Animal Farm", get_lines(LOG_FILE)[0][0]])
    tests.append(["[]", get_lines("a")])
    # Test the find_book_by_id function
    tests.append(["[]", find_book_by_id("0")])
    tests.append(["[]", find_book_by_id(1)])
    tests.append(["[]", find_book_by_id("str")])
    tests.append(["The Gruffalo", find_book_by_id("1")[2]])
    # Test update_db function (only part selected to be concise)
    update_db(find_book_by_id("1"), "1234")
    tests.append(["1234", find_book_by_id("1")[5].strip("\n")])
    update_db(find_book_by_id("1"), "0")
    tests.append(["0", find_book_by_id("1")[5].strip("\n")])
    # Tests for the update_lf function are done in the bookreturn.py module.
    # Run tests
    test(tests)
