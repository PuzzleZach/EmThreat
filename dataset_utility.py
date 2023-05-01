'''
dataset_utility.py
This file contains helper functions for interacting with datasets and curing data.
Will contain generic functions in the future to interact with a broad array of data inputs.
'''
def import_json(dataset):
    dataset = 'verified_online.json'
    import json # Handling json file
    ips= []
    with open(dataset) as file:
            data = json.load(file)
            for entry in range(len(data)):
                    try:
                            ips.append(data[entry]["details"][0]["ip_address"]) # Grab IP addresses
                    except: # Some entries are missing ip_address or are not formatted properly.
                            pass
    print(f"Unique IPs: {len(set(ips))}") # Use a set to find unique IPs
    # Going over the PhishTank json data to find unique IPs.
    return ips

def data_to_excel(data, column):
    import pandas as pd
    from pandas import ExcelWriter
    from pandas import ExcelFile
    # change IPs to the generic later
    df = pd.DataFrame({'IPs':list(set(ips))})
    # This saves those unique IPs to a spreadsheet.
    # Could definitely do a lot here.
    writer = ExcelWriter('PhishTank-IPs.xlsx')
    df.to_excel(writer,column,index=False)
    writer.save()

# Only grab high level paths.
def high_level(url):
    dir_count = 3
    # Now if the URL has 3 or more /'s, we want it.
    total = url.count("/")
    if total >= dir_count:
        return True
    return False

# Checks path against our criteria.
def check_path(url):
    min_length = 5
    max_length = 80
    # If the length is between what we want, return it.
    if len(url) > min_length and len(url) < max_length:
        return True
    else:
        return False

def remove_parameters(url):
    # Cleaning up the URL by removing parameters.
    params = "?"
    if params in url:
        return url.split(params)[0]
    return url

def remove_websites(url):
    # Cleaning up the URL by removing websites.
    sites = ["http://", "https://", "https//", "http//"]
    for pretext in sites:
        if pretext in url:
            return url.split(pretext)[0]
    return url

def find_emails(url):
    import re
    # Search for emails
    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", url)
    if len(emails) > 0:
        # If we have an email, split on the first one.
        # Then return everything in front of it.
        return url.split(emails[0])[0]
    return url

# Pull out just the paths of URLs.
def path_clean(urls):
    # List our prevalent paths.
    paths = [] 
    # Go over URLs array and only append values that meet our criteria.
    for value in urls:
        try:
            # Remove https://
            url = value.split("//", 1)[1]
            url_path = high_level(url)

            if url_path:
                #Split on the end of the TLD.
                split_url = url.split("/", 1)[1]
                param_url = remove_parameters(split_url)
                web_url = remove_websites(param_url)
                email_url = find_emails(web_url)

                url_check = check_path(email_url)
                if url_check:
                    paths.append(email_url)
        except:
            #If an error happens, ignore the input.
            pass
    return sorted(paths)
