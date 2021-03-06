#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
@Author: Mehdi Bahri
@Contact: m.bahri@imperial.ac.uk
@File: bulk_rename_arxiv.py
@Time: 2021/04/12 08:08 PM
"""

import os
import re
import sys
import glob
import pathlib

from collections import defaultdict

import arxiv


def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.

    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'

    https://github.com/django/django/blob/master/django/utils/text.py
    Copyright (c) Django Software Foundation and individual contributors.
    All rights reserved.
    """
    s = str(s).strip().replace('  ', ' ')
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


p = re.compile("^[0-9]{4}\.[0-9]{5}")
pdfs = pathlib.Path('.').rglob('*.pdf')

ids = []
ids_name_map = defaultdict(list)
has_duplicates = defaultdict(bool)
duplicate_data = defaultdict(list)

for n in pdfs:
    id_ = p.match(n.name)
    if id_:
        the_id = id_[0]
        if len(ids_name_map[the_id]) > 0:
            has_duplicates[the_id] = True
            print(f'Detected duplicates for id {the_id}')
        else:
            ids.append(the_id)

        ids_name_map[the_id].append(n)

print(sorted(ids))

print("{} ids to query".format(len(ids)))

entries = arxiv.query(id_list=ids)

print("Query done")

print("Renaming...")
for base, entry in zip(ids, entries):
    new_name = get_valid_filename(entry['title'])
    paths = ids_name_map[base]

    # OK because the list should only contain each id once
    if has_duplicates[base]:
        duplicate_data[base] = []

    for path in paths:
        target = os.path.join(path.parent, f'{base}_{new_name}.pdf')
        path.rename(target)
        if has_duplicates[base]:
            duplicate_data[base].append(target)
print('Done')

print('\n********\n')

print('The following duplicate ids were found:')
if len(duplicate_data.keys()) == 0:
    print('None.')
else:
    for dup_id, paths in duplicate_data.items():
        print(f'{dup_id}:')
        for path in paths:
            print(path)