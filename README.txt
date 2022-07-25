To run tests on each module, it must be run from the menu.py folder since they 
use the relative location of the database.txt and logfile.txt files. These will
not be accessed properly if the modules are run from the modules folder as this
is not the place the program would normally be run from. An example of correct
use would be "python modules/bookcheckout.py" instead of doing "cd modules", 
then "python bookcheckout.py"

== menu.py ==
Allows the user to access all the functions through a tkinter GUI.

Has 2 tabs that allow navigation between the book search, checkout and return
screen and the book weeding screen. This stops the screens from getting too
crowded.

The user can easily see all the book search results in a neatly formatted 
table.

If there are more results than the table can fit on its rows, the
user can use the scrollbar to scroll through the table.

Error and success messages are shown on a label below the table when required, 
then hidden after the next successful operation

The book weeding algorithm outputs results to an embedded matplotlib bar
chart that can be updated with different criteria. This allows the librarian
to see a certain amount of the least popular books over a given time frame.

== database.py ==
List comprehension used instead of for loops to make code more concise

Functions reused for reading logs and database lines

LOG_FILE and DB_FILE kept as constants in one file so can be easily changed in
one place

== booksearch.py ==
Book search finds books with title close to what user searched, not for an
exact match. So user error will not stop the program from functioning
correctly. Results are filtered by what results are closest to user input
so most relevant titles will appear first. If there are multiple results for a
single title then they are sorted by member id, so available books are shown
first. User is also to search for a book by a book id or isbn, this adds
extra functionality and allows the user to search for a book even if they do
not know the title of the book.

== bookweed.py ==
Books are filtered by how many times they have been loaned in a given time
frame, then a specific number of books are returned, depending on the function
parameters