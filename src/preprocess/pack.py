#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: compress.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 26, 2015
 #  Time: 13:48:16
 #  Description: extract jpeg files from tar 
 #               and pack them into a big binary file
 #               create inverted index at the same time
###############################################################################

import os
import tarfile

TAR_DIR = "TAR/"
WORDS_DICTIONARY = "words"
INVERTED_INDEX = "index"
COMPRESS_DIR = "COMPRESS/"
BLOCK_SIZE = int(1024 * 1024 * 1024 * 10) # 10 GiB
# tolerate 1 GiB empty space at the end of each block
MIN_BLOCK_SIZE = int(BLOCK_SIZE * 0.9) # 9 GiB

# check files and dirs
if not os.path.isfile(INVERTED_INDEX):
    print(INVERTED_INDEX, "does not exist. ")
    exit(1)
if not os.path.isfile(WORDS_DICTIONARY):
    print(WORDS_DICTIONARY, "does not exist. ")
    exit(1)
if not os.path.isdir(TAR_DIR):
    print(TAR_DIR, "does not exist or isn't a directory. ")
    exit(1)
if os.path.exists(COMPRESS_DIR) and not os.path.isdir(COMPRESS_DIR):
    print(COMPRESS_DIR, "exists and is not directory. ")
    exit(1)
if not os.path.exists(COMPRESS_DIR):
    os.mkdir(COMPRESS_DIR)


# load words dictionary
# words dictionary: tar_filename -> keywords splited with comma
words_dictionary = dict()
words_dict_file = open(WORDS_DICTIONARY)
for l in words_dict_file:
    index = l[: l.find('\t')]
    keywords = ",".join([ x.strip() for x in l[l.find('\t') + 1: -1].split(", ") ])
    words_dictionary[index] = keywords
words_dict_file.close()


# find the next compress block
compress_block_counter = 0
block_filename = format(compress_block_counter, "08x")
existing_compress_blocks = sorted(os.listdir(COMPRESS_DIR))
if len(existing_compress_blocks):
    last_block_filename = existing_compress_blocks[-1]
    last_block_size = os.path.getsize(COMPRESS_DIR + "/" + last_block_filename)
    compress_block_counter = int(last_block_filename, 16) 
    if last_block_size > MIN_BLOCK_SIZE:
        compress_block_counter += 1
    # we use 8 digit hex number as filename, in the range of uint32
    block_filename = format(compress_block_counter, "08x")


block_handler = open(COMPRESS_DIR + "/" + block_filename, "ab")
print("Append at", COMPRESS_DIR + block_filename, hex(block_handler.tell()))


# append content to block handler
# return (block index, offset, size)
def append_to_block(content):
    global block_handler
    global compress_block_counter
    global block_filename

    if block_handler.tell() + len(content) > BLOCK_SIZE:
        block_handler.close()
        compress_block_counter += 1
        block_filename = format(compress_block_counter, "08x")
        block_handler = open(COMPRESS_DIR + "/" + block_filename, "ab")

    offset = block_handler.tell()
    block_index = compress_block_counter 
    block_handler.write(content)
    assert block_handler.tell() - offset == len(content)

    return (block_index, offset, len(content))

inverted_index = dict()

# traverse each tar archive
for tar in os.listdir(TAR_DIR):
    if tar[: -4] not in words_dictionary:
        print("WARN: TAR", tar[: -4], "not in words dictionary. ")
        continue
    keywords = words_dictionary[tar[: -4]]

    print(tar, ":", keywords)

    tar_handler = tarfile.open(TAR_DIR + "/" + tar)
    for tar_mem in tar_handler.getmembers():
        content = tar_handler.extractfile(tar_mem).read()

        file_info = append_to_block(content)

        if keywords not in inverted_index:
            inverted_index[keywords] = [file_info]
        else:
            inverted_index[keywords].append(file_info)

# append inverted index
index_handler = open(INVERTED_INDEX, "a")
for keywords, positions in inverted_index.items():
    output_str = keywords + "\t"
    for pos in positions:
        for i in pos:
            output_str += format(i, "x") + ","
    output_str = output_str[: -1] + "\n"
    index_handler.write(output_str)
