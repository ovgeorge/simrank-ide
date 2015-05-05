import numpy as np
import scipy.io as sio
import time
import load
import explain_lyap
import numpy as np
import scipy.sparse as scsp

def my_callback(x):
    print 'Current residual =', x


def solve_system(y, matvec, call=my_callback):
    '''
    This function solves system by GMRES method with special matvec and
    right-hand side y
    '''
    n = max(y.shape)
    print 'Solving key linear system...'
    LA = scsp.linalg.LinearOperator((n, n), matvec=matvec, dtype=np.float64)
    d, info = scsp.linalg.gmres(LA, y, x0=y, callback=call)
    print 'Solving key linear system... Done'
    return d, info


def matvec(x, num_iter=10, threshold=1e-4):
    '''
    This function approximates matvec for GMRES method
    '''
    global W
    d = x.copy()
    XS = scsp.csr_matrix(scsp.diags(x, 0))
    for _ in xrange(num_iter):
        XS = W.T.dot(XS).dot(W)
        cond = abs(XS.data) > threshold
        not_cond = np.logical_not(cond)
        XS.data[not_cond] = 0.0
        XS.eliminate_zeros()
        if XS.data.shape[0] == 0:
            break
        d = d + XS.diagonal()
    return d



    
def mat_mat(i):
    global A, W, threshold
    c = A.dot(W[:, blocks[i]:blocks[i+1]])
    s = "Elements in c %d size: %3f mb" % (c.nnz, c.data.nbytes / 1024.0 / 1024.0)
    if c.nnz == 0:
        return
    else:
        pass    
     
    cond = abs(c.data) > threshold
    not_cond = np.logical_not(cond)
    c.data[not_cond] = 0.0
    c.eliminate_zeros()
    
    print s
    print "Thresholding. Elements in c ", c.nnz, ' size: ', c.data.nbytes / 1024.0 / 1024.0, "mb"

    row = c.nonzero()[0]
    col = c.nonzero()[1] + blocks[i]
    C = scsp.csr_matrix((c.data, (row, col)), shape=A.shape)
    return C


def block_mat_mat(parts, threshold=1e-3):
    global A
    D = scsp.csr_matrix(A.shape)
    n = A.shape[0]
    elements_in_part = n / parts
    print "Number co.datalumns in part", elements_in_part
    elements_in_last_part = n % parts
    print "Number columns in the last part", elements_in_last_part
    start = 0
    global blocks
    blocks = [0 for _ in xrange(parts + 1)]
    for i in xrange(parts + 1):
        blocks[i] = start
        if (i + 1) != parts or elements_in_last_part == 0:
            start += elements_in_part
        else:
            start += elements_in_last_part
            start += elements_in_part
    
    from multiprocessing import Pool 
    pool = Pool(4)
    result = pool.map(mat_mat, xrange(parts))
  
    pool.close()
    pool.join()

    for C in result:
        if C != None:
            D = D + C
    return D

def matvec_block(x, num_iter=10, threshold=1e-4):
    '''
    This function approximates matvec for GMRES method
    '''
    d = x.copy()
    XS = scsp.csr_matrix(scsp.diags(x, 0))
    global W, A 
    for _ in xrange(num_iter):
        A = W.T.dot(XS) 
        XS = block_mat_mat(1000, threshold) # number of blocks we partition matrix for multiplication.
        # adjust as needed. More blocks require less memory, but execution will be slower.
        if XS.data.shape[0] == 0:
            break
        d = d + XS.diagonal()
    return d




def my_matvec(x):
    return matvec(x, num_iter=10, threshold=threshold)

def my_block_matvec(x):
    return matvec_block(x, num_iter=10, threshold=threshold)
    
if __name__ == "__main__":
    path_to_data = "./simplewiki/"
    threshold = 2 * 1e-2
    output_filename = "d_simplewiki_2e-2"
    #G = Graph.load(path_to_data + 'delaunay_n10.mat', c=0.8)
    global W
    W = load.wiki(path_to_data + "W.mat", c=0.4)
    n = W.shape[0]
    # G = Graph.load_wiki(path_to_data + "W_enwiki.mat", c=0.4)
    num_iter = 10
    # S = G.simrank(num_iter)
    y = np.ones((n, 1))
    t1 = time.time()
    #d, info = solve_system(y, my_matvec, call=my_callback) #works on smaller datasets
    d, info = solve_system(y, my_block_matvec, call=my_callback) # scalable version, but with performance issues due to scipy sparse matrix realization
    t2 = time.time()
    print "The system is solved in", t2 - t1, "sec."
    print "GMRES output flag", info
    sio.savemat(path_to_data + output_filename, {"d": d})
