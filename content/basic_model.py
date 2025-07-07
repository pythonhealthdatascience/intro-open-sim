"""
Call Centre Simulation Model

A discrete event simulation model of a call centre using SimPy.
Contains experiment management, distribution classes, and simulation logic.

To be used with 07a_experiments_exercise.ipynb

Author: Tom Monks
"""

import numpy as np
import pandas as pd
import simpy
import itertools

# =============================================================================
# CONSTANTS AND DEFAULT VALUES
# =============================================================================

# Default resources
N_OPERATORS = 13

# Default mean inter-arrival time (exp)
MEAN_IAT = 60 / 100

# Default service time parameters (triangular)
CALL_LOW = 5.0
CALL_MODE = 7.0
CALL_HIGH = 10.0

# Sampling settings
N_STREAMS = 2
DEFAULT_RND_SET = 0

# Boolean switch to display simulation results as the model runs
TRACE = False

# Run variables
RESULTS_COLLECTION_PERIOD = 1000


# =============================================================================
# DISTRIBUTION CLASSES
# =============================================================================

class Triangular:
    """
    Convenience class for the triangular distribution.
    Packages up distribution parameters, seed and random generator.
    """

    def __init__(self, low, mode, high, random_seed=None):
        """
        Constructor. Accepts and stores parameters of the triangular dist
        and a random seed.

        Params:
        ------
        low: float
            The smallest values that can be sampled

        mode: float
            The most frequently sample value

        high: float
            The highest value that can be sampled

        random_seed: int | SeedSequence, optional (default=None)
            Used with params to create a series of repeatable samples.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.low = low
        self.high = high
        self.mode = mode

    def sample(self, size=None):
        """
        Generate one or more samples from the triangular distribution

        Params:
        --------
        size: int
            the number of samples to return. If size=None then a single
            sample is returned.

        Returns:
        -------
        float or np.ndarray (if size >=1)
        """
        return self.rand.triangular(self.low, self.mode, self.high, size=size)


class Exponential:
    """
    Convenience class for the exponential distribution.
    Packages up distribution parameters, seed and random generator.
    """

    def __init__(self, mean, random_seed=None):
        """
        Constructor

        Params:
        ------
        mean: float
            The mean of the exponential distribution

        random_seed: int| SeedSequence, optional (default=None)
            A random seed to reproduce samples. If set to none then a unique
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
            the number of samples to return. If size=None then a single
            sample is returned.

        Returns:
        -------
        float or np.ndarray (if size >=1)
        """
        return self.rand.exponential(self.mean, size=size)


# =============================================================================
# EXPERIMENT CLASS
# =============================================================================

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
        n_operators=N_OPERATORS,
        mean_iat=MEAN_IAT,
        call_low=CALL_LOW,
        call_mode=CALL_MODE,
        call_high=CALL_HIGH,
        n_streams=N_STREAMS,
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

    def init_results_variables(self):
        """
        Initialise all of the experiment variables used in results
        collection. This method is called at the start of each run
        of the model
        """
        # variable used to store results of experiment
        self.results = {}
        self.results["waiting_times"] = []

        # total operator usage time for utilisation calculation.
        self.results["total_call_duration"] = 0.0


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def trace(msg):
    """
    Turning printing of events on and off.

    Params:
    -------
    msg: str
        string to print to screen.
    """
    if TRACE:
        print(msg)


# =============================================================================
# MODEL LOGIC
# =============================================================================

def service(identifier, env, args):
    """
    Simulates the service process for a call operator

    1. request and wait for a call operator
    2. phone triage (triangular)
    3. exit system

    Params:
    ------
    identifier: int
        A unique identifer for this caller

    env: simpy.Environment
        The current environent the simulation is running in
        We use this to pause and restart the process after a delay.

    args: Experiment
        The settings and input parameters for the current experiment
    """

    # record the time that call entered the queue
    start_wait = env.now

    # request an operator - stored in the Experiment
    with args.operators.request() as req:
        yield req

        # record the waiting time for call to be answered
        waiting_time = env.now - start_wait

        # store the results for an experiment
        args.results["waiting_times"].append(waiting_time)

        trace(f"operator answered call {identifier} at {env.now:.3f}")

        # the sample distribution is defined by the experiment
        call_duration = args.call_dist.sample()

        # schedule process to begin again after call_duration
        yield env.timeout(call_duration)

        # update the total call_duration
        args.results["total_call_duration"] += call_duration

        # print out information for patient.
        trace(
            f"call {identifier} ended {env.now:.3f}; "
            + f"waiting time was {waiting_time:.3f}"
        )


def arrivals_generator(env, args):
    """
    IAT is exponentially distributed

    Parameters:
    ------
    env: simpy.Environment
        The simpy environment for the simulation

    args: Experiment
        The settings and input parameters for the simulation.
    """
    # use itertools as it provides an infinite loop
    # with a counter variable that we can use for unique Ids
    for caller_count in itertools.count(start=1):

        # the sample distribution is defined by the experiment
        inter_arrival_time = args.arrival_dist.sample()

        yield env.timeout(inter_arrival_time)

        trace(f"call arrives at: {env.now:.3f}")

        # we pass the experiment to the service function
        env.process(service(caller_count, env, args))


# =============================================================================
# EXPERIMENT EXECUTION FUNCTIONS
# =============================================================================

def single_run(experiment, rep=0, rc_period=RESULTS_COLLECTION_PERIOD):
    """
    Perform a single run of the model and return the results

    Parameters:
    -----------
    experiment: Experiment
        The experiment/paramaters to use with model
    
    rep: int, optional (default=0)
        The replication number for random seed control
        
    rc_period: float, optional (default=RESULTS_COLLECTION_PERIOD)
        Results collection period - how long to run the simulation

    Returns:
    --------
    dict: Dictionary containing the key performance indicators
    """

    # results dictionary. Each KPI is a new entry.
    run_results = {}

    # reset all result collection variables
    experiment.init_results_variables()

    # set random number set to the replication no.
    # this controls sampling for the run.
    experiment.set_random_no_set(rep)

    # environment is (re)created inside single run
    env = simpy.Environment()

    # we create simpy resource here - this has to be after we
    # create the environment object.
    experiment.operators = simpy.Resource(env, capacity=experiment.n_operators)

    # we pass the experiment to the arrivals generator
    env.process(arrivals_generator(env, experiment))
    env.run(until=rc_period)

    # end of run results: calculate mean waiting time
    run_results["01_mean_waiting_time"] = np.mean(
        experiment.results["waiting_times"]
    )

    # end of run results: calculate mean operator utilisation
    run_results["02_operator_util"] = (
        experiment.results["total_call_duration"]
        / (rc_period * experiment.n_operators)
    ) * 100.0

    # return the results from the run of the model
    return run_results


def multiple_replications(
    experiment, rc_period=RESULTS_COLLECTION_PERIOD, n_reps=5
):
    """
    Perform multiple replications of the model.

    Params:
    ------
    experiment: Experiment
        The experiment/paramaters to use with model

    rc_period: float, optional (default=RESULTS_COLLECTION_PERIOD)
        results collection period.
        the number of minutes to run the model to collect results

    n_reps: int, optional (default=5)
        Number of independent replications to run.

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing results from all replications
    """

    # loop over single run to generate results dicts in a python list.
    results = [single_run(experiment, rep, rc_period) for rep in range(n_reps)]

    # format and return results in a dataframe
    df_results = pd.DataFrame(results)
    df_results.index = np.arange(1, len(df_results) + 1)
    df_results.index.name = "rep"
    return df_results


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def set_trace(trace_on=True):
    """
    Convenience function to turn tracing on/off globally.

    Its not ideal to use global variables like this, but
    it is included for simplicity.
    
    Params:
    -------
    trace_on: bool, optional (default=True)
        Whether to turn tracing on or off
    """
    global TRACE
    TRACE = trace_on


def summary_stats(results_df):
    """
    Calculate summary statistics for a results DataFrame
    
    Params:
    -------
    results_df: pandas.DataFrame
        DataFrame from multiple_replications function
        
    Returns:
    --------
    pandas.DataFrame: Summary statistics (mean, std, min, max)
    """
    return results_df.describe()


def compare_experiments(experiments_dict, n_reps=10, rc_period=RESULTS_COLLECTION_PERIOD):
    """
    Compare multiple experiments and return summary results
    
    Params:
    -------
    experiments_dict: dict
        Dictionary where keys are experiment names and values are Experiment objects
    n_reps: int, optional (default=10)
        Number of replications for each experiment
    rc_period: float, optional (default=RESULTS_COLLECTION_PERIOD)
        Results collection period
        
    Returns:
    --------
    pandas.DataFrame: Comparison of mean results across experiments
    """
    comparison_results = {}
    
    for name, experiment in experiments_dict.items():
        results = multiple_replications(experiment, rc_period, n_reps)
        comparison_results[name] = results.mean()
    
    return pd.DataFrame(comparison_results).T


def create_summary_table(results_dict, label_key, label_order):
    """
    Create a summary DataFrame for multiple scenarios or demand levels.

    Parameters:
    -----------
    results_dict: dict
        Dictionary where keys are labels (e.g., scenario or demand level names) and values are
        pandas DataFrames containing replication results with columns '01_mean_waiting_time' and '02_operator_util'.

    label_key: str
        The name of the column for the labels in the summary table (e.g., 'Scenario' or 'Demand_Level').

    label_order: list
        The order of labels to appear in the summary table.

    Returns:
    --------
    pandas.DataFrame
        Summary table with mean and std for waiting time and utilization.
    """
    summary_data = {
        label_key: [],
        'Mean_Waiting_Time': [],
        'Std_Waiting_Time': [],
        'Mean_Utilization': [],
        'Std_Utilization': []
    }

    for label in label_order:
        df = results_dict[label]
        summary_data[label_key].append(label)
        summary_data['Mean_Waiting_Time'].append(df['01_mean_waiting_time'].mean())
        summary_data['Std_Waiting_Time'].append(df['01_mean_waiting_time'].std())
        summary_data['Mean_Utilization'].append(df['02_operator_util'].mean())
        summary_data['Std_Utilization'].append(df['02_operator_util'].std())

    return pd.DataFrame(summary_data)



# =============================================================================
# MODULE INFORMATION
# =============================================================================

__version__ = "1.0.0"
__author__ = "Tom Monks"
__all__ = [
    # Classes
    'Experiment', 'Triangular', 'Exponential',
    # Main functions
    'single_run', 'multiple_replications',
    # Model functions
    'service', 'arrivals_generator',
    # Utility functions
    'trace', 'set_trace', 'summary_stats', 'compare_experiments', "create_summary_table",
    # Constants
    'N_OPERATORS', 'MEAN_IAT', 'CALL_LOW', 'CALL_MODE', 'CALL_HIGH',
    'RESULTS_COLLECTION_PERIOD', 'TRACE'
]
