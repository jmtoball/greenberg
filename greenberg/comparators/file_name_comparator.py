from os import path
from difflib import SequenceMatcher
from greenberg.comparators import Comparator

class FileNameComparator(Comparator):

    def compare(self):
        return SequenceMatcher(None,
            path.basename(self.path_one),
            path.basename(self.path_two)
        ).ratio()
