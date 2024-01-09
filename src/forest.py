import numpy as np

from model import Model
from tree import DecisionTreeClassifier


class RandomForestClassifier(Model):
    def __init__(self, n_trees: int = 100, max_depth: int = 3, min_samples_split: int = 2):
        """
        :param n_trees: Number of decision trees.
        :param max_depth: Maximum depth of a decision tree.
        :param min_samples_split: Minimum number of samples to split data into right and left nodes.
        """
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split

        self.decision_trees = None

    def fit(self, x: np.ndarray, y: np.ndarray):
        """
        Grow a random forest by creating and training multiple decision trees.
        :param x: Training data.
        :param y: Targets.
        :return:
        """
        self.decision_trees = []

        for _ in range(self.n_trees):
            decision_tree = DecisionTreeClassifier(max_depth=self.max_depth, min_samples_split=self.min_samples_split)
            x_new, y_new = self._bootstrap_dataset(x, y)

            decision_tree.fit(x_new, y_new)
            self.decision_trees.append(decision_tree)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict labels by passing each data sample through all trees and taking the most common prediction
        across the forest.
        :param x: Test data.
        :return: Predictions.
        """
        forest_preds = np.array([tree.predict(x) for tree in self.decision_trees])  # Shape is (n_trees, n_samples)
        forest_preds = np.swapaxes(forest_preds, axis1=0, axis2=1)  # Swap axes to be (n_samples, n_trees)

        predictions = np.array([self._find_most_common(tree_pred) for tree_pred in forest_preds])
        return predictions

    def _bootstrap_dataset(self, x: np.ndarray, y: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Creates new 'x' and 'y' datasets of the original size, but the same element can occur multiple times
        in the new datasets.
        :param x: Training data.
        :param y: Targets.
        :return: Bootstrapped 'x', Bootstrapped 'y'
        """
        n_samples, _ = x.shape

        indices = np.random.choice(a=n_samples, size=n_samples, replace=True)
        x_new, y_new = x[indices], y[indices]

        return x_new, y_new

    def _find_most_common(self, y: np.ndarray) -> int:
        """
        Find the most common class in the array of targets.
        :param y: Targets.
        :return: Most common class.
        """
        most_common = np.bincount(y).argmax()
        return most_common
