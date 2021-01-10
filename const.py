#!/usr/bin/env python3
"""
Constants from file const.py used in main files compare.py and utils.py
"""


BUTTONS = ['First File', 'Second File', 'Generate report']
CLEAR_BUTTONS = ['Clear First File', 'Clear Second File']
UNDO_REDO = ['undo', 'redo']
VARIANTS_ITEMS = ['First file and Second file', 'First file or Second file',
                  'only First file', 'only Second file']
VARIANTS_VAL = ['Show both values with delimiter', 'Show first value',
                'Show second value', 'Show nothing',
                'Show inscription "different"', 'Do not show this Item']
VARIANTS_VAL_MATH = ['Show nothing', 'Show value', 'Show inscription "math"']
VARIANTS_DELIMIT = ['   /   ', ' / ', '   |   ', ' | ', ' ', r'new line (\n)']
VARIANTS_KEY_ABSENT = ['Show one of value with "None"', 'Show one of value',
                       'Show sign "-"', 'Show inscription "absent"',
                       'Do not show this Item', 'Show nothing']
VARIANTS_COLUMNS = ['First file and Second file', 'First file or Second file',
                    'if column is in one if file and it is absent in other',
                    'only First file', 'only Second file']

IMAGE_EXIT = 'images/exit.png'
IMAGE_OPEN = 'images/open-file.png'
IMAGE_CLEAR = 'images/clear.png'
IMAGE_GENERATE = 'images/generate.png'
IMAGE_UNDO = 'images/undo.png'
IMAGE_REDO = 'images/redo.png'

ITEMS = 'items'
DIFFERENT_FIELDS = 'different_fields'
VALUES_DIFFERENT = 'values_different'
VALUES_MATH = 'values_math'
DELIMITER = 'delimiter'
ABSENT = 'absent'
COLUMNS = 'columns'
FIELDS = 'fields'
MATH = 'math'
DIFFERENT = 'different'
DASH = '-'
NOTHING = ' '

COMPLETED = 'Completed'
LOAD_DATA = 'Load data'
SAVE_DATA = 'Save data'
CSV_TO_DICT = 'Convert Csv to Dict'
FAILED_ERROR = ' failed, error: '
ERROR_PATH = 'Path to file did not set or set not correctly'
ERROR_READ_FILE = 'Format of read file does not known'

CSV = 'csv'

LEN_SMALL_DICTS = 10
