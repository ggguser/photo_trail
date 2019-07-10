from collections import Counter


def search_area_db(areas, search_query: str):
    search_words = prepare_search(search_query)
    area_id = get_area_id(areas, search_words)

    return area_id


def prepare_search(search_query: str):
    """
    Подготовка поискового запроса: разбивка на слова, уменьшение регистра.
    >>> prepare_search('автономное сообщество Андалусия')
    ['автономное', 'сообщество', 'андалусия']
    """
    return [x for x in search_query.lower().split()]


def get_area_id(areas: list, search_words: list):
    result = []
    for word in search_words:
        for area in areas:
            if word in area.name.lower().split():
                result.append(area.id)
    return get_most_frequent(result)


def get_most_frequent(items: list):
    """
    Из списка достаёт наиболее часто встречающийся элемент
    >>> get_most_frequent([1, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0])
    0
    """
    #  Composing a dictionary with 'elements': frequency pairs
    frequency = Counter(items)
    #  From dictionary composing a list of tuples sorted by frequency
    sorted_frequency = frequency.most_common()
    #  List of tuples getting the first element of the first tuple
    return sorted_frequency[0][0]
