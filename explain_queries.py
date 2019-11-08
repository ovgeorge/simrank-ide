import math
import sys
from itertools import cycle
from json import load

import matplotlib.pyplot as plt
import numpy as np
from scipy import interp
from sklearn.metrics import roc_curve, auc
from tqdm import tqdm

from utils import concept_to_dense_id, similarity_for_query


def main(path_to_data, matfile):
    d2s = load(open(path_to_data + 'dense_to_sparse.json', 'r'))
    i2t = load(open(path_to_data + 'ID-title_dict.json', 'r'))
    t2i = load(open(path_to_data + 'title-ID_dict.json', 'r'))
    s2d = load(open(path_to_data + 'sparse_to_dense.json', 'r'))
    i2c = load(open(path_to_data + 'ID-to-category.json', 'r'))
    category_titles = load(open(path_to_data + 'category-titles.json', 'r'))
    category_titles = category_titles[:50]  # random.sample(category_titles, 500) if need random
    total_cat = {}
    titles = tqdm(category_titles)
    for title in titles:
        p_c = [title]
        p_ids = list(map(concept_to_dense_id, [t2i], [s2d], p_c))
        computed_categories = similarity_for_query(p_ids, path_to_data, matfile, d2s=d2s, i2c=i2c, i2t=i2t)
        if not computed_categories:
            continue
        for computed in computed_categories:
            if computed not in total_cat:
                total_cat[computed] = {
                    'label': [],
                    'predict': [],
                    'total': 0
                }
            total_cat[computed]['label'].append(computed_categories[computed]['label'])
            total_cat[computed]['predict'].append(computed_categories[computed]['predict'])
            total_cat[computed]['total'] += 1

    top_k = sorted(total_cat.items(), key=lambda k: -k[1]['total'])[:5]
    top_k = {cat[0]: cat[1] for cat in top_k}
    fpr, tpr, roc_auc = {}, {}, {}

    for cat in top_k:
        fpr[cat], tpr[cat], _ = roc_curve(np.array(top_k[cat]['label']), np.array(top_k[cat]['predict']), pos_label=1)
        roc_auc[cat] = auc(fpr[cat], tpr[cat])
        if math.isnan(roc_auc[cat]):
            fpr[cat] = tpr[cat]
            roc_auc[cat] = auc(fpr[cat], tpr[cat])

    all_fpr = np.unique(np.concatenate([fpr[i] for i in top_k]))
    mean_tpr = np.zeros_like(all_fpr)
    for i in top_k:
        mean_tpr += interp(all_fpr, fpr[i], tpr[i])
    mean_tpr /= len(top_k)
    fpr['macro'] = all_fpr
    tpr['macro'] = mean_tpr
    roc_auc['macro'] = auc(fpr['macro'], tpr['macro'])

    plt.figure()
    lw = 2
    colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'green', 'red'])
    for cat, color in zip(top_k, colors):
        plt.plot(fpr[cat], tpr[cat], color=color, lw=lw,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                       ''.format(cat, roc_auc[cat]))
    plt.plot(fpr['macro'], tpr['macro'],
             label='macro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc['macro']),
             color='navy', linestyle=':', linewidth=4)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.savefig('data.png')
    plt.show()


if __name__ == "__main__":
    if sys.argv[2] is None:
        raise Exception('Script must contains path to folder with .json and to .mat file')
    path_to_data = sys.argv[1]
    mat_filename = sys.argv[2]
    main(path_to_data, mat_filename)
