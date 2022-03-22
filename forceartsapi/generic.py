"""Generic helper functions"""


def get_or_none(classmodel, **kwargs):
    """Returns object or None"""
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
