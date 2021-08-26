import pandas as pd
from collections import namedtuple


class Printer(object):
    def __init__(self, field_names):
        self.field_names_ = field_names
        self.records_ = []
        self.handlers_ = dict()
        self.str_lens_ = dict()
        self.title_printed_ = False
        self.Record = None

    def finish(self):
        self.Record = namedtuple("Record", self.field_names_)
        err = f"{len(self.field_names_)} vs. {len(self.handlers_)}"
        assert len(self.field_names_) == len(self.handlers_), err
        err = f"{len(self.field_names_)} vs. {len(self.str_lens_)}"
        assert len(self.field_names_) == len(self.str_lens_), err
        for fname in self.field_names_:
            assert fname in self.handlers_, f"{fname} handler not register"
            assert fname in self.str_lens_, f"{fname} str_len not register"

    def record(self, *args, **kwargs):
        assert self.Record is not None
        r = self.Record(*args, **kwargs)
        self.records_.append(r)

    def register_handler(self, field, handler):
        assert callable(handler)
        self.handlers_[field] = handler

    def register_str_len(self, field, str_len):
        assert isinstance(str_len, int)
        self.str_lens_[field] = str_len

    def print_field_names(self):
        fields = ""
        sep = ""

        for fname in self.field_names_:
            str_len = self.str_lens_[fname]
            fields += "| {} ".format(fname.ljust(str_len))
            sep += f"| {'-' * str_len} "

        fields += "|"
        sep += "|"
        print(fields)
        print(sep)
        self.title_printed_ = True

    def reset_title_printed(self):
        self.title_printed_ = False

    def print(self):
        df = pd.DataFrame(self.records_)
        record = ""

        for fname in self.field_names_:
            assert fname in self.handlers_
            handler = self.handlers_[fname]
            field_value = handler(df[fname])

            str_len = self.str_lens_[fname]
            record += "| {} ".format(str(field_value).ljust(str_len))

        record += "|"

        if not self.title_printed_:
            self.print_field_names()

        print(record)
        self.records_ = []
