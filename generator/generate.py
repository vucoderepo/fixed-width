"""
    Name: generate.py
    Author: Venu Uppala
    purpose: To create fixed width file and generate csv file from it
"""
import json
import logging

# Initialize logger
logger = logging.getLogger("fixed-width")
logger.setLevel(logging.INFO)
# To log information in console
log_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s"

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_file_format))
logger.addHandler(console_handler)


class FixedWidthFile(object):
    """
        Creates Fixed width records and writes them into fixed width text file
        Also, converts fixed width file into csv file
    """

    def __init__(self):
        self.records = set()
        # Read fixed width configuration json file
        with open("../spec.json") as spec_json:
            self.spec = json.load(spec_json)
        spec_json.close()

    def add_record(self, record):
        """
        Validates given record against spec.json file and saves the record for later use
        :param record: List of values for a fixed width record
        :return: None
        """
        logger.info("Input Record:{}".format(record))
        fwr = FixedWidthRecord(self.spec['Offsets'], record)
        if self.validate_fixed_width_record(fwr):
            self.records.add(fwr)

    def create(self):
        """
        Creates fixed width file with input records. Uses value of
        'FixedWidthEncoding' defined in spec.json file to encode fixed width record
        :return: None
        """
        fixed_width_file = open("fw_file.txt", "wb")

        if len(self.records) > 0:

            logger.info("Start - Generating Fixed-width line file")
            # Add header record
            fwr = FixedWidthRecord(self.spec['Offsets'], self.spec['ColumnNames'])
            fixed_width_file.write((str(fwr) + "\n").encode(self.spec['FixedWidthEncoding']))
            # Data records
            for record in self.records:
                fixed_width_file.write((str(record) + "\n").encode(self.spec['FixedWidthEncoding']))
            fixed_width_file.close()
            logger.info("End - Generating Fixed-width line file")

    def get_field_indexes(self):
        """
        Identifies start and end positions of all columns in fixed width file
        based on offsets defined in spec.json file
        :return: list of start and end positions for all columns in fixed width file
        """
        field_indexes = []
        for index, offset in enumerate(self.spec['Offsets']):
            if index == 0:
                field_indexes.append([0, int(offset)])
            else:
                field_indexes.append([field_indexes[index - 1][1], field_indexes[index - 1][1] + int(offset)])
        return field_indexes

    def convert_to_csv(self):
        """
        Converts fixed width file into csv file. Uses value of
        'FixedWidthEncoding' defined in spec.json file to decode fixed width record,
        and uses value of 'DelimitedEncoding' to encode CSV record
        :return: None
        """
        logger.info("Start-Convert Fixed-width line file to CSV")
        fixed_width_file = open("fw_file.txt", "rb")
        csv_file = open("fw_csv_file.csv", "wb")
        for line in fixed_width_file.readlines():
            record = line.decode(self.spec['FixedWidthEncoding'])
            csv_record = ""
            for indexes in self.get_field_indexes():
                if not csv_record:
                    csv_record = record[indexes[0]:indexes[1]].strip()
                else:
                    csv_record = csv_record + "," + record[indexes[0]:indexes[1]].strip()
            if csv_record:
                csv_file.write((csv_record + "\n").encode(self.spec['DelimitedEncoding']))
        fixed_width_file.close()
        csv_file.close()
        logger.info("End-Convert Fixed-width line file to CSV")

    def validate_fixed_width_record(self, record):
        """
        Checks given input record is according to spec.json file.
        Throws exception if number of values in the given input record are not
        matching with number of columns specified in spec.json file
        :param record: type(FixedWidthRecord)
        :return: True or False
        :raises: type(FixedWidthRecordException) if input record is not according to spec.json file
        """
        is_valid_record = False
        if record:
            if not record.values:
                raise FixedWidthRecordException("Values of fields are empty in Fixed width record")
            if len(record.values) != len(self.spec['ColumnNames']):
                raise FixedWidthRecordException("Number of field values are not matching with number "
                                                "of columns in spec.json file")
            is_valid_record = True
        return is_valid_record


class FixedWidthRecord(object):
    """
    Creates and formats values of input record according fixed width convention.
    Adjusts values of fields to right, leaving spaces to left
    """

    """
    :param offsets - Offsets specified in spec.json file
    :param values - input record of type list
    """

    def __init__(self, offsets, values):
        self.offsets = [int(i) for i in offsets]
        self.values = values

    """
    Formats values of fields to right according to fixed width convention
    """

    def __str__(self):
        return "".join("%*s" % i for i in zip(self.offsets, self.values))


class FixedWidthRecordException(Exception):
    """Base exception class for Fixed width record"""
    pass


if __name__ == '__main__':
    # Create Fixed width object
    gfw = FixedWidthFile()

    # Input records
    record_1 = [1, "TWO", 3, 4, 5, 6, 7, 8, 9, 10]
    record_2 = ['abcde', 'abcdefghijkl', 'abc', 'ab', 'abcdefghijklm', 'abcdefg',
                'abcdefghij', 'abcdefghijkln', 'abcdefghijabcdefghij', 'abcdefghijklo']

    gfw.add_record(record_1)
    gfw.add_record(record_2)

    # Create Fixed width file
    gfw.create()
    with open("fw_file.txt") as fw_file:
        logger.info("Records in generated fixed width file:{}".format(fw_file.readlines()))
    fw_file.close()

    # Convert Fixed width file to CSV
    gfw.convert_to_csv()
    with open("fw_csv_file.csv") as fw_csv_file:
        logger.info("Records in generated CSV file:{}".format(fw_csv_file.readlines()))
    fw_csv_file.close()
