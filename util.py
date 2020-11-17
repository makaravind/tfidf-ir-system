import pickle
import os


def save_obj(obj, name):
    with open('meta/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('meta/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def is_saved(name):
    return os.path.exists('meta/' + name + '.pkl')


def print_result(document_results):
    scores_gt_zero = 0
    for item in document_results:
        if item['similarity_score'] > 0:
            print(f"""{item['document_name']} ({item['similarity_score']})""")
            scores_gt_zero += 1

    if scores_gt_zero == 0:
        print('Sorry, No documents found matching the query. Try again with different keywords')
    elif scores_gt_zero < 10:
        print(f"""Attempted to find top 10 documents but only found {scores_gt_zero} documents relevant to the query""")
