from arcade import SpriteList


def extend_sprite_list(lst: SpriteList, iterable):
    """
    Extend sprite list with elements on iterable.
    """
    append = lst.append
    for x in iterable:
        append(x)


def fix_all():
    """
    Monkey patch external libs.
    """

    SpriteList.extend = extend_sprite_list
