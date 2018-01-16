from functools import reduce
from datetime import datetime
from collections import defaultdict
from sqlalchemy import create_engine
import pandas
import numpy
import dill

# Read input.
def read_csv_to_dataframe(csv_filename):
    data_frame = pandas.read_csv(csv_filename)
    data_frame = data_frame.dropna()
    data_frame['created_at_date'] = pandas.to_datetime(data_frame['created_at_date'])
    data_frame = data_frame.sort_values(['customer_id', 'created_at_date'])

    return data_frame

# Item 1.
def get_max_num_items_dataframe(data_frame):
    customer_to_max_num_items = \
        data_frame.groupby(['customer_id', 'order_id'], as_index=False)['num_items'].sum() \
                    .groupby(['customer_id'], as_index=False)['num_items'].max()
    customer_to_max_num_items.rename(columns={'num_items': 'max_num_items'}, inplace=True)
    
    return customer_to_max_num_items

# Item 2.
def get_max_revenue_dataframe(data_frame):
    customer_to_max_revenue = \
        data_frame.groupby(['customer_id', 'order_id'], as_index=False)['revenue'].sum() \
                  .groupby(['customer_id'], as_index=False)['revenue'].max()
    customer_to_max_revenue.rename(columns={'revenue': 'max_revenue_in_order'}, inplace=True)

    return customer_to_max_revenue

# Item 3.
def get_total_revenue_dataframe(data_frame):
    customer_to_total_revenue = \
        data_frame.groupby(['customer_id'], as_index=False)['revenue'].sum()
    customer_to_total_revenue.rename(columns={'revenue': 'total_revenue'}, inplace=True)    
    return customer_to_total_revenue

# Item 4.
def get_num_orders_dataframe(data_frame):
    customer_to_num_orders = \
        data_frame[['customer_id', 'order_id']].drop_duplicates() \
            .groupby('customer_id', as_index=False)['order_id'].count()
    customer_to_num_orders.rename(columns={'order_id': 'num_of_orders'}, inplace=True)        
    return customer_to_num_orders

# Item 5.
def get_days_since_last_order_dataframe(data_frame):
    customer_to_last_date = data_frame.groupby('customer_id', as_index=False)['created_at_date']\
                                      .max().rename(columns={'created_at_date':'last_date'})
    final_date = datetime.strptime("2017-10-17", '%Y-%m-%d')
    customer_to_last_date['last_date'] = (final_date - customer_to_last_date['last_date']).dt.days
    customer_to_days_since_last_order = customer_to_last_date.rename(columns={'last_date':'days_since_last_order'})
    
    return customer_to_days_since_last_order

# Item 6.
def get_interval_dataframe(data_frame, customer_to_days_since_last_order_df):
    cd = data_frame[['customer_id', 'created_at_date']]
    cds = cd.shift(-1).rename(columns={'customer_id': 'next_customer_id',
                                       'created_at_date': 'next_created_at_date'})
    cd = cd.join(cds)
    day = numpy.timedelta64(1, 'D')
    cd['interval'] = ((cd['next_created_at_date']-cd['created_at_date'])/day).astype(float)
    cd.loc[cd['customer_id'] != cd['next_customer_id'], 'interval'] = numpy.NaN
    customer_to_interval = cd[['customer_id', 'interval']].groupby('customer_id').max()
    avg_interval = customer_to_interval['interval'].mean()
    dt = customer_to_days_since_last_order_df.join(customer_to_interval, on='customer_id')
    dt.loc[dt['interval'].isnull(), 'interval'] = dt['days_since_last_order'].apply(lambda days: days+avg_interval)
    customer_to_interval = dt.drop(['days_since_last_order'], axis=1)
    
    return customer_to_interval

def compute_final_dataframe(data_frame):
    max_num_items = get_max_num_items_dataframe(data_frame)
    max_revenue = get_max_revenue_dataframe(data_frame)
    total_revenue = get_total_revenue_dataframe(data_frame)
    num_orders = get_num_orders_dataframe(data_frame)
    days_since_last_order = get_days_since_last_order_dataframe(data_frame)
    interval = get_interval_dataframe(data_frame, days_since_last_order)
    dfs = [max_num_items, max_revenue, total_revenue,
           num_orders, days_since_last_order, interval]

    final_dataframe = reduce(lambda left, right:
                      pandas.merge(left, right, on='customer_id'), dfs)
    
    return final_dataframe

def compute_predictions(model_filename, input_dataframe):
    model_input = input_dataframe.drop(['customer_id'], axis=1).as_matrix()
    with open(model_filename, 'rb') as model_file:
        m = dill.load(model_file)
    predictions = m.predict(model_input)
    
    return predictions


if __name__ == '__main__':
    input_dataframe = read_csv_to_dataframe('orders.csv')
    final_dataframe = compute_final_dataframe(input_dataframe)
    predictions = compute_predictions('model.dill', final_dataframe)
    customers = final_dataframe['customer_id'].as_matrix()
    output = pandas.DataFrame({'customer_id': customers, 'predicted_clv': predictions})
    output.to_csv('predictions.csv', sep=',', index=False)
    disk_engine = create_engine('sqlite:///predictions.db')
    output.to_sql('predictions', disk_engine, if_exists='replace')
