#!/usr/bin/python
from re import finditer
from json import dump


def process_line(line, d):
    '''
    Gets the ID and name for each page in the line
    '''
    pattern = "\((\d+),(\d+),'(.*?)','"
    line = line.replace('\\', '')
    for match in finditer(pattern, line):
        ID, namespace, name = match.groups()
        if namespace == '0':
            d[name] = int(ID)


def main(infile='page.sql'):
    '''
    Reads page.sql line by line and processes it
    '''
    print('Making title <--> ID dictionaries...')
    path_to_data = ''
    crap = 'INSERT INTO `page` VALUES'
    t2id = {}
    for line in open(path_to_data + infile, 'rb'):
        if crap in str(line):
            process_line(str(line), t2id)
    id2t = {v: k for k, v in t2id.items()}
    dump(t2id, open(path_to_data + 'title-ID_dict.json', 'w'))
    dump(id2t, open(path_to_data + 'ID-title_dict.json', 'w'))
    print('Making title <--> ID dictionaries... Done')


if __name__ == "__main__":
    main()
