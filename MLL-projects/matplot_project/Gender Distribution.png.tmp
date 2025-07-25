import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv(r"C:\Users\Victor328\OneDrive\Documents\GitHub\MLL-projects\matplot_project\customers.csv")

df = pd.DataFrame(data)
print(df)

#Line Plot – Age vs. Purchase
df_sorted = df.sort_values('age')
plt.plot(df_sorted["age"], df_sorted["purchase_amount"], color="blue", marker="o")
plt.title("Age vs. Purchase_Amount")
plt.xlabel("Customer Age")
plt.ylabel("Purchase_Amount (ksh)")
plt.grid(True)
plt.show()

#Bar Chart – Purchases by Country
country_sale = df.groupby("country")["purchase_amount"].sum()
plt.bar(country_sale.index, country_sale.values.tolist(), color="green")
plt.title("Total_Purchases by Country")
plt.xlabel("Country")
plt.ylabel("Total_Purcahse")
plt.xticks(rotation=45)
plt.show()

#Pie Chart – Gender Distribution
gender_counts = df["gender"].value_counts()
plt.pie(gender_counts, labels=gender_counts.tolist(), autopct="%1.1f%%", colors=["skyblue", "lightcoral"])
plt.title("Gender Distribution")
plt.axis("equal")
plt.show()

#Histogram – Age Distribution
plt.hist(df["age"], bins=5, color="purple", edgecolor="black")
plt.title("Age_Distribution")
plt.xlabel("age")
plt.ylabel("Number_of_customer")
plt.show()

# Box Plot – Summary of distribution (median, IQR, outliers)
plt.boxplot(df['purchase_amount'])
plt.title('Boxplot of Purchase Amount')
plt.ylabel('Purchase Amount (Ksh)')
plt.grid(True)
plt.show()


# Just an example - assumes these columns exist
plt.scatter(
    df['age'],
    df['purchase_amount'],
    #s=df['visits'] * 10,         # Bubble size
    c=df['gender'].replace({'Male': 'blue', 'Female': 'red'}),  # Color by gender
    alpha=0.6
)
plt.title('Age vs Purchase Amount (Colored by Gender, Sized by Visits)')
plt.xlabel('Age')
plt.ylabel('Purchase Amount')
plt.grid(True)
plt.show()

