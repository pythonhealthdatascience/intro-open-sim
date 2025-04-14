import numpy as np
import pandas as pd
from typing import Protocol, Optional, Union, runtime_checkable
from numpy.random import SeedSequence

# Constants
# default resources
N_OPERATORS = 13
N_NURSES = 10

# default mean inter-arrival time (exp)
MEAN_IAT = 60 / 100

## default service time parameters (triangular)
CALL_LOW = 5.0
CALL_MODE = 7.0
CALL_HIGH = 10.0

# nurse uniform distribution parameters
NURSE_CALL_LOW = 10.0
NURSE_CALL_HIGH = 20.0

# probability of a callback (parameter of Bernoulli)
CHANCE_CALLBACK = 0.4

# sampling settings - we now need 4 streams
N_STREAMS = 4
DEFAULT_RND_SET = 0

# Boolean switch to simulation results as the model runs
TRACE = False

# run variables
RESULTS_COLLECTION_PERIOD = 1000
WARM_UP_PERIOD = 0

# DISTRIBUTION CLASSES


@runtime_checkable
class Distribution(Protocol):
    def sample(self, size: Optional[int] = None) -> Union[float, np.ndarray]:
        """Generate random samples from this distribution.
        
        Parameters
        ----------
        size : Optional[int], default=None
            If None, return a single sample.
            If int, return that many samples in a 1D array.
                 
        Returns
        -------
        Union[float, np.ndarray]
            A single sample (if size is None) or array of samples
        """
        pass


class Bernoulli:
    """
    Convenience class for the Bernoulli distribution.
    Packages up distribution parameters, seed and random generator.

    The Bernoulli distribution is a special case of the binomial distribution
    where a single trial is conducted.

    Use the Bernoulli distribution to sample success or failure.
    """

    def __init__(self, p: float, random_seed: Optional[Union[int, SeedSequence]] = None):
        """
        Constructor

        Parameters
        ----------
        p : float
            Probability of drawing a 1
            
        random_seed : Optional[Union[int, SeedSequence]], default=None
            A random seed to reproduce samples. If set to None then a unique
            sample is created.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.p = p

    def sample(self, size: Optional[int] = None) -> Union[float, np.ndarray]:
        """
        Generate a sample from the Bernoulli distribution.

        Parameters
        ----------
        size : Optional[int], default=None
            The number of samples to return. If size=None then a single
            sample is returned.

        Returns
        -------
        Union[float, np.ndarray]
            Either a single sample (if size is None) or an array of samples
        """
        return self.rand.binomial(n=1, p=self.p, size=size)


class Uniform:
    """
    Convenience class for the Uniform distribution.
    Packages up distribution parameters, seed and random generator.
    """

    def __init__(self, low: float, high: float, random_seed: Optional[Union[int, SeedSequence]] = None):
        """
        Constructor

        Parameters
        ----------
        low : float
            Lower range of the uniform
        
        high : float
            Upper range of the uniform
        
        random_seed : Optional[Union[int, SeedSequence]], default=None
            A random seed to reproduce samples. If set to None then a unique
            sample is created.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.low = low
        self.high = high

    def sample(self, size: Optional[int] = None) -> Union[float, np.ndarray]:
        """
        Generate a sample from the uniform distribution

        Parameters
        ----------
        size : Optional[int], default=None
            The number of samples to return. If size=None then a single
            sample is returned.

        Returns
        -------
        Union[float, np.ndarray]
            Either a single sample (if size is None) or an array of samples
        """
        return self.rand.uniform(low=self.low, high=self.high, size=size)

class Triangular:
    """
    Convenience class for the triangular distribution.
    Packages up distribution parameters, seed and random generator.
    """

    def __init__(self, low: float, mode: float, high: float, 
                 random_seed: Optional[Union[int, SeedSequence]] = None):
        """
        Constructor. Accepts and stores parameters of the triangular dist
        and a random seed.

        Parameters
        ----------
        low : float
            The smallest values that can be sampled
        
        mode : float
            The most frequently sampled value
        
        high : float
            The highest value that can be sampled
        
        random_seed : Optional[Union[int, SeedSequence]], default=None
            Used with params to create a series of repeatable samples.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.low = low
        self.high = high
        self.mode = mode

    def sample(self, size: Optional[int] = None) -> Union[float, np.ndarray]:
        """
        Generate one or more samples from the triangular distribution

        Parameters
        ----------
        size : Optional[int], default=None
            The number of samples to return. If size=None then a single
            sample is returned.

        Returns
        -------
        Union[float, np.ndarray]
            Either a single sample (if size is None) or an array of samples
        """
        return self.rand.triangular(self.low, self.mode, self.high, size=size)

class Exponential:
    """
    Convenience class for the exponential distribution.
    Packages up distribution parameters, seed and random generator.
    """

    def __init__(self, mean: float, random_seed: Optional[Union[int, SeedSequence]] = None):
        """
        Constructor

        Parameters
        ----------
        mean : float
            The mean of the exponential distribution
        
        random_seed : Optional[Union[int, SeedSequence]], default=None
            A random seed to reproduce samples. If set to None then a unique
            sample is created.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.mean = mean

    def sample(self, size: Optional[int] = None) -> Union[float, np.ndarray]:
        """
        Generate a sample from the exponential distribution

        Parameters
        ----------
        size : Optional[int], default=None
            The number of samples to return. If size=None then a single
            sample is returned.

        Returns
        -------
        Union[float, np.ndarray]
            Either a single sample (if size is None) or an array of samples
        """
        return self.rand.exponential(self.mean, size=size)


# Experiment class

class Experiment:
    """
    Encapsulates the concept of an experiment 🧪 with the urgent care
    call centre simulation model.

    An Experiment:
    1. Contains a list of parameters that can be left as defaults or varied
    2. Provides a place for the experimentor to record results of a run
    3. Controls the set & streams of psuedo random numbers used in a run.

    """

    def __init__(
        self,
        random_number_set=DEFAULT_RND_SET,
        n_streams=N_STREAMS,
        n_operators=N_OPERATORS,
        mean_iat=MEAN_IAT,
        call_low=CALL_LOW,
        call_mode=CALL_MODE,
        call_high=CALL_HIGH,
        n_nurses=N_NURSES,
        chance_callback=CHANCE_CALLBACK,
        nurse_call_low=NURSE_CALL_LOW,
        nurse_call_high=NURSE_CALL_HIGH,
    ):
        """
        The init method sets up our defaults.
        """
        # sampling
        self.random_number_set = random_number_set
        self.n_streams = n_streams

        # store parameters for the run of the model
        self.n_operators = n_operators
        self.mean_iat = mean_iat
        self.call_low = call_low
        self.call_mode = call_mode
        self.call_high = call_high

        # resources: we must init resources after an Environment is created.
        # But we will store a placeholder for transparency
        self.operators = None

        # nurse parameters
        self.n_nurses = n_nurses
        self.chance_callback = chance_callback
        self.nurse_call_low = nurse_call_low
        self.nurse_call_high = nurse_call_high

        # nurse resources placeholder
        self.nurses = None

        # initialise results to zero
        self.init_results_variables()

        # initialise sampling objects
        self.init_sampling()

    def set_random_no_set(self, random_number_set):
        """
        Controls the random sampling
        Parameters:
        ----------
        random_number_set: int
            Used to control the set of pseudo random numbers used by
            the distributions in the simulation.
        """
        self.random_number_set = random_number_set
        self.init_sampling()

    def init_sampling(self):
        """
        Create the distributions used by the model and initialise
        the random seeds of each.
        """
        # produce n non-overlapping streams
        seed_sequence = np.random.SeedSequence(self.random_number_set)
        self.seeds = seed_sequence.spawn(self.n_streams)

        # create distributions

        # call inter-arrival times
        self.arrival_dist = Exponential(
            self.mean_iat, random_seed=self.seeds[0]
        )

        # duration of call triage
        self.call_dist = Triangular(
            self.call_low,
            self.call_mode,
            self.call_high,
            random_seed=self.seeds[1],
        )

        # create the callback and nurse consultation distributions
        self.callback_dist = Bernoulli(
            self.chance_callback, random_seed=self.seeds[2]
        )

        self.nurse_dist = Uniform(
            self.nurse_call_low,
            self.nurse_call_high,
            random_seed=self.seeds[3],
        )

    def init_results_variables(self):
        """
        Initialise all of the experiment variables used in results
        collection.  This method is called at the start of each run
        of the model
        """
        # variable used to store results of experiment
        self.results = {}
        self.results["waiting_times"] = []

        # total operator usage time for utilisation calculation.
        self.results["total_call_duration"] = 0.0

        # nurse sub process results collection
        self.results["nurse_waiting_times"] = []
        self.results["total_nurse_call_duration"] = 0.0

def trace(msg):
    """
    Turing printing of events on and off.

    Params:
    -------
    msg: str
        string to print to screen.
    """
    if TRACE:
        print(msg)

