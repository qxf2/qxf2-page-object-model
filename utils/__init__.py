
"Check if dict item exist for given key else return none"

def get_dict_item(from_this, get_this):
    """ get dic object item """
    if not from_this:
        return None
    item = from_this
    if isinstance(get_this, str):
        if from_this.has_key(get_this):
            item = from_this[get_this]
        else:
            item = None
    else:
        for key in get_this:
            if isinstance(item, dict) and item.has_key(key):
                item = item[key]
            else:
                return None
    return item
