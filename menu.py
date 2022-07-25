""" A main program to allow user to access all functions using a GUI

    This program imports the main functions of all the modules and links them
    to tkinter GUI widgets so the user can easily call the functions, passing
    inputs from entry boxes and dropdown menus as parameters. Then returning
    the output in a easily readable format on the GUI.
"""
import sys

sys.path.append("modules")
import tkinter as tk
import matplotlib.pyplot as plt
from bookcheckout import book_checkout
from booksearch import book_search
from bookreturn import book_return
from bookweed import book_weed
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def gui_search():
    """ Gets input search results and outputs in a table """
    title = text_entry_title.get()
    output_msg.set("")
    # Clear all rows of table
    treeView.delete(*treeView.get_children())
    # For each result in output, put in row of table
    index = 0
    for book in book_search(choice.get().lower(), title):
        treeView.insert("", index, index, values=book)
        index += 1


def gui_checkout():
    """ Passes inputs to checkout module, shows status message """
    book_id = checkout_bookid.get()
    member_id = checkout_memberid.get()
    # Check user inputs are not empty
    if book_id.strip(" ") == "":
        output_msg.set("Error: Book ID cannot be empty")
    elif member_id.strip(" ") == "":
        output_msg.set("Error: Member ID cannot be empty")
    else:
        # Show checkout status on label
        output_msg.set(book_checkout(member_id, book_id))


def gui_return():
    """ Gets user input and returns return status message """
    book_id = return_bookid.get()
    # Check user input is not empty
    if book_id.strip(" ") == "":
        output_msg.set("Error: Book ID cannot be empty")
    else:
        # Show return status
        output_msg.set(book_return(book_id))


def quit_me():
    """ Closes the window when X button is pressed

    Fixes issue where program will keep running when closed, caused by
    matplotlib
    """
    window.quit()
    window.destroy()


def update_chart():
    """ Produces a set of data based input values

    Calls the book weeding function and updates the bar chart with the values
    returned.
    """
    days = day.get()
    results = result.get()
    # Clear chart
    chart.cla()
    # Get books from weeding algorithm
    books = book_weed(days, results)
    # For each book, add bar to chart with values
    count = 1
    for book in books:
        # Color bar based on its value in comparison to other values
        c = book[1] / books[0][1] / 2
        plt.bar(count, book[1], color=[(.8, c, c)],
                label="{}. {}".format(count, book[0]))
        count += 1
    # Create legend with keys for each bar
    chart.legend(title="Book Titles", loc='upper right', bbox_to_anchor=(2, 1))
    # Create axis labels
    plt.suptitle("{} least loaned book(s) in the last {} days."
                 .format(results, days), fontsize=20, y=0.98)
    plt.xlabel("Book title")
    plt.ylabel("Loans")
    # Add custom ticks so no float values are used
    plt.xticks([n + 1 for n in range(results)])
    plt.yticks([n + 1 for n in range(books[0][1])])
    # Draw chart
    plt.draw()


# Main
window = tk.Tk()
window.title("Library Management System")
window.resizable(False, False)

# Label (Title)
Label(window, text="Library Management System", font=("Helvetica", 16))\
    .pack(expand=1, fill="both", pady=10, padx=10)

# =======================
# ===== TAB CONTROL =====
# =======================
tab_controller = Notebook(window)
# Customer help tab
tab_help = Frame(tab_controller)
tab_controller.add(tab_help, text="Customer Help")
# Book weeding tab
tab_weed = Frame(tab_controller)
tab_controller.add(tab_weed, text="Book Weeding")
tab_controller.pack(expand=1, fill="both")

# ===========================
# ===== Search for book =====
# ===========================
# Book search label frame
lf_search = LabelFrame(tab_help, text="Book Search")
lf_search.grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipadx=5, ipady=5,
               sticky=tk.EW)
lf_search.columnconfigure(0, min=125)
# Dropdown menu
choice = tk.StringVar(lf_search)
dropdown_menu = OptionMenu(lf_search, choice, "Title", "Title", "ISBN",
                           "Author")
dropdown_menu.grid(row=0, column=0, sticky=tk.W)
# Text entry
text_entry_title = Entry(lf_search)
text_entry_title.grid(row=0, column=1, sticky=tk.EW)
# Button
Button(lf_search, text="Search", width=10, command=gui_search)\
    .grid(row=1, column=1, sticky=tk.W)

# =========================
# ===== Checkout book =====
# =========================
# Checkout book Labelframe
lf_checkout = LabelFrame(tab_help, text="Book Checkout")
lf_checkout.grid(row=2, column=0, columnspan=2, padx=5, pady=5, ipadx=5,
                 ipady=5, sticky=tk.EW)
# Label
Label(lf_checkout, text="Enter book ID:", width=20) \
    .grid(row=2, column=0, sticky=tk.W)
Label(lf_checkout, text="Enter member ID:") \
    .grid(row=3, column=0, sticky=tk.W)
# Text entry
checkout_bookid = Entry(lf_checkout, width=20)
checkout_bookid.grid(row=2, column=1, sticky=tk.W)
checkout_memberid = Entry(lf_checkout, width=20)
checkout_memberid.grid(row=3, column=1, sticky=tk.W)
# Button
Button(lf_checkout, text="Checkout", width=10, command=gui_checkout) \
    .grid(row=4, column=1, sticky=tk.W)

# === Book Return ===
# Book return Labelframe
lf_return = LabelFrame(tab_help, text="Book Return")
lf_return.grid(row=3, column=0, columnspan=5, padx=5, pady=5, ipadx=5, ipady=5,
               sticky=tk.EW)
# Label
Label(lf_return, text="Enter book ID:", width=20) \
    .grid(row=2, column=0, sticky=tk.W)
# Text entry
return_bookid = Entry(lf_return, width=20)
return_bookid.grid(row=2, column=1, sticky=tk.W)
# Button
Button(lf_return, text="Return", width=10, command=gui_return) \
    .grid(row=4, column=1, sticky=tk.W)

# ======================
# ===== Output Box =====
# ======================
# Output Labelframe
output_box = LabelFrame(tab_help, text="Output")
output_box.grid(row=1, column=5, columnspan=4, rowspan=4, padx=5, pady=5,
                ipadx=5, ipady=5, sticky=tk.W)
# Table
treeView = Treeview(output_box)
treeView.grid(row=0, column=0, padx=5)
# Scrollbar
vsb = Scrollbar(output_box, orient="vertical", command=treeView.yview)
vsb.grid(row=0, column=1, rowspan=4, sticky=tk.NS)
treeView.configure(yscrollcommand=vsb.set)
# Table column configuration
treeView["columns"] = ["ID", "ISBN", "Title", "Author", "Purchase Date",
                       "Member ID"]
treeView["show"] = "headings"
# Configure table column headers and widths
treeView.heading("ID", text="ID")
treeView.column("ID", width=50, minwidth=50)
treeView.heading("ISBN", text="ISBN")
treeView.column("ISBN", width=100, minwidth=100)
treeView.heading("Title", text="Title")
treeView.column("Title", width=100, minwidth=100)
treeView.heading("Author", text="Author")
treeView.column("Author", width=100, minwidth=100)
treeView.heading("Purchase Date", text="Purchase Date")
treeView.column("Purchase Date", width=100, minwidth=100)
treeView.heading("Member ID", text="Member ID")
treeView.column("Member ID", width=100, minwidth=100)
# Text Output
output_msg = tk.StringVar()
output = Label(output_box, textvariable=output_msg)
output.grid(row=1, column=0, padx=5)

# ========================
# ===== Book Weeding =====
# ========================
# Book weed Labelframe
lf_weed = LabelFrame(tab_weed, text="Book Weeding")
lf_weed.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipadx=5, ipady=5,
             sticky=tk.EW)
# Labels
Label(lf_weed, text="Number of days:", width=20) \
    .grid(row=0, column=0, sticky=tk.W)
Label(lf_weed, text="Number of results:", width=20) \
    .grid(row=1, column=0, sticky=tk.W)
# Days Dropdown Menu
day = tk.IntVar(lf_weed)
num_of_days = OptionMenu(lf_weed, day, 800, 200, 400, 600, 800)
num_of_days.grid(row=0, column=1, sticky=tk.W)
# Results Dropdown menu
result = tk.IntVar(lf_weed)
num_of_results = OptionMenu(lf_weed, result,
                            10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
num_of_results.grid(row=1, column=1, sticky=tk.W)
# Submit Button
Button(lf_weed, text="Update", width=10, command=update_chart) \
    .grid(row=4, column=1, sticky=tk.W)

# =================
# ===== Chart =====
# =================
# Chart frame
chart_frame = Frame(tab_weed)
chart_frame.grid(row=0, column=4, columnspan=5, sticky=tk.E)
# Set figure size and scale
fig = plt.figure(figsize=(8, 4), dpi=60)
# Set background color to look transparent
fig.patch.set_facecolor('grey')
fig.patch.set_alpha(0.12)
chart = fig.add_subplot(1, 1, 1)
# Configure dimensions so all axis and data is visible
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.subplots_adjust(right=0.5)
# Draw canvas
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=1, ipadx=40, ipady=40, sticky=tk.E)
# Fill chart with default values
update_chart()

# Close window
window.protocol("WM_DELETE_WINDOW", quit_me)
# Main Loop
window.mainloop()
