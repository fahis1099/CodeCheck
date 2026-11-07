import os


def add_item(item, items=[]):
    try:
        items.append(item)
    except:
        print("Something went wrong")

    return items