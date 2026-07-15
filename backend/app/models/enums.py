from enum import Enum


class BookStatus(str, Enum):
    WANT_TO_READ = "Want to Read"
    READING = "Reading"
    FINISHED = "Finished"