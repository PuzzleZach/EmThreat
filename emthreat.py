#!/usr/bin/env python3
import requests
import sys
import argparse

from lcs import driver
from chunking import BLOCK_SIZE
from urlgraph import URLGraph
from known_paths import identify_software
from time import perf_counter as timer


import chunking
import dataset_utility
import fetch

from multiprocessing.pool import ThreadPool

'''
EmThreat is a tool to help web admins notice spikes in phishing activity
for software that they use by analyzing the URLs on PhishTank
and comparing them to URLs used by the admin.

Many websites have similar URL paths because they use the same software
so if many URLs pop up on PhishTank that match the ones used by a web admin,
that software may have a new exploit targeting it.

python3 EmThreat.py --help
'''

THREAD_COUNT = BLOCK_SIZE // 2

# Run LCS on blocks.
def block_lcs(blocks):
    # Create an array to store the dictionary outputs.
    results = []
    threads = THREAD_COUNT
    pool = ThreadPool(processes=threads)
    for block in blocks:
        # driver returns a dictionary of URLs from lcs.py.
        async_result = pool.apply_async(driver, (block,))
        result = async_result.get()
        results.append(result)
    # Returns [{url:count}, {url2:count2},...]
    return results

# Prints out results to the command line.
def print_output(results):
    # Store the results that we want in a new 2D array.
    new_results = loop_dict(results) 
    print(f"{len(new_results)} results found after cleaning output.")
    for pair in new_results:
        print(f"URL:{pair[0]} Count: {pair[1]}")

# Saves output to a file.
def save_output(results, file_name):
    with open(file_name, "w+") as file:
        new_results = loop_dict(results)
        for pair in new_results:
                file.write(f"URL:{pair[0]} Count: {pair[1]}\n")
        print(f"Wrote {len(new_results)} to {file_name}")

# Loops over a dictionary to get URLs that meet our basic criteria.
def loop_dict(results):
    # Grab total of all dictionaries.
    reslen = sum(len(block) for block in results) 
    print(f"EmThreat has found {reslen} common substrings.")
    # Min frequency and length
    new_results = []
    freq = 10
    minlength = 5
    print(f"Searching for substrings that appear more than {freq} times and are longer than {minlength} characters.")
    for pair in results:
        # For each pair in the dictionary.
        for value, count in pair.items():
            # If the URL appears enough times and is longer than a few characters.
            if count > freq and len(value) > minlength:
                new_results.append([value, count])
    
    # Send 2D array to directory_elim
    directory_only = directory_elim(new_results)
    # Returns 2D array of paths that only have directories and their counts. 
    #print(directory_only[:10])
    return directory_only

def directory_elim(results):
    # Input is a 2D array
    # [value, count]
    new_results = []
    for pair in results:
        path = pair[0]
        # If the path contains a directory level, append it. 
        is_directory_level = dataset_utility.high_level(path)
        if is_directory_level:
            new_results.append(pair)
    return new_results

if __name__ == "__main__":
    # Using ArgumentParser to handle our arguments.
    parser = argparse.ArgumentParser(description='EmThreat 1.3 is a tool to help web admins notice spikes in phishing activity for software \
        that they use by analyzing the URLs on PhishTankand comparing them to URLs used by the admin.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-f', help="db_file: The file that URLs will be read from.")
    parser.add_argument('-c', help="total_urls: The amount of URLs that will be processed.")
    parser.add_argument('-i', default="txt", choices=["csv", "json", "txt"], help="Input: Determines the file type of the database used.")
    group.add_argument('-o', default = "print", choices=["print", "save"], help="Output: Determines if saved to a file or printed to screen.")
    parser.add_argument('-n', default ="report.txt", help="Name: The name that the report file will be saved as.")
    parser.add_argument('-s', default=False, action="store_true", help="Software Paths: Prints the output of software path matches.")
    args = parser.parse_args()

    # Variables to store main actions we will take.
    total_urls = int(args.c)
    db_file = str(args.f)
    db_type = str(args.i)
    # Report type and output.
    report_output = str(args.o)
    report_name = str(args.n)
    # Additional actions
    check_softwarepaths = args.s

    # An array of URLs extracted from supported file types.
    urls = fetch.open_database(db_file, total_urls, db_type)

    # Grabs just the paths from the URLs.
    words = dataset_utility.path_clean(urls)
    start = timer()

    # Turns words into blocks.
    blocks = chunking.block_gen(words)
    # Runs LCS on each block.
    results = block_lcs(blocks)

    end = timer()
    diff = end - start
    print(f'Finished in {diff / 60} minutes\n')

    # Handle what we do after reaching our results.
    if report_output == "print":
        print_output(results)
    else:
        save_output(results, report_name)

    # Build a URLGraph object with the top 10 results of loop_dict(results) 
    cleaned_results = loop_dict(results)

    if check_softwarepaths:
        software_count = identify_software(cleaned_results)
        for software in software_count:
            print(f"There are {software_count[software]} URL paths related to {software}")
    test_output = URLGraph(cleaned_results, 10)
    test_output.build_graph()