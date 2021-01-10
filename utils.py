#!/usr/bin/env python3
"""
Class CacheData and functions from file utils.py used in main file compare.py
"""


import csv

import const


class CacheData():
    """
    The class used to cache changes of settings
    The cache queue works according to the LIFA principle - the last change
    will leave the queue first, and the first change will go last.
    """

    def __init__(self, data=None, max_count=20):
        self.data = []
        self.count = 0
        self.max_count = max_count
        if data:
            self.append(data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"CacheData(len of 'data': {len(self.data)}, " \
               f"'count': {self.count}, 'max_count': {self.max_count})"

    def __str__(self):
        return repr(self)

    def append(self, item):
        """
        Append the change in settings to the end of the queue.
        If the counter for the last change is equal to the maximum length of
        the queue, then the first change is removed from the queue, and the
        current change is added to the end of the queue.
        If the counter for the last change is less than the maximum length of
        the queue or the queue is empty, then the change is written to the
        end of the queue, and the value of the counter is increased by one.
        """
        if self.count >= self.max_count:
            self.data = self.data[1:]
        elif self.count < len(self.data):
            self.data = self.data[0:self.count]
            self.count += 1
        else:
            self.count += 1
        self.data.append(item)

    def is_undo(self):
        """
        Checking the possibility to undo the change.
        Return True if there are changes in queue
        """
        return bool(self.count > 1)

    def is_redo(self):
        """
        Checking the possibility to redo of the change.
        Return True if the counter does not indicate on the last change
        """
        return bool(self.count < len(self.data))

    def undo(self):
        """
        Undo the last change if it is possible.
        Return the last change
        """
        result = None
        if self.is_undo():
            self.count -= 1
            result = self.data[self.count - 1]
        return result

    def redo(self):
        """
        Redo the last undo change if it is possible.
        Return the last undo change
        """
        result = None
        if self.is_redo():
            result = self.data[self.count]
            self.count += 1
        return result

    def clear(self):
        """
        Clear the change
        """
        self.data = []
        self.count = 0


def save_data(path, my_data):
    """
    Save data in csv-file on the path.
    Return error or None
    """
    error = None

    try:
        my_file = open(path, 'w')
        with my_file:
            writer = csv.writer(my_file)
            writer.writerows(my_data)

    except Exception as err:  # pylint: disable=W0703
        error = f'{const.SAVE_DATA}{const.FAILED_ERROR}{err}'

    return error


def load_data(path):
    """
    Load data from csv-file on the path.
    Return result of this action and error or None
    """
    result = None
    error = None

    if path:
        with open(path, 'r') as open_file:
            try:
                if path.endswith(const.CSV):
                    result = []
                    data = csv.reader(open_file)
                    for item in data:
                        result.append(item)
                else:
                    error = const.ERROR_READ_FILE
            except Exception as err:  # pylint: disable=W0703
                error = f'{const.LOAD_DATA}{const.FAILED_ERROR}{err}'

    return result, error


def convert_csv_to_dict(csv_data, name_key_field, list_field):
    """
    Convert data from csv-file to the dictionary.
    Return result of this action and error or None
    """
    result = {}
    error = None
    key_field = None
    fields = []

    try:
        for index, item in enumerate(csv_data[0]):
            if item == name_key_field:
                key_field = index
            if item in list_field:
                fields.append((index, item))

        for row in csv_data[1:]:
            ret = {}
            for item in fields:
                ret.update({item[1]: row[item[0]]})
            result.update({row[key_field]: ret})

    except Exception as err:  # pylint: disable=W0703
        error = f'{const.CSV_TO_DICT}{const.FAILED_ERROR}{err}'

    return result, error


def create_small_dicts(dicts):
    """
    Create small dictionaries from full dictionaries to show.
    Return small dictionaries
    """
    result = [{}, {}]

    for index, dict_item in enumerate(dicts):
        if dict_item is None or len(dict_item) == 0:
            continue

        keys = dict_item.keys()
        count = 0

        for key in keys:
            if count > const.LEN_SMALL_DICTS:
                break

            result[index].update({key: dict_item[key]})
            count += 1

    return result


def prepare_columns(settings, key_field):
    """
    Create names of columns for result
    Return these names
    """
    result = []

    if settings.get(const.FIELDS) and isinstance(settings[const.FIELDS], list):
        mode = settings[const.COLUMNS]

        if mode == 0:
            for item in settings[const.FIELDS][0]:
                if item in settings[const.FIELDS][1]:
                    result.append(item)

        elif mode == 1:
            result = settings[const.FIELDS][0][0:]
            for item in settings[const.FIELDS][1]:
                if item not in result:
                    result.append(item)

        elif mode == 2:
            for item in settings[const.FIELDS][0]:
                if item not in settings[const.FIELDS][1]:
                    result.append(item)
            for item in settings[const.FIELDS][1]:
                if item not in settings[const.FIELDS][0]:
                    result.append(item)

        elif mode == 3:
            result = settings[const.FIELDS][0][0:]

        else:
            result = settings[const.FIELDS][1][0:]

        if settings[const.DIFFERENT_FIELDS]:
            result.insert(1, const.DIFFERENT_FIELDS)

        if key_field not in result:
            result.insert(0, key_field)
        elif result.index(key_field) != 0:
            result.pop(result.index(key_field))
            result.insert(0, key_field)

    return result


def process(list_field, dict_1, dict_2, key, settings):
    """
    Create row of result dictionary depending on settings
    Return result row
    """
    different_fields = None
    res = []
    delimiter = const.VARIANTS_DELIMIT[0]

    if settings.get(const.DELIMITER):
        if settings.get(const.DELIMITER) == len(const.VARIANTS_DELIMIT) - 1:
            delimiter = '\n'
        elif settings.get(const.DELIMITER):
            delimiter = const.VARIANTS_DELIMIT[settings[const.DELIMITER]]

    for item in list_field:
        if item == list_field[0]:
            res.append(str(key))

        elif item == const.DIFFERENT_FIELDS:
            res.append(const.NOTHING)
            different_fields = []

        elif dict_1 and dict_2 is None:
            res.append(dict_1.get(item))

        elif dict_2 and dict_1 is None:
            res.append(dict_2.get(item))

        elif (dict_1.get(item) is None
              or dict_2.get(item) is None):
            if settings.get(const.ABSENT) == 0:
                res.append(f'{dict_1.get(item)}{delimiter}{dict_2.get(item)}')
            if settings.get(const.ABSENT) == 1:
                item_1 = dict_1.get(item) if dict_1.get(item) else ''
                item_2 = dict_2.get(item) if dict_2.get(item) else ''
                res.append(f'{item_1}{item_2}')
            elif settings.get(const.ABSENT) == 2:
                res.append(const.DASH)
            elif settings.get(const.ABSENT) == 3:
                res.append(const.ABSENT)
            elif settings.get(const.ABSENT) == 4:
                res = []
                break
            elif settings.get(const.ABSENT) == 5:
                res.append(const.NOTHING)

        elif dict_1.get(item) == dict_2.get(item):
            if settings.get(const.VALUES_MATH) == 0:
                res.append(const.NOTHING)
            elif settings.get(const.VALUES_MATH) == 2:
                res.append(const.MATH)
            else:
                res.append(dict_1[item])

        else:
            if settings.get(const.VALUES_DIFFERENT) == 0:
                res.append(f'{dict_1.get(item)}{delimiter}{dict_2.get(item)}')
            elif settings.get(const.VALUES_DIFFERENT) == 1:
                res.append(dict_1.get(item))
            elif settings.get(const.VALUES_DIFFERENT) == 2:
                res.append(dict_2.get(item))
            elif settings.get(const.VALUES_DIFFERENT) == 3:
                res.append(const.NOTHING)
            elif settings.get(const.VALUES_DIFFERENT) == 4:
                res.append(const.DIFFERENT)
            elif settings.get(const.VALUES_DIFFERENT) == 5:
                res = []
                break

            if different_fields is not None:
                different_fields.append(item)

    if different_fields is not None and len(res) > 0:
        res[1] = ', '.join(different_fields)

    return res


def generate_report(dicts, settings, key_field):
    """
    Create result dictionary of compare two dictionaries
    Return result dictionary
    """
    result = []
    keys = []

    if not (isinstance(dicts, list) and len(dicts) == 2 and
            isinstance(settings, dict) and
            len(settings.get(const.FIELDS)) > 0 and
            isinstance(dicts[0], dict) and isinstance(dicts[1], dict)):
        return None

    list_field = prepare_columns(settings, key_field)

    if settings.get(const.ITEMS) == 0:
        keys = [x for x in dicts[0].keys() if dicts[1].get(x)]

    elif settings.get(const.ITEMS) == 1:
        keys_1 = [x for x in dicts[0].keys()]
        keys_2 = [x for x in dicts[1].keys()]
        keys = list(set(keys_1 + keys_2))

    elif settings.get(const.ITEMS) == 2:
        keys = [x for x in dicts[0].keys() if dicts[1].get(x) is None]

    elif settings.get(const.ITEMS) == 3:
        keys = [x for x in dicts[1].keys() if dicts[0].get(x) is None]

    result.append(list_field)
    for key in keys:
        row = process(list_field, dicts[0].get(key), dicts[1].get(key),
                      key, settings)

        if len(row) > 0:
            result.append(row)

    return result


def dict_to_table(in_dict, list_field):
    """
    Create table from dictionary
    Return table
    """
    result = [list_field]

    for key in in_dict.keys():
        row = [key]
        for item in list_field[1:]:
            row.append(in_dict[key].get(item))
        result.append(row)

    return result
