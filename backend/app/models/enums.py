from enum import Enum


# Enum representing the different reading states of a book
class BookStatus(str, Enum):
    # Book is planned to be read
    WANT_TO_READ = "Want to Read"

    # Book is currently being read
    READING = "Reading"

    # Book has been completed
    FINISHED = "Finished"