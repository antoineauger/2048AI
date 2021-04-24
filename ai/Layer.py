# coding: utf-8
import numpy as np

# Uncomment to get the same results when generating random numbers
# np.random.seed(100)


class Layer:
    """
    Represents a layer (hidden or output) in our neural network
    """

    def __init__(self, n_input, n_neurons, weights=None, bias=None):
        """
        @param n_input: The input size (coming from the input layer or a previous hidden layer)
        @type n_input: int
        @param n_neurons: The number of neurons in this layer
        @type n_neurons: int
        @param weights: The layer's weights
        @type weights: np.array

        @param bias: The layer's bias
        @type bias: np.array
        """
        self.weights = weights if weights is not None else np.random.rand(n_input, n_neurons)
        self.bias = bias if bias is not None else np.random.rand(n_neurons)
        self.last_activation = None
        self.error = None
        self.delta = None

    @staticmethod
    def apply_activation(r):
        """
        Applies the sigmoid activation function

        @param r: The normal value
        @type r: np.array

        @return: The "activated" value
        @rtype: np.array
        """
        return 1 / (1 + np.exp(-r))

    @staticmethod
    def apply_activation_derivative(r):
        """
        Applies the derivative of the sigmoid activation function

        @param r: The normal value
        @type r: np.array

        @return: The "derived" value
        @rtype: np.array
        """
        # We use 'r' directly here because its already activated, the only values that
        # are used in this function are the last activations that were saved.
        return r * (1 - r)

    def activate(self, x):
        """
        Calculates the dot product of this layer.

        @param x: The input
        @type x: np.array

        @return: The result
        @rtype: np.array
        """
        r = np.dot(x, self.weights) + self.bias
        self.last_activation = self.apply_activation(r)
        return self.last_activation
