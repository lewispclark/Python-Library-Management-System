"""
    A Python module which contains the functions that allow the librarian to
    return books using the unique id of the book.
"""
from database import find_book_by_id, update_db, get_lines, LOG_FILE, test, \
    update_lf
import datetime

d = datetime.date


def book_return(book_id):
    """ Allows the member to return a book that has been loaned

    Checks if book exists in database, then checks if it is on loan. If it is
    on loan, updates database text file so book is returned.

    :param book_id: unique id of the book (string)
    :return: status (string)
    """
    book = find_book_by_id(book_id)
    if not book:
        return "Error: No book found with book_id = %s" % book_id
    elif book[5].strip("\n") == '0':
        return "Error: Book %s is not on loan" % book_id
    else:
        # Update book in database with member_id of 0
        update_db(book, "0")
        logs = get_lines(LOG_FILE)
        for i in range(len(logs)):
            if logs[i][1] == book_id and len(logs[i]) == 3:
                # Add return date to the checkout log
                log = ",".join(logs[i]).strip("\n")
                log += ",{}\n".format(str(d.today()))
                logs[i] = log.split(",")
                break
        # Convert all log lists to strings
        new_logs = [",".join(log) for log in logs]
        # Update logfile
        return update_lf(new_logs)


# Runs a series of tests on the functions of the module
if __name__ == "__main__":
    from bookcheckout import book_checkout
    tests = []
    # Testing the book_return function
    tests.append(["Error: No book found with book_id = 0", book_return("0")])
    tests.append(["Error: No book found with book_id = 1", book_return(1)])
    tests.append(["Error: No book found with book_id = str", book_return("str")])
    book_return("1")
    tests.append(["Error: Book 1 is not on loan", book_return("1")])
    book_checkout("1000", "2")
    tests.append(["Book successfully returned", book_return("2")])
    # Run tests
    test(tests)
