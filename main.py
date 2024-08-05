books = open("books.txt", "r+", encoding="utf-8")
students = open("students.txt", "r+", encoding="utf-8")

def DisplayMenu():
    print("\n --- LİBRARY APP --- \n")
    print("1. List All Books in the Library ")
    print("2. List All Received Books ")
    print("3. Add a new book ")
    print("4. Delete a book ")
    print("5. Search for Books (ISBN) ")
    print("6. Search for Books (name) ")
    print("7. Get a Book Delivered ")
    print("8. List All Students ")
    print("9. Exit \n")

def MenuLoop():
    while True:

        DisplayMenu()
        option = int(input("Enter a number (1,9): "))
        print()
        if (option >= 1) and (option <= 9):
            break

    return option
def OptionsLoop():
    while True:

        option = MenuLoop()

        if option == 1:
            list_all_books()
        elif option == 2:
            list_borrowed_books()
        elif option == 3:
            add_new_book()
        elif option == 4:
            remove_book()
        elif option == 5:
            search_book_by_isbn()
        elif option == 6:
            search_book_by_name()
        elif option == 7:
            student_receive_book()
        elif option == 8:
            list_all_students()
        elif option == 9:
            exit_program()

def parse_book_line(line):
    parts = line.strip().split(',')
    if len(parts) == 4:
        isbn = parts[0].strip()
        name = parts[1].strip()
        author = parts[2].strip()
        checked_out = parts[3].strip()

        return isbn, name, author, checked_out
    else:
        return None

def list_all_books():
    with open('books.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    all_books = []

    for line in lines:
        book_info = parse_book_line(line)
        if book_info:
            all_books.append(book_info)

    for book in all_books:
        print(book)
def list_borrowed_books():
    with open('books.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    filtered_books = []
    for line in lines:
        book_info = parse_book_line(line)
        if book_info and book_info[3].strip() == 'F':
            filtered_books.append(book_info)

    for borrowed_books in filtered_books:
        print(borrowed_books)

def add_new_book():
    isbn = input("enter ISBN number:  ")
    name = input("enter book name:  ").capitalize()
    author = input("enter author :  ").capitalize()
    checked = input("enter chacked T/F :  ").upper()

    with open("books.txt", "a", encoding="utf-8") as file:
        file.write(f"\n{isbn} , {name} , {author} , {checked}")

        print("\nNew book added successfully ")

def remove_book():
    found = False

    while not found:
        isbn_to_remove = input("Enter the ISBN of the book to remove: ")

        with open('books.txt', 'r+', encoding='utf-8') as file:
            lines = file.readlines()

        with open('books.txt', 'w', encoding='utf-8') as file:
            for line in lines:
                if not line.startswith(isbn_to_remove):
                    file.write(line)
                else:
                    found = True
                    print(f"Book with ISBN {isbn_to_remove} has been removed.")

        if not found:
            print(f"Book with ISBN {isbn_to_remove} not found. Please try again.")

    another = input("Do you want to remove another book? (y/n): ")
    if another.lower() == 'y':
        remove_book()

def search_book_by_isbn():
    search_isbn = input("Enter the ISBN of the book to search: ")

    with open('books.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    found_books = []

    for line in lines:
        book_info = parse_book_line(line)
        if book_info:
            isbn = book_info[0]
            if isbn == search_isbn:
                 found_books.append(book_info)

    if found_books:
        print("Books found with the given ISBN:")
        for book in found_books:
            print(book)
    else:
        print(f"No books found with the ISBN '{search_isbn}'.")

def search_book_by_name():
    search_name = input("Enter the name of the book to search: ")

    with open('books.txt', 'r+', encoding='utf-8') as file:
        lines = file.readlines()

    found_books = []

    for line in lines:
        book_info = parse_book_line(line)
        if book_info:
            name = book_info[1]
            if name.capitalize() == search_name.capitalize():
                found_books.append(book_info)

    if found_books:
        print("Books found with the given name:")
        for book in found_books:
            print(book)
    else:
        print(f"No books found with the name '{search_name}'.")

def student_receive_book():
    student_id = input("Enter the student ID: ")
    isbn_to_receive = input("Enter the ISBN of the book to deliver: ")

    with open('books.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    found = False
    delivered_book_info = None

    with open('books.txt', 'w', encoding='utf-8') as file:
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 4:
                isbn = parts[0].strip()
                name = parts[1].strip()
                author = parts[2].strip()
                checked_out = parts[3].strip()

            if isbn == isbn_to_receive and checked_out == 'T':
                delivered_book_info = (isbn, name, author, 'F')
                found = True
            else:
                file.write(line)

    if found:
        print(f"Book with ISBN {isbn_to_receive} has been delivered to student {student_id}.")

        with open('students.txt', 'r', encoding='utf-8') as student_file:
            student_lines = student_file.readlines()

        with open('students.txt', 'w', encoding='utf-8') as student_file:
            for student_line in student_lines:
                parts = student_line.strip().split(',')
                if parts[0].strip() == student_id:
                    if delivered_book_info:
                        # Append the book information to the student's line
                        student_file.write(f"{student_line.strip()}, {delivered_book_info[1]}\n")
                else:
                    student_file.write(student_line)

    #  update the 'T' ->'F'
    if found and delivered_book_info:
        with open('books.txt', 'a', encoding='utf-8') as file:
            file.write(
                f"{delivered_book_info[0]}, {delivered_book_info[1]}, {delivered_book_info[2]}, {delivered_book_info[3]}\n")

    else:
        print(f"Book with ISBN {isbn_to_receive} not found or already checked out.")

def list_all_students():
    with open('students.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    all_students = []

    for line in lines:
        parts = line.strip().split(',')
        student_id = parts[0].strip()
        student_name = parts[1].strip()

        all_students.append([student_id, student_name])

    if all_students:
        print("List of all students:")
        for student in all_students:
            print(student)
    else:
        print("No students found.")

def exit_program():
    print("Exiting The Library Program... Goodbye!")
    exit()

OptionsLoop()


