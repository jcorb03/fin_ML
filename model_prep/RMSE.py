import numpy as np

def RMSE(true: list[float] , pred: list[float]):
    sum = 0

    if len(true) != len(pred):
        raise ValueError("not equal lengths")

    for i in range(len(true)):
        sum += (true[i]-pred[i])**2

    return np.sqrt(sum/len(true))
    