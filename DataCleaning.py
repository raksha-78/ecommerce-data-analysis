import pandas as pd

#data set loading for data cleaning.

customer=pd.read_csv("../Data Sets/olist_customers_dataset.csv")
location=pd.read_csv("../Data Sets/olist_geolocation_dataset.csv")
orderitems=pd.read_csv("../Data Sets/olist_order_items_dataset.csv")
orderpayment=pd.read_csv("../Data Sets/olist_order_payments_dataset.csv")
orderreviews=pd.read_csv("../Data Sets/olist_order_reviews_dataset.csv")
orders=pd.read_csv("../Data Sets/olist_orders_dataset.csv")
products=pd.read_csv("../Data Sets/olist_products_dataset.csv")
sellers=pd.read_csv("../Data Sets/olist_sellers_dataset.csv")
productcategory=pd.read_csv("../Data Sets/product_category_name_translation.csv")

# Basic data Modeling

#here we are counting total number of rows and column in each dataframe
print(customer.shape)
print(location.shape)
print(orderitems.shape)
print(orderpayment.shape)
print(orderreviews.shape)
print(orders.shape)
print(products.shape)
print(sellers.shape)
print(productcategory.shape)

# Here we are checking all column names

print(customer.columns)
print(location.columns)
print(orderitems.columns)
print(orderpayment.columns)
print(orderreviews.columns)
print(orders.columns)
print(products.columns)
print(productcategory.columns)

# Here were are checking column data types

print(customer.dtypes)
print(location.dtypes)
print(orderitems.dtypes)
print(orderpayment.dtypes)
print(orderreviews.dtypes)
print(orderreviews.dtypes)
print(orders.dtypes)
print(products.dtypes)
print(productcategory.dtypes)

# Here we are checking the quick summery

print(customer.describe(include="all"))
print(location.describe(include="all"))
print(orderitems.describe(include="all"))
print(orderpayment.describe(include="all"))
print(orderreviews.describe(include="all"))
print(orderreviews.describe(include="all"))
print(orders.describe(include="all"))
print(products.describe(include="all"))
print(productcategory.describe(include="all"))

# Here we are checking is there any null values are apeared in dataset

print(customer.isnull().sum())
print(location.isnull().sum())
print(orderitems.isnull().sum())
print(orderpayment.isnull().sum())
print(orderreviews.isnull().sum())
print(orders.isnull().sum())
print(products.isnull().sum())
print(productcategory.isnull().sum())

''' Here we are checking duplicates are there or not we will get duplicated value in location 
that was expected behaviour'''

print(customer.duplicated().sum())
print(location.duplicated().sum())
print(orderitems.duplicated().sum())
print(orderpayment.duplicated().sum())
print(orderreviews.duplicated().sum())
print(orders.duplicated().sum())
print(products.duplicated().sum())
print(productcategory.duplicated().sum())

'''Here we are checking the relarionship between all tables.'''

print("customer table columns")
print(customer.columns)
print("location table columns")
print(location.columns)
print("orderitems table columns")
print(orderitems.columns)
print("orderpayment table coulmns")
print(orderpayment.columns)
print("orderreviews table columns")
print(orderreviews.columns)
print("orders table columns")
print(orders.columns)
print("products table columns")
print(products.columns)
print("productcategory table columns")
print(productcategory.columns)

#***********Table relationship checks start here************

customer["customer_id"].nunique()
orders["customer_id"].nunique()
# Find customer_ids in orders but NOT in customers table
#this is for if orders are more than customer then we have check any customer id was missed or not
missing_customers = set(orders['customer_id']) - set(customer['customer_id'])
print(len(missing_customers))
print(missing_customers)
# View those orphaned order rows
orders[orders['customer_id'].isin(missing_customers)]
# Check dtypes match before comparing — silent bug source
print(customer['customer_id'].dtype, orders['customer_id'].dtype)

orders["order_id"].nunique()
orderitems["order_id"].nunique()
missing_orders=set(orderitems["order_id"])-set(orders["order_id"])
print(len(missing_orders))

products["product_id"].nunique()
orderitems["product_id"].nunique()
missing_products=set(orderitems["product_id"])-set(products["product_id"])
print(len(missing_products))

sellers["seller_id"].nunique()
orderitems["seller_id"].nunique()
missing_items=set(orderitems["seller_id"])-set(sellers["seller_id"])
print(len(missing_items))

orderpayment["order_id"].nunique()
orderreviews["order_id"].nunique()

#here we are validating primary keys are contain null valuees or not
print("customers", customer["customer_id"].duplicated().sum())
print("orders",orders["order_id"].duplicated().sum())
print("Products",products["product_id"].duplicated().sum())
print("sellers",sellers["seller_id"].duplicated().sum())

'''while doing data quaility i have found 774 values are mismatching so i have did below process'''

not_same_orderid=set(orders["order_id"])-set(orderitems["order_id"])
print(len(not_same_orderid))
print(orders[orders["order_id"].isin(not_same_orderid)])
orders[orders["order_id"].isin(not_same_orderid)]["order_status"].value_counts()

not_same_orderid = set(orders["order_id"]) - set(orderitems["order_id"])
unmatched_orders = orders[
    orders["order_id"].isin(not_same_orderid)
]

unmatched_orders.shape

unmatched_orders[
    ~unmatched_orders["order_status"].isin(["unavailable", "canceled"])
][[
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at"
]]

unmatched_orders[
    ~unmatched_orders["order_status"].isin(["unavailable", "canceled"])
].isnull().sum()

#reltionship checling with other tables
orphan_order_items = set(orderitems["order_id"]) - set(orders["order_id"])
print(len(orphan_order_items))

orphan_products = set(orderitems["product_id"]) - set(products["product_id"])
print(len(orphan_products))

orphan_sellers = set(orderitems["seller_id"]) - set(sellers["seller_id"])
print(len(orphan_sellers))

orphan_payments = set(orderpayment["order_id"]) - set(orders["order_id"])
print(len(orphan_payments))

orphan_reviews = set(orderreviews["order_id"]) - set(orders["order_id"])
print(len(orphan_reviews))

#checking the null value and validation

tables={
    "customer":customer,
    "location":location,
    "orderitems":orderitems,
    "orderpayment":orderpayment,
    "orderreviews":orderreviews,
    "orders":orders,
    "products":products,
    "productcategory":productcategory
}

for name,data in tables.items():
    print(f"\n*******{name.upper()}*****")
    print(data.isnull().sum()[data.isnull().sum()>0])
