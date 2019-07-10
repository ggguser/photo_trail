from collections import Counter


def get_area_id(areas: list, search_query: str):
    result = []
    search_words = search_query.lower().split()
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
    try:
        #  Composing a dictionary with 'elements': frequency pairs
        frequency = Counter(items)
        #  From dictionary composing a list of tuples sorted by frequency
        sorted_frequency = frequency.most_common()
        #  List of tuples getting the first element of the first tuple
        return sorted_frequency[0][0]
    except IndexError:
        return None


