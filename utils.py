import numpy as np
import scipy.sparse as scsp
from scipy.io import loadmat
from sklearn.preprocessing import normalize


def simrank_single_source(W, d, x, num_items=100):
    '''
    This function computes approximate SimRank similarities
    for given query in vector x
    '''
    n = W.shape[0]
    D = scsp.spdiags(d, 0, n, n)
    s = D.dot(x)
    for i in range(num_items):
        wx = W.dot(x)
        dwx = D.dot(wx)
        for k in range(i + 1):
            wtdwx = W.T.dot(dwx)
            dwx = wtdwx
        s = s + dwx
        x = wx
    return s


def load_data(path_to_data, file_d):
    d = loadmat(path_to_data + file_d)['d']
    W = loadmat(path_to_data + 'W.mat')['W']
    W = normalize(W * 1.0, norm='l1', axis=0)
    return d, W


def concept_to_dense_id(t2i, s2d, concept):
    id_s = t2i[concept]
    return s2d[str(id_s)]


def dense_id_to_concept(d2s, i2t, d_id):
    s_id = d2s[str(d_id)]
    return i2t[str(s_id)]


def dense_id_to_cat(d2s, i2c, d_id):
    s_id = str(d2s[str(d_id)])
    return i2c[s_id] if s_id in i2c else None


def get_simrank_by_ids(p_ids, path_to_data, file_d):
    d, W = load_data(path_to_data, file_d)
    n = max(W.shape)
    c = 0.4
    x = np.zeros((n, 1))
    nrm_p = len(p_ids)
    for id in p_ids:
        x[id, 0] = 1.0 / nrm_p
    s = simrank_single_source(np.sqrt(c) * W, d, x, 20)
    idx = sorted(list(range(max(s.shape))), key=lambda k: -s[k])
    return idx, s


def similarity(p_ids, path_to_data, file_d, d2s, i2t):
    print('Compute Simrank...')
    idx, s = get_simrank_by_ids(p_ids, path_to_data, file_d)
    print('Compute Simrank... Done')

    for k in range(30):
        d_id = idx[k]
        try:
            print(s[d_id], dense_id_to_concept(d2s, i2t, d_id))
        except:
            pass


def similarity_for_query(p_ids, path_to_data, file_d, d2s, i2t, i2c):
    idx, s = get_simrank_by_ids(p_ids, path_to_data, file_d)
    q_name = dense_id_to_concept(d2s, i2t, idx[0])
    # print('Main categories for {}'.format(q_name))
    original_categories = dense_id_to_cat(d2s, i2c, idx[0])
    if not original_categories:
        return
    categories_score = {}
    top_k = [rank[0] for rank in s[idx] if rank > 0.025]
    for k, score in enumerate(top_k):
        d_id = idx[k]
        try:
            categories = dense_id_to_cat(d2s, i2c, d_id)
            for category in categories:
                if category not in categories_score:
                    categories_score[category] = 0
                categories_score[category] += 1
        except:
            pass
    predicted = {cat: categories_score[cat] / len(top_k) for cat in categories_score}
    predicted = sorted(predicted.items(), key=lambda x: -x[1])
    predicted = {cat[0]: cat[1] for cat in predicted if cat[1] > 0.75}
    result = {}
    for category in predicted:
        result[category] = {
            'label': 0,
            'predict': 0.0
        }

        if category in original_categories:
            result[category]['label'] = 1
        result[category]['predict'] = predicted[category]

    return result
