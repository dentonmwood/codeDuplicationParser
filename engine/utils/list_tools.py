def flatten(list_of_lists):
    """
    Flattens a list of list into a single flat list.

    Arguments:
        list_of_lists {list[list[T]]} -- List of lists to flatten.

    Returns:
        list[T] -- Flat list generated by flattening the source list of lists.
    """
    flat = []

    for l in list_of_lists:
        flat.extend(l)

    return flat