from cPickle import load, dump
from scipy.io import savemat, mmwrite
from scipy.sparse import coo_matrix

path_to_data = ''


def create_compact_dicts():
    print 'Compactifying...'
    sparse_to_dense, dense_to_sparse = {}, {}
    k = 0
    for line in open(path_to_data + 'graph.txt'):
        k = k + 1
        if k % 100000 == 0:
            print k
        # FIX id generation!!!1111
        IDs = line.split()
        for id in IDs:
            ID = int(id)
            if ID not in sparse_to_dense:
                i = len(dense_to_sparse)
                sparse_to_dense[ID] = i
                dense_to_sparse[i] = ID
    print len(sparse_to_dense)
    print len(dense_to_sparse)
    dump(sparse_to_dense, open(path_to_data + 'sparse_to_dense.pickle', 'w'), 2)
    dump(dense_to_sparse, open(path_to_data + 'dense_to_sparse.pickle', 'w'), 2)
    print 'Compactifying... Done'


def create_matrix():
    sparse_to_dense = load(open(path_to_data + 'sparse_to_dense.pickle'))
    print 'Reading graph file and matrixifying...'
    I, J = [], []
    for line in open(path_to_data + 'graph.txt'):
        converted = [sparse_to_dense.get(int(ID)) for ID in line.split()]
        i = converted[0]
        j = converted[1]
        I.append(i)
        J.append(j)
    n = max([max(I), max(J)]) + 1
    data = [1] * len(I)
    print 'Reading graph file and matrixifying... Done'
    return coo_matrix((data, (I, J)), shape = (n, n), dtype = 'i4')


def main():
    create_compact_dicts()
    W = create_matrix()
    savemat(path_to_data + 'W.mat', dict(W = W + W.T))

if __name__ == '__main__':
    main()
