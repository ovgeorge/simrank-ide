from cPickle import load, dump
from scipy.io import savemat, mmwrite
from scipy.sparse import coo_matrix

def create_compact_dicts():
    print 'Compactifying...'
    sparse_to_dense, dense_to_sparse = {}, {}
    k = 0.0
    f = open('graph.txt')
    lines = f.readlines()
    f.close()
    mk_step = 20
    step = len(lines) / mk_step
    for l in lines:
        k = k + 1
        if k % step == 0:
            print "%d%% done" % (100 / mk_step * k / step)
        IDs = l.split()
        for id in IDs:
            ID = int(id)
            if ID not in sparse_to_dense:
                i = len(dense_to_sparse)
                sparse_to_dense[ID] = i
                dense_to_sparse[i] = ID
    dump(sparse_to_dense, open('sparse_to_dense.pickle', 'w'), 2)
    dump(dense_to_sparse, open('dense_to_sparse.pickle', 'w'), 2)
    print 'Compactifying... Done'


def create_matrix():
    sparse_to_dense = load(open('sparse_to_dense.pickle'))
    print 'Reading graph file and matrixifying...'
    I, J = [], []
    for line in open('graph.txt'):
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
    savemat('W.mat', dict(W = W + W.T))

if __name__ == '__main__':
    main()
