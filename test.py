import csv
import dill
import numpy
from datetime import datetime
from collections import defaultdict

# Filename Variables:
input_csv_filename = 'orders.csv'
output_csv_filename = 'prediction-' + input_csv_filename
model_filename = 'model.dill'

# Maps for processing item 1.
user_order_to_num_items = defaultdict(lambda: 0)
user_to_max_num_items = defaultdict(lambda: 0)

# Maps for processing item 2.
user_order_to_revenue = defaultdict(lambda: 0.0)
user_to_max_revenue = defaultdict(lambda: 0.0)

# Map for processing item 3.
user_to_total_revenue = defaultdict(lambda: 0.0)

# Map for processing item 4.
user_to_orders = defaultdict(lambda: set())

# Map and final date for processing item 5.
user_to_last_order = defaultdict(lambda: datetime.min)
final_date = datetime.strptime("2017-10-17", '%Y-%m-%d')

# Map for processing item 6.
user_to_longest_interval = defaultdict(lambda: 0)

with open(input_csv_filename, newline='') as csvfile:
    orders_reader = csv.reader(csvfile, delimiter=',')
    next(orders_reader) # skipping header
    
    for row in orders_reader:
        # Processing item 1.
        try:
            user_order_to_num_items[(row[0], row[1])] += int(row[3])
        except ValueError:
            continue
        if user_to_max_num_items[row[0]] < user_order_to_num_items[(row[0], row[1])]:
            user_to_max_num_items[row[0]] = user_order_to_num_items[(row[0], row[1])]

        # Processing item 2.
        try:
            user_order_to_revenue[(row[0], row[1])] += float(row[4])
        except ValueError:
            print(row[4] + " is not a float.")
            continue
        if user_to_max_revenue[row[0]] < user_order_to_revenue[(row[0], row[1])]:
            user_to_max_revenue[row[0]] = user_order_to_revenue[(row[0], row[1])]        


        # Processing item 3.
        user_to_total_revenue[row[0]] += float(row[4])

        # Processing item 4.
        user_to_orders[row[0]].add(row[1])

        # Processing item 6.
        d = datetime.strptime(row[5], '%Y-%m-%d')

        if user_to_last_order[row[0]] > datetime.min:
            td = d - user_to_last_order[row[0]]
            days_diff = td.days
            
            if user_to_longest_interval[row[0]] < days_diff:
                user_to_longest_interval[row[0]] = days_diff
        else:
            user_to_longest_interval[row[0]] = 0

        if user_to_last_order[row[0]] <= d:
            user_to_last_order[row[0]] = d
        else:
            print("is not in order ", user_to_last_order[row[0]], d)

avg_longest_interval = 0
user_count = 0
for user, interval in user_to_longest_interval.items():
    if interval > 0:
        user_count += 1
        avg_longest_interval += interval
        
if user_count > 0:
    avg_longest_interval = avg_longest_interval/user_count
else:
    avg_longest_interval = 0

user_to_days_since_last_order = {}
            
for user, last_order in user_to_last_order.items():
    user_to_days_since_last_order[user] = final_date - last_order
    user_to_days_since_last_order[user] = user_to_days_since_last_order[user].days

for user, interval in user_to_longest_interval.items():
    if len(user_to_orders[user]) == 1:
        user_to_longest_interval[user] = avg_longest_interval + user_to_days_since_last_order[user]

rows = []
    
for user, max_num_items in user_to_max_num_items.items():
    row = []
    row.append(max_num_items)
    row.append(user_to_max_revenue[user])
    row.append(user_to_total_revenue[user])
    row.append(len(user_to_orders[user]))
    row.append(user_to_days_since_last_order[user])
    row.append(user_to_longest_interval[user])
#    print(user, row)
    rows.append(row)
    
#z = []
#with open(model_filename, 'rb') as model_file:
#    m = dill.load(model_file)
#    y = numpy.array(rows)
#    z = m.predict(y)
    
#with open(output_csv_filename, 'w') as prediction_file:
#    prediction_writer = csv.writer(prediction_file, delimiter=',')
#    prediction_writer.writerow(['customer_id', 'predicted_clv'])
    
#    for index, key in enumerate(user_to_max_num_items):
#        x = key
#        y = z[index]

#        prediction_writer.writerow([x, y])

