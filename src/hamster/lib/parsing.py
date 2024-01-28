import logging
logger = logging.getLogger(__name__)   # noqa: E402

import re

from hamster.lib import datetime as dt


# separator between times and activity
activity_separator = r"\s+"

# match #tag followed by any space or # that will be ignored
# tag must not contain '#' or ','
tag_re = re.compile(r"""
    \#          # hash character
    (?P<tag>
        [^#,]+  # (anything but hash or comma)
    )
""", flags=re.VERBOSE)

tags_in_description = re.compile(r"""
    \#
    (?P<tag>
        [a-zA-Z] # Starts with an alphabetic character (digits excluded)
        [^\s]+   # followed by anything except spaces
    )
""", flags=re.VERBOSE)

tags_separator = re.compile(r"""
    ,{1,2}      # 1 or 2 commas
    \s*         # maybe spaces
    (?=\#)      # hash character (start of first tag, doesn't consume it)
""", flags=re.VERBOSE)


def get_tags_from_description(description):
    return list(re.findall(tags_in_description, description))

def consume_until(it, separators):
    """Consume iterator until one of the separators is found.

    Characters prefixed by backslash are replaced by the character
    (without backslash) and loose their potential meaning as
    separators.

    Returns:
    - Consumed string without escaping backslashes,
    - the separator that stopped consumption or None if end of
      iterator was reached before separator was found.
    """

    ret = []
    sep = None
    while True:
        try:
            c = next(it)
        except StopIteration:
            break

        if c in separators:
            sep = c
            break

        if c == '\\':
            try:
                c = next(it)
            except StopIteration:
                ret.append(c)  # TODO: What to do when \ is last symbol? IMO this should be a parse error. Currently just append it.
                break

        ret.append(c)

    return "".join(ret), sep


def parse_fact(text, range_pos="head", default_day=None, ref="now"):
    """Extract fact fields from the string.

    Returns found fields as a dict.

    Tentative syntax (not accurate):
    start [- end_time] activity[@category][, description][,]{ #tag}
    According to the legacy tests, # were allowed in the description
    """

    res = {}

    text = text.strip()
    if not text:
        return res

    # datetimes
    # force at least a space to avoid matching 10.00@cat
    (start, end), remaining_text = dt.Range.parse(text, position=range_pos,
                                                  separator=activity_separator,
                                                  default_day=default_day)
    res["start_time"] = start
    res["end_time"] = end

    it = iter(remaining_text)
    res["activity"], sep = consume_until(it, ',@')
    if sep == "@":
        res["category"], sep = consume_until(it, ',')

    if sep == None:
        res["description"] = ''
        res["tags"] = []
        # print(res)  # TODO: remove
        return res

    split = re.split(tags_separator, sep + ''.join(it), 1)
    remaining_text = split[0]
    tags_part = split[1] if len(split) > 1 else None
    if tags_part:
        tags = list(map(lambda x: x.strip(), re.findall(tag_re, tags_part)))
    else:
        tags = []

    # description
    description = remaining_text.lstrip(',').strip()  # TODO: Stripping multiple commas is weird but resembles the previous behavior
    # Extract tags from description, put them before other tags
    tags = get_tags_from_description(description) + tags

    res["description"] = description
    res["tags"] = tags


    # print(res)  # TODO: remove
    return res
