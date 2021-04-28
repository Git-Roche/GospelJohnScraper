
from os import path
from pickle import load, dump
import pandas as pd
from time import sleep

def get_data(function, fpath, get_new = False, sleep_time = None, **kwargs):

    """
    Get data from api as dictionary using function.
    kwargs get sent to function.
    save result to fpath.

    If result already exists at fpath, then load fpath pickle data instead.

    ### Params

    * function : function that returns the data
    * fpath : where to save the pickle of the data
    * get_new : if false will load the pickle data if it exists
    * sleep_time : pause for x seconds
    * **kwargs : passed to function

    ### Returns

    function(**kwargs)

    ### Example:

    >>> import requests
    >>> resp = get_data(
    >>>     requests.get,
    >>>     fpath,
    >>>     url = myurl
    >>> )
    """
        
    if not path.exists(fpath) or get_new:
        print('getting new {}'.format(fpath))
        response = function(**kwargs)

        #stay below 3 requests per second limit on coinbase pro
        if sleep_time:
            sleep(sleep_time)

        with open(fpath, 'wb') as f:
            dump(response, f)
    else:
        print('loading existing {}'.format(fpath))
        
        with open(fpath, 'rb') as f:
            response = load(f)

    # df = pd.DataFrame.from_dict(response)

    return response


def dict_list_to_df(dict_list) -> pd.DataFrame:
    """
    Takes in a list of dictionaries and returns a DataFrame.
    Fills missing keys with None as values.

    ### Params

    * dict_list : list of dictionaries, key value pairs.

    ### Example

    >>> data = [
    >>>     {
    >>>         'k1' : 1,
    >>>         'k2' : 2
    >>>     },
    >>>     {
    >>>         'k1' : 3
    >>>     }
    >>> ]
    >>> df = dict_list_to_df(data)
    
    """
    
    keys = []
    for a in dict_list:
        for k in a:
            if not k in keys:
                keys.append(k)
    account_dict = {}
    for k in keys:
        account_dict[k] = []
    for a in dict_list:
        for k in keys:
            if k in a:
                account_dict[k].append(a[k])
            else:
                account_dict[k].append(None)

    df = pd.DataFrame(account_dict)

    return df