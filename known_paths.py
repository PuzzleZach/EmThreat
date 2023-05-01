

'''
This class will be used to take in a list of JSON objects.
{"application": ["software_path1", "software_path2", ...], "application2": [...]}
It will go over the 2D array of [['url', count], ['url2', count2]] and match them to the software.
Then we build a dictionary showing the total count for each application. 
'''

# We will have a function import this from a file later
software_json = {
    "WordPress": ["wp-includes", "wp-admin"]
}

def identify_software(url_array):
    software_count = {}
    # Need to find a way to reduce the cost of this.
    for url in url_array:
        for row in software_json:
            found_url = [x in url[0] for x in software_json[row]]
            if True in found_url:
                if row not in software_count:
                    software_count[row] = 1
                else:
                    software_count[row] += 1
                    
    return software_count
