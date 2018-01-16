import math
import unittest
import pandas as pd
from predict import read_csv_to_dataframe, compute_final_dataframe

class TestCase01(unittest.TestCase):

    def setUp(self):
        input_dataframe = read_csv_to_dataframe('test01.csv')
        self.df = compute_final_dataframe(input_dataframe)
        
    def test_max_num_items(self):
        col = 'max_num_items'
        self.assertEqual(self.df[col][0], 5)
        self.assertEqual(self.df[col][1], 1)
        self.assertEqual(self.df[col][2], 10)        
        
    def test_max_revenue(self):
        col = 'max_revenue_in_order'
        self.assertEqual(self.df[col][0], 3)
        self.assertEqual(self.df[col][1], 1)
        self.assertEqual(self.df[col][2], 6)        

    def test_total_revenue(self):
        col = 'total_revenue'
        self.assertEqual(self.df[col][0], 9)
        self.assertEqual(self.df[col][1], 1)
        self.assertEqual(self.df[col][2], 6)                

    def test_num_orders(self):
        col = 'num_of_orders'
        self.assertEqual(self.df[col][0], 3)
        self.assertEqual(self.df[col][1], 1)
        self.assertEqual(self.df[col][2], 1)        

    def test_days_since_last_order(self):
        col = 'days_since_last_order'
        self.assertEqual(self.df[col][0], 44)
        self.assertEqual(self.df[col][1], 46)
        self.assertEqual(self.df[col][2], 44)        

    def test_interval(self):
        col = 'interval'
        self.assertEqual(self.df[col][0], 1)
        self.assertEqual(self.df[col][1], 46.5)
        self.assertEqual(self.df[col][2], 0)        


class TestCase02(unittest.TestCase):

    def setUp(self):
        input_dataframe = read_csv_to_dataframe('test02.csv')
        self.df = compute_final_dataframe(input_dataframe)
        
    def test_max_num_items(self):
        col = 'max_num_items'
        self.assertEqual(self.df[col][0], 10)
        self.assertEqual(self.df[col][1], 10)        
        
    def test_max_revenue(self):
        col = 'max_revenue_in_order'
        self.assertEqual(self.df[col][0], 24)
        self.assertEqual(self.df[col][1], 24)        

    def test_total_revenue(self):
        col = 'total_revenue'
        self.assertEqual(self.df[col][0], 31)
        self.assertEqual(self.df[col][1], 31)        

    def test_num_orders(self):
        col = 'num_of_orders'
        self.assertEqual(self.df[col][0], 2)
        self.assertEqual(self.df[col][1], 2)        

    def test_days_since_last_order(self):
        col = 'days_since_last_order'
        self.assertEqual(self.df[col][0], 46)
        self.assertEqual(self.df[col][1], 46)        

    def test_interval(self):
        col = 'interval'
        self.assertEqual(self.df[col][0], 4383)
        self.assertEqual(self.df[col][1], 4383)


class TestCase03(unittest.TestCase):

    def setUp(self):
        input_dataframe = read_csv_to_dataframe('test03.csv')
        self.df = compute_final_dataframe(input_dataframe)

    def test_max_num_items(self):
        col = 'max_num_items'
        self.assertEqual(self.df[col][0], 1)
        
    def test_max_revenue(self):
        col = 'max_revenue_in_order'
        self.assertEqual(self.df[col][0], 15)

    def test_total_revenue(self):
        col = 'total_revenue'
        self.assertEqual(self.df[col][0], 15)

    def test_num_orders(self):
        col = 'num_of_orders'
        self.assertEqual(self.df[col][0], 1)

    def test_days_since_last_order(self):
        col = 'days_since_last_order'
        self.assertEqual(self.df[col][0], 46)

    def test_interval(self):
        col = 'interval'
        self.assertTrue(math.isnan(self.df[col][0]))
        
class TestCase04(unittest.TestCase):

    def setUp(self):
        input_dataframe = read_csv_to_dataframe('test04.csv')
        self.df = compute_final_dataframe(input_dataframe)

    def test_max_num_items(self):
        col = 'max_num_items'
        self.assertEqual(self.df[col][0], 5)
        self.assertEqual(self.df[col][1], 5)
        self.assertEqual(self.df[col][2], 5)        

    def test_max_revenue(self):
        col = 'max_revenue_in_order'
        self.assertEqual(self.df[col][0], 25)
        self.assertEqual(self.df[col][1], 25)
        self.assertEqual(self.df[col][2], 25)

    def test_total_revenue(self):
        col = 'total_revenue'
        self.assertEqual(self.df[col][0], 40)
        self.assertEqual(self.df[col][1], 40)
        self.assertEqual(self.df[col][2], 25)

    def test_num_orders(self):
        col = 'num_of_orders'
        self.assertEqual(self.df[col][0], 2)
        self.assertEqual(self.df[col][1], 2)
        self.assertEqual(self.df[col][2], 1)

    def test_days_since_last_order(self):
        col = 'days_since_last_order'
        self.assertEqual(self.df[col][0], 42)
        self.assertEqual(self.df[col][1], 44)
        self.assertEqual(self.df[col][2], 44)

    def test_interval(self):
        col = 'interval'
        self.assertEqual(self.df[col][0], 4)
        self.assertEqual(self.df[col][1], 2)
        self.assertEqual(self.df[col][2], 47)        
        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCase01('test_max_num_items'))
    suite.addTest(TestCase01('test_max_revenue'))
    suite.addTest(TestCase01('test_total_revenue'))
    suite.addTest(TestCase01('test_num_orders'))
    suite.addTest(TestCase01('test_days_since_last_order'))
    suite.addTest(TestCase01('test_interval'))
    
    suite.addTest(TestCase02('test_max_num_items'))
    suite.addTest(TestCase02('test_max_revenue'))
    suite.addTest(TestCase02('test_total_revenue'))
    suite.addTest(TestCase02('test_num_orders'))
    suite.addTest(TestCase02('test_days_since_last_order'))
    suite.addTest(TestCase02('test_interval'))        
    
    suite.addTest(TestCase03('test_max_num_items'))
    suite.addTest(TestCase03('test_max_revenue'))
    suite.addTest(TestCase03('test_total_revenue'))
    suite.addTest(TestCase03('test_num_orders'))
    suite.addTest(TestCase03('test_days_since_last_order'))
    suite.addTest(TestCase03('test_interval'))        
    
    suite.addTest(TestCase04('test_max_num_items'))
    suite.addTest(TestCase04('test_max_revenue'))
    suite.addTest(TestCase04('test_total_revenue'))
    suite.addTest(TestCase04('test_num_orders'))
    suite.addTest(TestCase04('test_days_since_last_order'))
    suite.addTest(TestCase04('test_interval'))    
    
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
