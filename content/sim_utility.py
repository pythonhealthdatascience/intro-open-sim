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
