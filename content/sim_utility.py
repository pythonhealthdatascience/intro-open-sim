import numpy as np
from typing import Optional


# Internal module state for tracing (default to True)
_trace_state = {"enabled": True}

# ----------------------------------------------------------------------------
# HELPER FUNCTIONS & DISTRIBUTIONS
# ----------------------------------------------------------------------------

def set_trace(state: bool):
    '''
    Toggles the simulation trace output on or off.
    
    Usage:
    ------
    Call this before running your simulation to enable/disable printing.
    
    >>> set_trace(True)
    
    Params:
    -------
    state: bool
        True to enable print output, False to disable.
    '''
    _trace_state["enabled"] = state
    print(f"Simulation tracing set to: {state}")

def trace(msg):
    '''
    Prints an event message if tracing is enabled.
    
    Params:
    -------
    msg: str
        string to print to screen.
    '''
    if _trace_state["enabled"]:
        print(msg)

def spawn_seeds(n_streams: int, main_seed: Optional[int] = None) -> list[np.random.SeedSequence]:
    """
    Taken from `sim-tools`
    
    Generate multiple statistically independent random seeds.

    This function creates a set of SeedSequence objects that are guaranteed
    to produce independent streams of random numbers. This is crucial for
    ensuring that multiple random number generators don't produce correlated
    outputs, which could bias simulation results.

    Parameters
    ----------
    n_streams : int
        The number of independent seed sequences to generate.
        Must be a positive integer.

    main_seed : Optional[int], default=None
        Master seed that determines all generated sequences.
        If None, a random entropy source is used, making results
        non-reproducible across runs. Providing a value enables
        reproducible sequences.

    Returns
    -------
    List[np.random.SeedSequence]
        A list of n_streams SeedSequence objects that can be used
        to initialize random number generators with independent streams.

    Notes
    -----
    This approach is preferred over manually creating seeds because
    it uses NumPy's entropy pool management to guarantee statistical
    independence between streams, avoiding subtle correlations that
    might occur with manually chosen seeds.

    Examples
    --------
    >>> seeds = spawn_seeds(3, main_seed=12345)
    >>> rng1 = np.random.default_rng(seeds[0])
    >>> rng2 = np.random.default_rng(seeds[1])
    >>> rng3 = np.random.default_rng(seeds[2])
    """
    seed_sequence = np.random.SeedSequence(main_seed)
    seeds = seed_sequence.spawn(n_streams)
    return seeds
