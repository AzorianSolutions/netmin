
def action_label(value: int):
    return 'Update' if value else 'Create'


def no_value(value):
    return '' if value is None else value


def none_value(value):
    return 'None' if value is None or not len(str(value).strip()) else value


def selected(value, match):
    return 'selected' if value == match else ''


def checked(value, match):
    return 'checked' if value == match else ''
