#!/usr/bin/python
from re import finditer
from cPickle import dump


def process_line(line, d):
    '''
    Gets the ID and name for each page in the line
    '''
    pattern = "\((\d+),(\d+),'(.*?)','"
    for match in finditer(pattern, line):
        ID, namespace, name = match.groups()
        if namespace == '0':
            d[name] = int(ID)


def main(infile = 'page.sql'):
    '''
    Reads page.sql line by line and processes it
    '''
    print 'Making title <--> ID dictionaries...'
    path_to_data = ''
    crap = 'INSERT INTO `page` VALUES'
    t2id = {}
    for line in open(path_to_data + infile):
        if line[:len(crap)] == crap:
            process_line(line, t2id)
    id2t = {v: k for k, v in t2id.iteritems()}
    dump(t2id, open(path_to_data + 'title-ID_dict.pickle', 'w'), 2)
    dump(id2t, open(path_to_data + 'ID-title_dict.pickle', 'w'), 2)
    print 'Making title <--> ID dictionaries... Done'
if __name__ == "__main__":
    main()
