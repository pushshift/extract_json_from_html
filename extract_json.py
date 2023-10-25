#!/usr/bin/env python3

import sys
import ujson as json
import time
import requests
import logging
logging.basicConfig(level=logging.DEBUG)


def find_json_obj(data:str=None, test_size:int=3_000):

    start_time = time.time()
    start_char, end_char = "{", "}"
    start_chars, end_chars = [],[]
    anchor_text = "friendCount"
    try:
        anchor_start = data.index(anchor_text)
    except ValueError:
        logging.error(f"Anchor text is not present in data")
        sys.exit()
    else:
        logging.debug(f"Anchor text start position is located at {anchor_start:,}")

    # Sanity checks
    assert(test_size < anchor_start)
    assert(test_size < (len(data) - (anchor_start + len(anchor_text))))

    previous_index = None
    for eb in range(anchor_start, anchor_start + test_size):
        if data[eb] == end_char:
            logging.debug(f"Found end bracket at location {eb:,}")
            end_chars.append(eb)

            # Don't include ending characters that have the same character
            # directly after them. With JSON objects, if the end of the string
            # contains "}}", the actual end of the object will be the last one.
            if previous_index is not None and eb - previous_index == 1:
                del end_chars[-2]
            previous_index = eb

    logging.debug(f"Total ending characters found: {len(end_chars):,}")

    # Find beginning brackets
    for sb in range(anchor_start - test_size, anchor_start):

        if data[sb] == start_char:
            logging.debug(f"Found start bracket at location {sb:,}")
            start_chars.append(sb)

            if previous_index is not None and sb - previous_index == 1:
                del start_chars[-2]
            previous_index = sb

    logging.debug(f"Total start characters found: {len(start_chars):,}")
    logging.debug(f"Total time taken: {(time.time() - start_time)*1_000:.1f} milliseconds.")

    total_time = None
    is_done = False

    # Test for valid JSON objects
    for start in start_chars:
        if is_done:
            break
        for end in end_chars:
            obj = data[start:end+1]
            logging.debug(f"Testing positions: {start} to {end}")
            try:
                j = json.loads(obj)
            except json.JSONDecodeError:
                pass
            else:
                total_time = (time.time() - start_time) * 1_000
                logging.debug(f"Found valid JSON -- {start} to {end} | Total size: {end-start:,} characters")
                logging.debug(f"JSON Object:\n\n{obj}\n")
                logging.debug(f"Total script time: {total_time:.2f} milliseconds")
                is_done = True
                break

    return obj


if __name__ == "__main__":

    tiktok_user = "@khaby.lame"
    logging.debug(f"Fetching the most popular tiktok user: {tiktok_user}")
    r = requests.get(url=f"https://www.tiktok.com/{tiktok_user}")

    if r.ok:
        data = r.text
        json_string = find_json_obj(data=data, test_size=5_000)
        json_dict = json.loads(json_string)

    '''
    Do something with json_dict (or json_string if you want to put the data into Mongo DB or
    PostgreSQL. This script is designed to help the programmer locate the JSON object within
    a string of text or inside HTML. Many times it is extremely difficult to figure out the
    start and end borders for a large JSON object embedded in HTML.

    Current limitations of this script include making the assumption that there is only one
    JSON object to be fetched from a large string. This can be easily rectified and will be
    included in a future version of this script.
    '''

