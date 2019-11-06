from json import load, dump
from scipy.io import savemat
from scipy.sparse import coo_matrix


def create_compact_dicts(name='graph.txt'):
    print('Compactifying...')
    sparse_to_dense, dense_to_sparse = {}, {}
    k = 0.0
    file = open(name, 'r')
    lines = file.readlines()
    file.close()
    mk_step = 20
    step = len(lines) / mk_step
    for l in lines:
        k = k + 1
        if k % step == 0:
            print("%d%% done" % (100 / mk_step * k / step))
        IDs = l.split()
        for id in IDs:
            ID = int(id)
            if ID not in sparse_to_dense:
                i = len(dense_to_sparse)
                sparse_to_dense[ID] = i
                dense_to_sparse[i] = ID
    dump(sparse_to_dense, open('sparse_to_dense.json', 'w'))
    dump(dense_to_sparse, open('dense_to_sparse.json', 'w'))
    print('Compactifying... Done')


def create_matrix(name='graph.txt'):
    sparse_to_dense = load(open('sparse_to_dense.json', 'r'))
    print('Reading graph file and matrixifying...')
    I, J = [], []
    for line in open(name, 'r'):
        converted = [sparse_to_dense.get(ID) for ID in line.split()]
        i = converted[0]
        j = converted[1]
        I.append(i)
        J.append(j)
    n = max([max(I), max(J)]) + 1
    data = [1] * len(I)
    print('Reading graph file and matrixifying... Done')
    return coo_matrix((data, (I, J)), shape=(n, n), dtype='i4')


def main():
    create_compact_dicts('graph.txt')
    W = create_matrix('graph.txt')
    savemat('W.mat', dict(W=W + W.T))


if __name__ == '__main__':
    main()
