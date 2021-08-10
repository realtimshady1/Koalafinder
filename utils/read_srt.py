import re


def extract_content(content):
    # check if content is empty
    if content:
        # extract the time and content data
        time, info = re.sub('<[^>]+>', '', content).split('\n')[3:]
        
        # convert the information to a dictionary
        info = dict(re.sub('\[|\]| ', '', idx).split(':', 1) for idx in info.split('] ['))
        
        # update timestamp to the dictionary
        info.update({'timestamp': time})    
        
        return info


def read_srt(file_name):
    # read the file
    with open(file_name, 'r') as f:
        lines = re.split('\n\n', f.read())
        
    # parse contents to srt conversion
    contents = [extract_content(line) for line in lines]
    
    return contents
