#!/usr/bin/python
from json import dump, load
from tqdm import tqdm


def main(infile='graph.txt'):
    '''
    Reads page.sql line by line and processes it
    '''
    print('Making exists titles...')
    path_to_data = ''
    i2t = load(open(path_to_data + 'ID-title_dict.json', 'r'))
    exists = []
    lines = tqdm(open(path_to_data + infile, 'r').readlines())
    for line in lines:
        title_id, _, _ = line.split(' ')
        if i2t[title_id] not in exists:
            exists.append(i2t[title_id])
    dump(exists, open(path_to_data + 'category-titles.json', 'w'))
    print('Done')


if __name__ == "__main__":
    main()
