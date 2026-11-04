import numpy as np
import pandas as pd

#Method answers: “If I entered a trade at this point, how would it end under these exit rules?”

#For every hypothetical entry, set three barriers:
#Take profit	Exit if the price rises 5%
#Stop loss	Exit if the price falls 3%
#Time limit	Exit after 20 trading days if neither price barrier is reached

def triple_barrier(
        close:pd.Series,
        take_profit:float=0.05,
        stop_loss:float=0.03,
        max_days:int=20
) -> pd.DataFrame:
    """
    Triple barrier method for labeling financial time series data.

    Parameters
    ----------
    close : pd.Series
        Series of closing prices.
    take_profit : float, optional
        Take profit threshold (default is 0.05 for 5%).
    stop_loss : float, optional
        Stop loss threshold (default is 0.03 for 3%).
    max_days : int, optional
        Maximum number of days to hold the position (default is 20).

    Returns
    -------
    pd.DataFrame
        DataFrame containing the entry index, exit index, and exit type.
    """
    
    # Initialize a list to store the results
    results = []

    # Iterate over each entry point in the closing prices
    for entry_index in range(len(close) - max_days):
        entry_price = close.iloc[entry_index]
        
        # Calculate the take profit and stop loss levels
        take_profit_level = entry_price * (1 + take_profit)
        stop_loss_level = entry_price * (1 - stop_loss)
        
        # Initialize exit variables
        exit_index = None
        exit_type = None
        
        # Check the next max_days for exit conditions
        for day in range(1, max_days + 1):
            
            current_price = close.iloc[entry_index + day]
            
            if current_price >= take_profit_level:
                exit_index = entry_index + day
                exit_type = 'take_profit'
                break
            elif current_price <= stop_loss_level:
                exit_index = entry_index + max_days
                exit_type = 'stop_loss'
                break
        
        # If no exit was found within max_days, set the exit to max_days later
        if exit_index is None:
            exit_index = min(entry_index + max_days, len(close) - 1)
            exit_type = 'time_limit'

        exit_price = close.iloc[exit_index]

        # Append the result for this entry point
        results.append({
            'entry_index': entry_index,
            'exit_index': exit_index,
            'exit_type': exit_type,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'return': (exit_price - entry_price) / entry_price,
            'holding_period': exit_index - entry_index
        })
    
    return pd.DataFrame(results)