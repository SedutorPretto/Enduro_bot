def dict_from_message(text):
    data = {}
    for element in text.split('\n'):
        key, value = element.split('-')
        data[key.strip()] = value.strip()
    return data
