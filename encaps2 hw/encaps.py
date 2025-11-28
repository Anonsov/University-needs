from abc import ABC, abstractmethod

class AbstractBook(ABC):
    def __init__(self, title, author, year, copies):
        self._title = title
        self._author = author
        self._year = year
        self._copies = copies

    @abstractmethod
    def get_title(self):
        pass

    @abstractmethod
    def get_author(self):
        pass

    @abstractmethod
    def get_year(self):
        pass

    def get_copies(self):
        return self._copies

    def set_copies(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Copies must be a non-negative integer")
        self._copies = value

    copies = property(get_copies, set_copies)

class Book(AbstractBook):
    def __init__(self, title, author, year, copies):
        super().__init__(title, author, year, copies)

    def get_title(self):
        return self._title

    def get_author(self):
        return self._author

    def get_year(self):
        return self._year

    def __eq__(self, other):
        return isinstance(other, Book) and self._title.lower() == other._title.lower()

    def __hash__(self):
        return hash((self._title, self._author, self._year))

    def __str__(self):
        return f"{self._title} - {self._author} ({self._year}) x{self._copies}"

class EBook(Book):
    def __init__(self, title, author, year, copies, file_size_mb):
        super().__init__(title, author, year, copies)
        self._file_size_mb = file_size_mb

    def get_title(self):
        return self._title + " [EBOOK]"

    def get_file_size(self):
        return self._file_size_mb

class AudioBook(Book):
    def __init__(self, title, author, year, copies, length_minutes):
        super().__init__(title, author, year, copies)
        self._length_minutes = length_minutes

    def get_title(self):
        return self._title + " [AUDIOBOOK]"

    def get_length(self):
        return self._length_minutes

class Library:
    def __init__(self, name, address):
        self._name = name
        self._address = address
        self._books = []
        self._log = []

    def add_book(self, book):
        if not isinstance(book, AbstractBook):
            raise ValueError("Only Book objects can be added")
        for b in self._books:
            if b == book:
                b.copies += book.copies
                self._log.append(f"Updated copies for {b.get_title()}")
                return
        self._books.append(book)
        self._log.append(f"Added {book.get_title()}")

    def remove_book(self, title):
        for b in self._books:
            if b.get_title() == title:
                self._books.remove(b)
                self._log.append(f"Removed {title}")
                return True
        return False

    def find_by_title(self, title):
        return [b for b in self._books if b.get_title() == title]

    def search(self, author=None, title=None):
        result = []
        for b in self._books:
            if author and title:
                if b.get_author() == author and b.get_title() == title:
                    result.append(b)
            elif author:
                if b.get_author() == author:
                    result.append(b)
            elif title:
                if b.get_title() == title:
                    result.append(b)
            else:
                result.append(b)
        return result

    def borrow(self, title):
        for b in self._books:
            if b.get_title() == title and b.copies > 0:
                b.copies -= 1
                self._log.append(f"Borrowed {title}")
                return True
        return False

    def return_book(self, title):
        for b in self._books:
            if b.get_title() == title:
                b.copies += 1
                self._log.append(f"Returned {title}")
                return True
        return False

    def get_books(self):
        return list(self._books)

    def get_log(self):
        return list(self._log)

    def __contains__(self, title):
        return any(b.get_title() == title for b in self._books)

    def __getitem__(self, index):
        return self._books[index]

    def __len__(self):
        return len(self._books)

    def __iter__(self):
        return iter(self._books)

    def __str__(self):
        return f"Library({self._name}, books={len(self._books)}, addr={self._address})"

if __name__ == "__main__":
    lib = Library("Central Library", "Main Street 1")
    lib.add_book(Book("Dune", "Herbert", 1965, 3))
    lib.add_book(EBook("Clean Code", "Martin", 2008, 10, 5))
    lib.add_book(AudioBook("1984", "Orwell", 1949, 1, 600))
    print(lib)
    for book in lib:
        print(book)