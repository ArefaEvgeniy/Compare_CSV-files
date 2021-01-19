import pytest

import utils
import const


@pytest.fixture()
def init_csv():
    return [
        ['name', 'value_1', 'value_2', 'value_3'],
        ['green', '1', '2', '3'],
        ['blue', 1, 2, 3],
        ['pink', None, '-', ''],
        ['black', '-', None, ['5', '6', 7]]
    ]


@pytest.fixture()
def cache():
    cache = utils.CacheData()
    cache.append({'item_1': {'a': 1, 'b': 2}})
    cache.append({'item_2': 'value_2'})
    cache.append({'item_3': 3})
    cache.append('item_4')
    cache.append(['item_5', 5])
    cache.append(None)
    return cache


CSV_DATA_1 = [
    ['key_f', 'field_1', 'field_2', 'field_3'],
    ['key_1', 1, 2, 3],
    ['key_2', '1', '', None],
]
CSV_DATA_2 = [
    ['key', 'first', 'second', 'fourth'],
    ['key_1', 1, '2', None],
    ['key_2', 3, None, None],
    ['key_3', None, '', None],
]
DICT_DATA_1 = {
    'key_1': {'key_f': 'key_1', 'field_1': 1, 'field_2': 2, 'field_3': 3},
    'key_2': {'key_f': 'key_2', 'field_1': '1', 'field_2': '', 'field_3': None},
}
DICT_DATA_2 = {
    'key_1': {'key': 'key_1', 'first': 1, 'second': '2', 'fourth': None},
    'key_2': {'key': 'key_2', 'first': 3, 'third': 'third'},
    'key_3': {'key': 'key_3', 'second': '', 'fifth': 5},
}
FILE_DATA_1 = 'key_f,field_1,field_2,field_3\nkey_1,1,2,3\nkey_2,1,,\n'
FILE_DATA_2 = 'key,first,second,fourth\nkey_1,1,2,\nkey_2,3,,\nkey_3,,,\n'

values_for_save_data = [
    [CSV_DATA_1, FILE_DATA_1],
    [CSV_DATA_2, FILE_DATA_2]
]

values_for_load_data = [
    [FILE_DATA_1, CSV_DATA_1],
    [FILE_DATA_2, CSV_DATA_2]
]

values_for_create_small_dicts = [
    [
        {'a': 1, 'b': 2},
        {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7,
         'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12}
    ],
    [
        {},
        {'a': [1, 2, 3], 'b': {1: 'a', 2: 'b', 3: 'c'}}
    ],
    [
        {},
        {}
    ]
]

values_for_prepare_columns = [
    [
        {
            const.COLUMNS: 0,
            const.FIELDS: [['field_1', 'field_2'], ['field_1', 'field_3']],
            const.DIFFERENT_FIELDS: True
        },
        'key'
    ],
    [
        {
            const.COLUMNS: 1,
            const.FIELDS: [['field_1', 'key'], ['key', 'field_3']],
            const.DIFFERENT_FIELDS: False
        },
        'key'
    ],
    [
        {
            const.COLUMNS: 2,
            const.FIELDS: [['field_1', 'key'], ['field_1', 'field_3']],
            const.DIFFERENT_FIELDS: True
        },
        'key'
    ],
    [
        {
            const.COLUMNS: 3,
            const.FIELDS: [['field_1', 'field_2'], ['field_1', 'field_3']],
            const.DIFFERENT_FIELDS: False
        },
        'key'
    ],
    [
        {
            const.COLUMNS: 4,
            const.FIELDS: [['field_1', 'field_2'], ['field_1', 'field_3']],
            const.DIFFERENT_FIELDS: True
        },
        'key'
    ],
]

values_for_process = [
    [
        ['key', 'field_1', 'field_2', 'field_3'],
        {'key': 1, 'field_1': None, 'field_2': 'value'},
        {'key': 1, 'field_1': 3, 'field_2': 'value', 'field_3': 'AAA'},
        1,
        {
            'items': 0, 'different_fields': True, 'values_different': 0,
            'delimiter': 0, 'values_math': 0, 'absent': 0, 'columns': 0,
            'fields': [
                ['key', 'field_1', 'field_2'],
                ['key', 'field_1', 'field_2', 'field_3']
            ]
        },
        ['1', 'None   /   3', ' ', 'None   /   AAA']
    ],
    [
        ['key', 'field_1', 'field_2'],
        {'key': 1, 'field_1': None, 'field_2': 'value'},
        {'key': 'second', 'field_1': 3, 'field_3': 'AAA'},
        'second',
        {
            'items': 1, 'different_fields': False, 'values_different': 0,
            'delimiter': 1, 'values_math': 1, 'absent': 0, 'columns': 1,
            'fields': [
                ['key', 'field_1', 'field_2'], ['key', 'field_1', 'field_3']
            ]
        },
        ['second', 'None / 3', 'value / None']
    ],
    [
        ['key', 'field_1', 'field_2', 'field_3'],
        {'key': 1, 'field_1': None, 'field_2': 'value'},
        {'key': 1, 'field_1': 3, 'field_2': 'value', 'field_3': 'AAA'},
        1,
        {
            'items': 2, 'different_fields': False, 'values_different': 1,
            'delimiter': 2, 'values_math': 0, 'absent': 1, 'columns': 0,
            'fields': [
                ['key', 'field_1', 'field_2'],
                ['key', 'field_1', 'field_2', 'field_3']
            ]
        },
        ['1', '3', ' ', 'AAA']
    ],
    [
        ['key', 'field_1', 'field_2', 'field_3'],
        {'key': 1, 'field_1': None, 'field_2': 'value'},
        {'key': 1, 'field_1': 3, 'field_2': 'value', 'field_3': 'AAA'},
        1,
        {
            'items': 2, 'different_fields': True, 'values_different': 2,
            'delimiter': 2, 'values_math': 2, 'absent': 0, 'columns': 3,
            'fields': [
                ['key', 'field_1', 'field_2'],
                ['key', 'field_1', 'field_2', 'field_3']
            ]
        },
        ['1', 'None   |   3', 'math', 'None   |   AAA']
    ]
]

values_for_generate_report = [
    [
        [
            {
                'key_1': {'key_f': 'key_1', 'field_1': 'value_1_1',
                          'field_2': 'value_1_2', 'field_3': 'value_1_3'},
                'key_2': {'key_f': 'key_2', 'field_1': 'value_2_1',
                          'field_2': 'value_2_2'},
            },
            {
                'key_1': {'key_f': 'key_1', 'field_1': 'value_1_1',
                          'field_2': 'value_2'},
                'key_3': {'key_f': 'key_3', 'field_1': 'value_3_1',
                          'field_3': 'value_3_2'},
            },
        ],
        {
            'items': 2, 'different_fields': True, 'values_different': 2,
            'delimiter': 2, 'values_math': 2, 'absent': 0, 'columns': 3,
            'fields': [
                ['key_f', 'field_1', 'field_2', 'field_3'],
                ['key_f', 'field_1', 'field_2']
            ]
        },
        'key_f',
        [
            ['key_f', 'different_fields', 'field_1', 'field_2', 'field_3'],
            ['key_2', '', 'value_2_1', 'value_2_2', None]
        ]
    ],
    [
        [
            {
                'key_1': {'key_f': 'key_1', 'field_1': 'value_1_1',
                          'field_2': 'value_1_2', 'field_3': 'value_1_3'},
                'key_2': {'key_f': 'key_2', 'field_1': 'value_2_1',
                          'field_2': 'value_2_2'},
                'key_3': {'key_f': 'key_3', 'field_1': 'value_3_1',
                          'field_3': 'value_3_2'},
            },
            {
                'key_1': {'key_f': 'key_1', 'field_1': 'value_1_1',
                          'field_2': 'value_2'},
                'key_3': {'key_f': 'key_3', 'field_1': 'value_3_1',
                          'field_3': 'value_3_2'},
            },
        ],
        {
            'items': 1, 'different_fields': False, 'values_different': 0,
            'delimiter': 3, 'values_math': 0, 'absent': 0, 'columns': 2,
            'fields': [
                ['key_f', 'field_1', 'field_2', 'field_3'],
                ['key_f', 'field_1', 'field_2']
            ]
        },
        'key_f',
        [
            ['key_f', 'field_3'],
            ['key_3', ' '],
            ['key_1', 'value_1_3 | None'],
            ['key_2', None]
        ]
    ],
]

values_for_dict_to_table = [
    [
        DICT_DATA_1,
        ['key_f', 'field_1', 'field_2', 'field_3'],
        CSV_DATA_1
    ],
    [
        DICT_DATA_2,
        ['key', 'first', 'second', 'fourth'],
        CSV_DATA_2
    ]
]
