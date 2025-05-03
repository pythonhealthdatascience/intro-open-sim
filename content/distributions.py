import numpy as np
from typing import Optional, Union, Tuple
from numpy.random import SeedSequence
from numpy.typing import NDArray
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