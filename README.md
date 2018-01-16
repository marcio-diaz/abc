# Test

Running `python3.6 predict.py` creates a file `predictions.csv` and a file `predictions.db` with the predictions for the orders in `orders.csv`.
After running the Flask app using `python3.6 api.py` you can get the CLV at `http://127.0.0.1:5000/`.
Tests can be run using `python3.6 tests.py`.

I was using just plain python to process the orders but it was very slow. Then I started using Pandas and the time to process the orders was reduced like by half or more. I think is still possible to improve the performance of `predict.py` but I don't have more time to keep learning Pandas. Also to improve performance I could make it parallel (or distributed). Other option that I was considering was to use Dask or Spark.

Looks like it is necessary to use the version 3.6.X of Python, when I started I was using the version 3.5.X and executing the model in `model.dill` was given me `Segmentation fault`.

I'm not sure if my interpretation of the calculation of the intervals is correct when there is only one order. Also I'm removing the rows with NA values. In any case I think we can talk about this if there is a next step of the interview.