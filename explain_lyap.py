import sys
from pickle import load

from utils import concept_to_dense_id, similarity


def main(path_to_data, file_d, query):
    d2s = load(open(path_to_data + 'dense_to_sparse.pickle'))
    i2t = load(open(path_to_data + 'ID-title_dict.pickle'))
    t2i = load(open(path_to_data + 'title-ID_dict.pickle'))
    s2d = load(open(path_to_data + 'sparse_to_dense.pickle'))
    p_c = [query]
    p_ids = list(map(concept_to_dense_id, [t2i], [s2d], p_c))
    print("The query is '{0}'".format(p_c[0]))
    similarity(p_ids, path_to_data, file_d, d2s=d2s, i2t=i2t)


if __name__ == "__main__":
    if sys.argv[3] is None:
        raise Exception('Script must contains path to folder with .json and to .mat file and query')
    path_to_data = sys.argv[1]
    mat_filename = sys.argv[2]
    query = sys.argv[3]
    main(path_to_data, mat_filename, query)
