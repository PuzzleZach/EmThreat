'''
chunking.py


Will review if there is an easier way to handle this.

Chunking will create blocks of X URLs each to run LCS on.
Data should be sorted anyways before chunking so similar URLs are ran in the same block.
The top results from each block are saved to a new list.
That final list is ran through LCS one last time if desired.
'''
import math

# Controls the threads in emthreat.py as well!!
BLOCK_SIZE = 20
# Returns an array of X blocks.
# If 1000 results are passed to 10 blocks, then each block has 100 results. 
# [[block1], [block2],...[blockn]]
# [[url11, url12, url1n],...[urln1, urln2, urlnn]]
def block_gen(results):
    # Our blocks will be broken into 1/4th the size of results.
    block_length = len(results) // BLOCK_SIZE 
    # Calculate the total blocks used.
    block_total = BLOCK_SIZE
    # Create a 2D array to store blocks.
    # [[block1], [block2],...[blockn]]
    blocks = [[]]
    for index in range(block_total-1):
        new_row = []
        blocks.append(new_row)
    # Go over each new block.
    for block in range(len(blocks)):
        for index in range(1, block_length + 1):
            # Row 0 + block length means 0-10
            # Row 1 + block length means 11-21
            try:
                blocks[block].append(results[(block_length * block + index) -1])
            except:
                #print(f"Error:")
                #print(block_length * i + j)
                pass
    return blocks
