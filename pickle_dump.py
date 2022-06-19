import pickle
from random_loader import create_dataset as create_rand
from copious_loader import create_dataset as create_cop

random = "pickle/random.pickle"
copious = "pickle/copious.pickle"
copious_test = "pickle/copious_test.pickle"


def dump():
    """
    Helper function to write to pickle files.
    """

    rand_data = create_rand()
    cop_data  = create_cop()
    cop_test_data = create_cop(path='../data/copious_published/test')

    with (open(random, 'wb')) as f:
        pickle.dump(rand_data, f)

    with (open(copious, 'wb')) as f:
        pickle.dump(cop_data, f)

    with (open(copious_test, 'wb')) as f:
        pickle.dump(cop_test_data, f)


def rand_load():
    """
    Helper function for loading the random dataset from pickle
    """
    rand = []
    with (open(random, 'rb')) as f:
        rand = pickle.load(f)
    return rand


def cop_load():
    """
    Helper function for loading the copious dataset from pickle
    """
    cop = []
    with (open(copious, 'rb')) as f:
        cop = pickle.load(f)
    return cop

def cop_test_load():
    """
    Helper function for loading the copious TEST dataset from pickle
    """
    cop_test = []
    with (open(copious_test, 'rb')) as f:
        cop_test = pickle.load(f)
    return cop_test

# dump()

