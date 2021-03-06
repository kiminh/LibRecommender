from array import array
from collections import defaultdict
from scipy.sparse import csr_matrix
from distributed.new_features.utils.samplingNEW import NegativeSamplingFeat


class TransformedSet(object):
    def __init__(self, user_indices=None, item_indices=None, labels=None, sparse_indices=None,
                 dense_indices=None, dense_values=None, train=True):
        self._user_indices = user_indices
        self._item_indices = item_indices
        self._labels = labels
        self._sparse_indices = sparse_indices
        self._dense_indices = dense_indices
        self._dense_values = dense_values
        if train:
            self._sparse_interaction = csr_matrix(
                (self.labels, (self.user_indices, self.item_indices))
            )
        self._user_consumed, self._item_consumed = self.__interaction_consumed()
        self.sparse_indices_sampled = None
        self.dense_indices_sampled = None
        self.dense_values_sampled = None
        self.label_samples = None

    def __interaction_consumed(self):
        user_consumed = defaultdict(lambda: array("I"))
        item_consumed = defaultdict(lambda: array("I"))
        for u, i in zip(self.user_indices, self.item_indices):
            user_consumed[u].append(i)
            item_consumed[i].append(u)
        return user_consumed, item_consumed

    def build_negative_samples(self, data_info, num_neg=1, mode="random", seed=42):
        neg_generator = NegativeSamplingFeat(self, data_info, num_neg)
        if self.dense_values is None:
            (self.sparse_indices_sampled, self.dense_indices_sampled,
                self.dense_values_sampled, self.label_samples) = neg_generator(
                    seed, dense=False, mode=mode)
        else:
            (self.sparse_indices_sampled, self.dense_indices_sampled,
                self.dense_values_sampled, self.label_samples) = neg_generator(
                    seed, dense=True, mode=mode)

    def __len__(self):
        return len(self.sparse_indices)

    @property
    def user_indices(self):
        return self._user_indices

    @property
    def item_indices(self):
        return self._item_indices

    @property
    def sparse_indices(self):
        return self._sparse_indices

    @property
    def dense_indices(self):
        return self._dense_indices

    @property
    def dense_values(self):
        return self._dense_values

    @property
    def labels(self):
        return self._labels

    @property
    def sparse_interaction(self):
        return self._sparse_interaction

    @property
    def user_consumed(self):
        return self._user_consumed

    @property
    def item_consumed(self):
        return self._item_consumed

