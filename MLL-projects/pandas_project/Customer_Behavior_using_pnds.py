import pandas as pd

#importing & exploring data
df = pd.read_csv(r"C:\Users\Victor328\OneDrive\Documents\GitHub\MLL-projects\pandas_project\customers.csv")
print(df.head(5))#displays top 5
print(df.describe())#Basic descriptive and statistics for each column (or GroupBy)
print(df.memory_usage)#Prints the memory usage of each column in the DataFrame.

#data cleaning
print(df.dropna())#Drop rows with any column having NA/null data
print(df.fillna(False))#Replace all NA/null data with value

#filtering
Uganda =[(df["country"] == "Uganda") & (df["age"] < 25)]
print(Uganda)

#aggregation#Total spend per customer
total_spend = df.groupby("customer_id")["purchase_amount"].sum().reset_index()
print(total_spend)

#data handling by timestamp
#Days since last purchase 
df ["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"])
df["days_since_last"] = (pd.Timestamp.today() - df["last_purchase_date"]).dt.days
print(df["last_purchase_date"])
print(df["days_since_last"])

#Value Counts(Most Popular Categories)
#Most popular product category
populer = df["product_category"].value_counts().head()
print(populer)

#Value Counts(least Popular Categories)
#least populer product category
least_populer = df["product_category"].value_counts().tail(1) 
least_populer = df["product_category"].value_counts().idxmin() 
print(least_populer)

#ranking
#top 5 customer by spending
top_10_spenders = total_spend.nlargest(10, "purchase_amount")
bottom_10_spenders = total_spend.nsmallest(10, "purchase_amount")
print(bottom_10_spenders)

#transformation(create an age gruop column)
df["age_group"] = df["age"].apply(lambda age: "youth" if age < 30 else "Adult" if age < 50 else "senior")
print(df["age_group"].head(20))

#sorting(Sort by Purchase Amount)
sorted_df = df.sort_values(by="purchase_amount", ascending=False)#from top to down
sorted_df  = df.sort_values(by = "purchase_amount", ascending=True)#from down to top
sorted_age = df.sort_values(by = "age", ascending=False)
print(sorted_age)

#pivot table(Spend by Country and Category)
pivot = df.pivot_table(values="purchase_amount", index="country", columns="product_category", aggfunc="sum", fill_value=0)
print(pivot)#tell the total amount a certian country bought specific product category

#Column Operations(Rename, Drop, Reorder)
df.rename(columns={"gender": "sex"}, inplace=True)#renaming column
df.drop(columns={"join_date"}, inplace=True)#dropping column
df[["customer_id", "age", "sex", "country"]]#reordering
print(df)

#Merge/Join(Add Product Info from Another File)
products = pd.read_csv(r"C:\Users\Victor328\OneDrive\Documents\GitHub\MLL-projects\pandas_project\products.csv")
merged_df = df.merge(products, on='product_category', how='left')
print(merged_df)