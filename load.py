import scipy.io
import numpy as np
from sklearn.preprocessing import normalize


def wiki(matfile_name, c):
    '''
    This function loads adjacency matrix from mat-file
    with wiki-graph
    '''
    print("Create graph...")
    A = scipy.io.loadmat(matfile_name)['W']
    W = A.tocsr()
    W.data = W.data * 1.0
    Wn = normalize(W, norm='l1', axis=0)
    Wn.data = Wn.data * np.sqrt(c)
    print("Create graph... Done")
    print("The size of adjacency matrix", Wn.shape)
    return Wn
