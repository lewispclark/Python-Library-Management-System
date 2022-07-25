"""
    A Python module that contains the functions which allow the librarian to
    see the least popular books over a given period of time (used to
    determine which books should be removed from the library).
"""
from database import get_lines, DB_FILE, LOG_FILE, test
import datetime

d = datetime.date


def book_weed(time_period, number):
    """ Finds unpopular books using the logfile

    Checks the date on the logfile and compares it to the current date. If it
    is within the time period the librarian

    :param time_period: Number of days since loan (int)
    :param number: Number of results to return (int)
    :return: List of books (List of Lists)
    """
    books = get_lines(DB_FILE)
    logs = get_lines(LOG_FILE)
    # Create dictionary with each book title as key
    days_since_loans = {}
    for book in books:
        days_since_loans[book[2]] = 0
    # Put logs in chronological order
    logs.reverse()
    # Check if each log is in time period
    for log in logs:
        t = d.today()
        date = datetime.datetime.strptime(log[2].strip("\n"), "%Y-%m-%d").date()
        # Calculate days since last loan
        last_loan = (t - date).days
        if last_loan < time_period:
            days_since_loans[log[0]] += 1
    # Sort books by number of loans
    sorted_loans = sorted(days_since_loans.items(), key=lambda x: -x[1])
    # Return specific amount of most unpopular books
    return sorted_loans[-number:]


# Runs a series of tests on the functions of the module
if __name__ == "__main__":
    tests = []
    # Tests the book_weed function
    tests.append(["[(\"The Hitchhiker's Guide to the Galaxy\", 0)]",
                  book_weed(1, 1)])
    tests.append(["[(\"Alice's Adventures in Wonderland\", 2)]", book_weed(400, 1)])
    tests.append(["[(\"Alice's Adventures in Wonderland\", 5)]",
                  book_weed(1000, 1)])
    # Run tests
    test(tests)
    print("If one of these tests failed it may be because the logfile has been"
          " updated since the test was written.")
