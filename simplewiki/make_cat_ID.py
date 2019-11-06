#!/usr/bin/python
from re import finditer
from json import dump


def process_line(line, d):
    '''
    Gets the ID and name for each page in the line
    '''
    pattern = "\((\d+),'(.+?)','.+?','\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}','.*?','\w+?','(\w+)'\)"
    line = line.replace('\\', '')
    for match in finditer(pattern, line):
        ID, name, namespace = match.groups()
        if ID not in d:
            d[ID] = []
        if namespace == 'page':
            d[ID].append(name)

def main(infile = 'categorylinks.sql'):
    '''
    Reads page.sql line by line and processes it
    '''
    print('Making title <--> ID cat dictionaries...')
    path_to_data = ''
    crap = 'INSERT INTO `categorylinks` VALUES'
    id2cat = {}
    for line in open(path_to_data + infile, 'rb'):
        if crap in str(line):
            process_line(str(line), id2cat)
    dump(id2cat, open(path_to_data + 'ID-to-category.json', 'w'))
    print('Making title <--> ID cat dictionaries... Done')
if __name__ == "__main__":
    main()
