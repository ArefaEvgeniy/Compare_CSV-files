import pytest

import conftest
import utils
import const


def test_len(cache):
    assert len(cache) == 6


def test_str(cache):
    assert str(cache) == "CacheData(len of 'data': 6, 'count': 6, " \
                         "'max_count': 20)"


def test_append(cache):
    assert len(cache) == 6

    cache.append('New item')
    assert len(cache) == 7
    assert cache.data[-1] == 'New item'


def test_is_undo(cache):
    assert cache.is_undo() is True
    assert utils.CacheData().is_undo() is False


def test_is_redo(cache):
    assert cache.is_redo() is False
    cache.count = 5
    assert cache.is_redo() is True


def test_undo(cache):
    check_item = cache.data[-2]
    assert cache.data[-2] == check_item
    assert cache.count == 6
    assert len(cache) == 6

    item = cache.undo()
    assert item == check_item
    assert cache.data[-2] == check_item
    assert len(cache) == 6
    assert cache.count == 5

    cache.count = 1
    item = cache.undo()
    assert item is None
    assert len(cache) == 6
    assert cache.count == 1

    assert utils.CacheData().undo() is None


def test_redo(cache):
    last_item = cache.data[-1]
    before_last_item = cache.data[-2]
    assert cache.count == 6
    assert len(cache) == 6

    item = cache.redo()
    assert item is None

    cache.count = 5
    item = cache.redo()
    assert item == last_item

    cache.count = 4
    item = cache.redo()
    assert item == before_last_item
    item = cache.redo()
    assert item == last_item

    assert utils.CacheData().redo() is None


def test_clear(cache):
    assert len(cache) == 6

    cache.clear()
    assert len(cache) == 0
    assert cache.data == []
    assert cache.count == 0

    cache.clear()
    assert len(cache) == 0
    assert cache.data == []
    assert cache.count == 0


def test_max_count(cache):
    assert len(cache) == 6
    cache.max_count = 6
    item_0 = cache.data[0]
    assert cache.data[0] == item_0

    cache.append('New item')
    assert len(cache) == 6
    assert str(cache) == "CacheData(len of 'data': 6, 'count': 6, " \
                         "'max_count': 6)"
    assert cache.data[-1] == 'New item'
    assert cache.data[0] != item_0


@pytest.mark.parametrize('value', conftest.values_for_save_data)
def test_save_data(tmpdir, value):
    file_name = tmpdir.join('test.csv')
    utils.save_data(file_name, value[0])
    assert file_name.read() == value[1]


@pytest.mark.parametrize('value', conftest.values_for_load_data)
def test_load_data(tmpdir, value):
    file_name = tmpdir.join('test.csv')
    file_name.write(value[0])
    res = utils.load_data(file_name.strpath)

    answer = []
    for index_1, items_list in enumerate(value[1]):
        if len(answer) <= index_1:
            answer.append([])
        for item in items_list:
            if item is None:
                answer[index_1].append('')
            else:
                answer[index_1].append(str(item))

    assert res == (answer, None)


def test_convert_csv_to_dict(init_csv):
    res = utils.convert_csv_to_dict(init_csv, 'name', ['name', 'value_1',
                                                       'value_3'])
    assert len(res) == 2
    assert len(res[0]) == 4
    assert res[0].get('green') == {'name': 'green', 'value_1': '1',
                                   'value_3': '3'}
    assert res[0].get('blue') == {'name': 'blue', 'value_1': 1, 'value_3': 3}
    assert res[0].get('pink') == {'name': 'pink', 'value_1': None,
                                  'value_3': ''}
    assert res[0].get('black') == {'name': 'black', 'value_1': '-',
                                   'value_3': ['5', '6', 7]}
    assert res[1] is None


def test_convert_csv_to_dict_2(init_csv):
    init_csv[1][0] = 'blue'
    res = utils.convert_csv_to_dict(init_csv, 'name', ['name', 'value_1',
                                                       'value_2', 'value_3'])
    assert len(res) == 2
    assert len(res[0]) == 3
    assert res[0].get('blue') == {'name': 'blue', 'value_1': 1, 'value_2': 2,
                                  'value_3': 3}
    assert res[0].get('pink') == {'name': 'pink', 'value_1': None,
                                  'value_2': '-', 'value_3': ''}
    assert res[0].get('black') == {'name': 'black', 'value_1': '-',
                                   'value_2': None, 'value_3': ['5', '6', 7]}

    assert res[1] is None


@pytest.mark.parametrize('dicts', conftest.values_for_create_small_dicts)
def test_create_small_dicts(dicts):
    res = utils.create_small_dicts(dicts)
    for index in range(2):
        assert len(res[index]) == len(dicts[index]) \
            if len(dicts[index]) < const.LEN_SMALL_DICTS \
            else const.LEN_SMALL_DICTS


@pytest.mark.parametrize('value', conftest.values_for_prepare_columns)
def test_prepare_columns(value):
    res = utils.prepare_columns(value[0], value[1])

    assert res[0] == 'key'
    assert res[1] == const.DIFFERENT_FIELDS \
        if value[0].get(const.DIFFERENT_FIELDS) \
        else res[1] != const.DIFFERENT_FIELDS

    if value[0].get(const.COLUMNS) == 0:
        for item in value[0].get(const.FIELDS)[0]:
            assert item in res \
                if item in value[0].get(const.FIELDS)[1] \
                else item not in res

    elif value[0].get(const.COLUMNS) == 1:
        union = value[0].get(const.FIELDS)[0] + value[0].get(const.FIELDS)[1]
        for item in set(union):
            assert item in res

    elif value[0].get(const.COLUMNS) == 2:
        for number in range(2):
            for item in value[0].get(const.FIELDS)[number]:
                next_number = 1 if number == 0 else 0
                assert item in res \
                    if item not in value[0].get(const.FIELDS)[next_number] \
                    else item not in res

    elif value[0].get(const.COLUMNS) == 3:
        for item in value[0].get(const.FIELDS)[0]:
            assert item in res

    else:
        for item in value[0].get(const.FIELDS)[1]:
            assert item in res


@pytest.mark.parametrize('value', conftest.values_for_process)
def test_process(value):
    res = utils.process(value[0], value[1], value[2], value[3], value[4])
    assert res == value[5]


@pytest.mark.parametrize('value', conftest.values_for_generate_report)
def test_generate_report(value):
    res = utils.generate_report(value[0], value[1], value[2])
    assert res[0] == value[3][0]
    for item in res[1:]:
        assert item in value[3]


@pytest.mark.parametrize('value', conftest.values_for_dict_to_table)
def test_dict_to_table(value):
    res = utils.dict_to_table(value[0], value[1])
    assert res[0] == value[2][0]
    for item in res[1:]:
        assert item in value[2]
