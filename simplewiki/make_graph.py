#!/usr/bin/python
from re import finditer
from cPickle import load


def process_line(line, t2i, i2t, outfile):
    '''
    Prints outlinks for each page.

    Example contents of line:
    ...'),(12,0,'A._S._Neill'),(12,0,'AK_Press'),(12,0,...

    Each tuple is of the form ('from' page, namespace, 'to' page).  Print a
    line for each 'from' page with the outlinks that are in namespace 0 (the
    main wikipedia, ignores 'talk' pages, etc). Annoyingly, the 'from' pages
    are given by ID and the 'to' pages by name. Use the dictionary d to map the
    text names to IDs for consistency (and some space savings).
    '''
    pattern = "\((\d+),(\d+),'(.*?)',(\d+)\)[,;]"
    current_page = None
    for match in finditer(pattern, line):
        from_page, namespace, to_page, namespce2 = match.groups()
        if not to_page in t2i:
            continue
        if namespace != '0':
            continue
        if not int(from_page) in i2t:
            continue
        outfile.write(from_page + ' ')
        outfile.write(str(t2i[to_page]) + ' ')
        outfile.write('\n')


def main():
    '''
    Reads pagelinks.sql line by line and processes it. Needs the pickled
    dictionary mapping page names to IDs
    '''
    print "Building the graph..."
    crap = 'INSERT INTO `pagelinks` VALUES'
    path = ''  # set if needed (different current dir)
    t2i = load(open(path + 'title-ID_dict.pickle'))
    i2t = load(open(path + 'ID-title_dict.pickle'))

    with open(path + 'graph.txt', 'w') as outfile:
        for line in open(path + 'pagelinks.sql'):
            if line[:len(crap)] == crap:
                process_line(line, t2i, i2t, outfile)
    print "Building the graph... Done"

if __name__ == "__main__":
    main()
