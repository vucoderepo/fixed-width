""""
    Name: test_generate.py
    Author: Venu Uppala
    purpose: Used to define reusable fixtures
"""
import generator.generate
from pytest import raises


class FixedWidthFileTests:

    def add_record(self, record):
        fwf = generator.generate.FixedWidthFile()
        fwf.add_record(record)
        return fwf

    def test_add_record_valid(self, valid_record):
        fwf = self.add_record(valid_record)
        assert (isinstance(fwf, generator.generate.FixedWidthFile))
        assert len(fwf.records) > 0
        assert (isinstance(next(iter(fwf.records)), generator.generate.FixedWidthRecord))

    def bad_fixed_width_record(self, bad_record):
        with raises(generator.generate.FixedWidthRecordException):
            self.add_record(bad_record)

    def test_add_record_invalid(self, invalid_record):
        self.bad_fixed_width_record(invalid_record)

    def test_add_record_empty(self, empty_record):
        self.bad_fixed_width_record(empty_record)

    def test_get_field_indexes(self):
        fwf = generator.generate.FixedWidthFile()
        field_indexes = fwf.get_field_indexes()
        assert len(field_indexes) == 10

    def test_create_valid(self, valid_record):
        fwf = self.add_record(valid_record)
        fwf.create()
        with open("fw_file.txt") as fw_file:
            lines = fw_file.readlines()
        fw_file.close()
        assert len(lines) == 2

    def test_create_invalid(self, invalid_record):
        with raises(generator.generate.FixedWidthRecordException):
            fwf = self.add_record(invalid_record)
            fwf.create()

    def test_convert_to_csv_valid(self, valid_record):
        fwf = self.add_record(valid_record)
        fwf.create()
        fwf.convert_to_csv()
        assert (isinstance(fwf, generator.generate.FixedWidthFile))
        assert len(fwf.records) > 0
        assert (isinstance(next(iter(fwf.records)), generator.generate.FixedWidthRecord))
        with open("fw_csv_file.csv") as csv_file:
            lines = csv_file.readlines()
        assert len(lines) == 2

    def test_convert_to_csv_invalid(self, invalid_record):
        with raises(generator.generate.FixedWidthRecordException):
            fwf = self.add_record(invalid_record)
            fwf.create()
            fwf.convert_to_csv()
