from scipy.io import loadmat
from cPickle import load
import h5py
import numpy as np
import scipy.sparse as scsp

def simrank_single_source(W, d, x, num_items=100):
    '''
    This function computes approximate SimRank similarities
    for given query in vector x
    '''
    print "SimRank for given query computed..."
    n = W.shape[0]
    D = scsp.spdiags(d, 0, n, n)
    s = D.dot(x)
    for i in xrange(num_items):
        wx = W.dot(x)
        dwx = D.dot(wx)
        for k in xrange(i+1):
            wtdwx = W.T.dot(dwx)
            dwx = wtdwx
        s = s + dwx
        x = wx
    print "SimRank for given query computed... Done"
    return s

def load_data(file_d):
    from sklearn.preprocessing import normalize 

    print 'Loading data...'
    d = loadmat(path_to_data + file_d)['d']
    W = loadmat(path_to_data + 'W.mat')['W']
    W =  normalize(W * 1.0, norm='l1', axis=0)
    # W = h5py.File(path_to_data + 'Wn.mat')['W']
    print 'Loading data... Done'
    print 'The size of d', d.shape
    print 'The size of W', W.shape
    return d, W

def concept_to_dense_id(concept):
    global t2i
    id_s = t2i[concept]
    return s2d[id_s]

def dense_id_to_concept(d_id):
    global d2s
    s_id = d2s[d_id]
    return i2t[s_id]


def similarity(p_ids, file_d):
    d, W  = load_data(file_d)
    n = max(W.shape)
    c = 0.4
    x = np.zeros((n, 1))
    nrm_p = len(p_ids)
    for id in p_ids:
        x[id,0] = 1.0/nrm_p
    print 'Compute Simrank...'
    s = simrank_single_source(np.sqrt(c) * W, d, x, 20)
    print 'Compute Simrank... Done'
    idx = sorted(range(max(s.shape)), key=lambda k: -s[k])
    for k in range(30):
        d_id = idx[k]    
        try:
            print s[d_id], dense_id_to_concept(d_id)
        except:
            pass	       

def main(q, file_d):
    p_c = [q]
    p_ids = map(concept_to_dense_id, p_c)
    n_ids = []
    print "The query is '{0}'".format(p_c[0])
    similarity(p_ids, file_d)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        sys.exit('Usage: %s path_to_directory file_with_diagonal.mat query \n file_with_diagonal.mat, and all other necessary data assumed to be located at path_to_direcoty' % sys.argv[0])
    global path_to_data 
    path_to_data = sys.argv[1]
    query = sys.argv[3]
    global d2s, i2t, t2i, s2d
    
    d2s = load(open(path_to_data +'dense_to_sparse.pickle'))
    i2t = load(open(path_to_data +'ID-title_dict.pickle'))
    t2i = load(open(path_to_data +'title-ID_dict.pickle'))
    s2d = load(open(path_to_data +'sparse_to_dense.pickle'))
    
    main(query, sys.argv[2])
