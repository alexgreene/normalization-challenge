import csv
import re
from difflib import SequenceMatcher

class Normalizer(object):

    def __init__(self):
        self.manifest_lookup = {}
        pass

    def read_manifest(self, manifest):
        """reads a manifest file

        manifest should be a CSV containing the following columns
            * section_id
            * section_name
            * row_id
            * row_name

        Arguments:
            manifest {[str]} -- /path/to/manifest
        """

        with open(manifest, 'rb') as f:
            seats = csv.reader(f)
            for seat in seats:

                section_id = seat[0]
                section_name = seat[1].lower()
                row_id = seat[2]
                row_name = seat[3].lower()

                # find just the number from the section name
                section_number = re.findall(r'\d+', section_name)

                # sections without numbers will be placed under a generic key -> *
                section_key = section_number[0] if len(section_number) != 0 else '*'

                if section_key not in self.manifest_lookup:
                    self.manifest_lookup[ section_key ] = {}

                # file the section under its number
                if section_name not in self.manifest_lookup[ section_key ]:
                    self.manifest_lookup[ section_key ][ section_name ] = {
                        'section_id': section_id,
                        'rows': {}
                    }

                # add the row to its section
                if row_name:             
                    row_dict = self.manifest_lookup[ section_key ][ section_name ]['rows']   
                    row_dict[ row_name ] = row_id


    def normalize(self, section, row):
        """normalize a single (section, row) input

        Given a (Section, Row) input, returns (section_id, row_id, valid)
        where
            section_id = int or None
            row_id = int or None
            valid = True or False

        Arguments:
            section {[type]} -- [description]
            row {[type]} -- [description]
        """

        section_id = None
        row_id = None
        section = section.lower()

        try:  
            # find the number and then appropriate key that we should lookup 
            # in the manifest
            section_number = re.findall(r'\d+', section)
            section_key = section_number[0] if len(section_number) != 0 else '*'

            possible_sections = self.manifest_lookup[section_key].keys()
            max_ratio = max_index = ratio_words = 0
            max_words = word_index = 0
            backup_index = -1
            
            for i, section_to_compare in enumerate(possible_sections):
                section_to_compare = section_to_compare.lower()

                # determine how 'similar' the two strings are
                new_ratio = SequenceMatcher(None, section, section_to_compare).ratio()

                # knowing if the strings share common words is important
                a = section_to_compare.split()
                b = section.split()
                word_count = len(set(a).intersection(b))

                if new_ratio > max_ratio:
                    max_ratio = new_ratio
                    ratio_words = word_count
                    max_index = i

                if word_count > max_words:
                    max_words = word_count
                    word_index = i

                try:
                    # sometimes section names are abbreviated, so check the first letter
                    # of whatever non-digit characters are available
                    number_free =  ''.join([x for x in section if not x.isdigit()])
                    first_non_digit = number_free.lstrip()[0]
                    if section_to_compare[0] == first_non_digit:
                        backup_index = i

                except IndexError, e:
                    pass

            if max_ratio < .4 and backup_index != -1:
                # if there is little confidence, admit defeat
                max_index = backup_index
            elif ratio_words == 1:
                # if our chosen section shares no common words, change our strategy
                max_index = word_index
            elif section_key == "*" and ratio_words == 0:
                # if we're working w/ a numberless section and there are no common
                # words, we don't have a match
                return (None, None, False)
            elif max_ratio < .15: 
                # if there is little confidence to begin with, admit defeat
                return (None, None, False)

            chosen = possible_sections[max_index].lower();

            # we cannot confidently choose from similarly numbered sections if we are only provided
            # with the numerical aspect of a section name
            if len(possible_sections) > 1 and sum(not c.isdigit() for c in section) == 0:
                return (None, None, False)  

            match = self.manifest_lookup[section_key][chosen]
            section_id = int(match['section_id'])
            row = ( row if len(row) == 1 else row.lstrip("0") ).lower()
            row_id = None if len(match['rows']) == 0 else int(match['rows'][row])

        except KeyError as e:
            return (None, None, False)      

        return (section_id, row_id, True)
