
'''
lcs.py
This code is used to handle the longest common substring algorithm 
and a driver that will go over an input of URL paths.

The result is a dictionary of paths and the count of times they have been seen.
'''

# SequenceMatcher implementation to return the longest match.
def lcs(s1, s2):
    from difflib import SequenceMatcher
    seq = SequenceMatcher(None, s1, s2)
    lcs = seq.find_longest_match(0, len(s1),0, len(s2))
    if (lcs.size != 0):
        return str(s1[lcs.a: lcs.a + lcs.size])
    else:
        return ""


def lcs_driver(combos):
    urls = {}
    tried = {}
    # This is a driver that runs in async with other threads.
    # It will run over a subset of the combo list.
    for pair in combos:
        # For each combo, we grab the 2 URLs in it.
        word1 = pair[0]
        word2 = pair[1]
        # Ignore the same value
        if word1 == word2:
            pass
        # And inversions. This way we dont compute the same pair in reverse order.
        if (tried.get(word1 + word2) is not None) or (tried.get(word2 + word1) is not None):
            continue
        else:
            # Add i=j and j=i to the dictionary to make sure we don't call LCS on it later.
            tried[word1 + word2], tried[word2 + word1] = 1, 1      

        # Run the actual LCS function on this.
        holder = lcs(word1, word2) 

        # If we have already seen a substring, its count is incremented.
        if urls.get(holder) is not None:
            urls[holder] += 1
        # Otherwise it is added.
        else:
            urls[holder] = 1
    return urls


# Maintaining 2 dictionaries in the driver.
# As well as an n-length list using a n^2 loop.
def driver(wordlist):
    import itertools
    # Goes over the wordlist to find all combinations of words that we will run across.
    combos = [ combo for combo in itertools.combinations(wordlist,2)]
    urls = lcs_driver(combos)
    return urls
