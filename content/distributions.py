"""
Distribution and utility classes avilable to these examples.
"""

import numpy as np
from typing import Optional, Union, Tuple, Any
from numpy.random import SeedSequence
from numpy.typing import NDArray, ArrayLike
import math

class Lognormal:
    """
    Lognormal distribution implementation.

    A continuous probability distribution where the logarithm of a random
    variable is normally distributed. It is useful for modeling variables that
    are the product of many small independent factors.

    Notes: taken from my in development package sim-tools
    https://github.com/TomMonks/sim-tools
    """

    def __init__(
        self,
        mean: float,
        stdev: float,
        random_seed: Optional[Union[int, SeedSequence]] = None,
    ):
        """
        Initialize a lognormal distribution.

        Parameters
        ----------
        mean : float
            Mean of the lognormal distribution.

        stdev : float
            Standard deviation of the lognormal distribution.

        random_seed : Optional[Union[int, SeedSequence]], default=None
            A random seed or SeedSequence to reproduce samples. If None, a
            unique sample sequence is generated.
        """
        self.rng = np.random.default_rng(random_seed)
        mu, sigma = self.normal_moments_from_lognormal(mean, stdev**2)
        self.mu = mu
        self.sigma = sigma
        self.mean = mean
        self.stdev = stdev

    def __repr__(self):
        return f"Lognormal(mean={self.mean}, stdev={self.stdev})"

    def normal_moments_from_lognormal(
        self, m: float, v: float
    ) -> Tuple[float, float]:
        """
        Calculate mu and sigma of the normal distribution underlying
        a lognormal with mean m and variance v.

        Parameters
        ----------
        m : float
            Mean of lognormal distribution.
        v : float
            Variance of lognormal distribution.

        Returns
        -------
        Tuple[float, float]
            The mu and sigma parameters of the underlying normal distribution.

        Notes
        -----
        Formula source:
        https://blogs.sas.com/content/iml/2014/06/04/simulate-lognormal-data-
        with-specified-mean-and-variance.html
        """
        phi = math.sqrt(v + m**2)
        mu = math.log(m**2 / phi)
        sigma = math.sqrt(math.log(phi**2 / m**2))
        return mu, sigma

    def sample(
        self, size: Optional[Union[int, Tuple[int, ...]]] = None
    ) -> Union[float, NDArray[np.float64]]:
        """
        Generate random samples from the lognormal distribution.

        Parameters
        ----------
        size : Optional[Union[int, Tuple[int, ...]]], default=None
            The number/shape of samples to generate:
            - If None: returns a single sample as a float
            - If int: returns a 1-D array with that many samples
            - If tuple of ints: returns an array with that shape

        Returns
        -------
        Union[float, NDArray[np.float64]]
            Random samples from the lognormal distribution:
            - A single float when size is None
            - A numpy array of floats with shape determined by size parameter
        """
        return self.rng.lognormal(self.mu, self.sigma, size=size)

class Exponential:
    """
    Convenience class for the exponential distribution.
    packages up distribution parameters, seed and random generator.
    """

    def __init__(self, mean, random_seed=None):
        """
        Constructor

        Params:
        ------
        mean: float
            The mean of the exponential distribution

        random_seed: int| SeedSequence, optional (default=None)
            A random seed to reproduce samples.  If set to none then a unique
            sample is created.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.mean = mean

    def sample(self, size=None):
        """
        Generate a sample from the exponential distribution

        Params:
        -------
        size: int, optional (default=None)
            the number of samples to return.  If size=None then a single
            sample is returned.

        Returns:
        -------
        float or np.ndarray (if size >=1)
        """
        return self.rand.exponential(self.mean, size=size)


class Bernoulli:
    """
    Convenience class for the Bernoulli distribution.
    packages up distribution parameters, seed and random generator.

    The Bernoulli distribution is a special case of the binomial distribution
    where a single trial is conducted

    Use the Bernoulli distribution to sample success or failure.
    """

    def __init__(self, p, random_seed=None):
        """
        Constructor

        Params:
        ------
        p: float
            probability of drawing a 1

        random_seed: int | SeedSequence, optional (default=None)
            A random seed to reproduce samples.  If set to none then a unique
            sample is created.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.p = p

    def sample(self, size=None):
        """
        Generate a sample from the exponential distribution

        Params:
        -------
        size: int, optional (default=None)
            the number of samples to return.  If size=None then a single
            sample is returned.

        Returns:
        -------
        float or np.ndarray (if size >=1)
        """
        return self.rand.binomial(n=1, p=self.p, size=size)

class DiscreteEmpirical:
    """
    DiscreteEmpirical distribution implementation.

    A probability distribution that samples values with specified frequencies.
    Useful for modeling categorical data or discrete outcomes with known
    probabilities.

    Example uses:
    -------------
    1. Routing percentages
    2. Classes of entity
    3. Batch sizes of arrivals
    4. Initial conditions - no. entities in a queue.
    """

    def __init__(
        self,
        values: ArrayLike,
        freq: ArrayLike,
        random_seed: Optional[Union[int, SeedSequence]] = None,
    ):
        """
        Initialize a discrete distribution.

        Parameters
        ----------
        values : ArrayLike
            List of possible outcome values. Must be of equal length to freq.

        freq : ArrayLike
            List of observed frequencies or probabilities. Must be of equal
            length to values. These will be normalized to sum to 1.

        random_seed : Optional[Union[int, SeedSequence]], default=None
            A random seed or SeedSequence to reproduce samples. If None, a
            unique sample sequence is generated.

        Raises
        ------
        TypeError
            If values or freq are not positive arrays
        ValueError
            If values and freq have different lengths.
        """

        # convert to array first
        self.values = np.asarray(values)
        self.freq = np.asarray(freq)

        if len(self.values) != len(self.freq):
            raise ValueError(
                "values and freq arguments must be of equal length"
            )

        self.rng = np.random.default_rng(random_seed)
        self.probabilities = self.freq / self.freq.sum()

    def __repr__(self):
        values_repr = (
            str(self.values.tolist())
            if len(self.values) < 4
            else f"[{', '.join(str(x) for x in self.values[:3])}, ...]"
        )
        freq_repr = (
            str(self.freq.tolist())
            if len(self.freq) < 4
            else f"[{', '.join(str(x) for x in self.freq[:3])}, ...]"
        )
        return f"Discrete(values={values_repr}, freq={freq_repr})"

    def sample(
        self, size: Optional[Union[int, Tuple[int, ...]]] = None
    ) -> Union[Any, NDArray]:
        """
        Generate random samples from the discrete distribution.

        Parameters
        ----------
        size : Optional[Union[int, Tuple[int, ...]]], default=None
            The number/shape of samples to generate:
            - If None: returns a single sample
            - If int: returns a 1-D array with that many samples
            - If tuple of ints: returns an array with that shape

        Returns
        -------
        Union[Any, NDArray]
            Random samples from the discrete distribution:
            - A single value (of whatever type was in the values array) when
              size is None
            - A numpy array of values with shape determined by size parameter
        """
        sample = self.rng.choice(self.values, p=self.probabilities, size=size)

        if size is None:
            return sample.item()
        return sample

class FixedDistribution:
    """
    Fixed distribution implementation.

    A degenerate distribution that always returns the same fixed value.
    Useful for constants or deterministic parameters in models.

    Provides a method to
    sample a constant value regardless of the number of samples requested.
    """

    def __init__(self, value: float):
        """
        Initialize a fixed distribution.

        Parameters
        ----------
        value : float
            The constant value that will be returned by sampling.
        """
        self.value = value

    def __repr__(self):
        return f"FixedDistribution(value={self.value})"

    def sample(
        self, size: Optional[Union[int, Tuple[int, ...]]] = None
    ) -> Union[float, NDArray[np.float64]]:
        """
        Generate "samples" from the fixed distribution (always the same value).

        Parameters
        ----------
        size : Optional[Union[int, Tuple[int, ...]]], default=None
            The number/shape of samples to generate:
            - If None: returns the fixed value as a float
            - If int: returns a 1-D array filled with the fixed value
            - If tuple of ints: returns an array with that shape filled with
              the fixed value

        Returns
        -------
        Union[float, NDArray[np.float64]]
            The fixed value:
            - A single float when size is None
            - A numpy array filled with the fixed value with shape
              determined by size parameter
        """
        if size is not None:
            return np.full(size, self.value)
        return self.value

class Bernoulli:
    """
    Convenience class for the Bernoulli distribution.
    packages up distribution parameters, seed and random generator.

    The Bernoulli distribution is a special case of the binomial distribution
    where a single trial is conducted

    Use the Bernoulli distribution to sample success or failure.
    """

    def __init__(self, p, random_seed=None):
        """
        Constructor

        Params:
        ------
        p: float
            probability of drawing a 1

        random_seed: int | SeedSequence, optional (default=None)
            A random seed to reproduce samples.  If set to none then a unique
            sample is created.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.p = p

    def sample(self, size=None):
        """
        Generate a sample from the exponential distribution

        Params:
        -------
        size: int, optional (default=None)
            the number of samples to return.  If size=None then a single
            sample is returned.

        Returns:
        -------
        float or np.ndarray (if size >=1)
        """
        return self.rand.binomial(n=1, p=self.p, size=size)

