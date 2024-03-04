import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')


alldata_df = pd.read_csv("alldata_merge.csv")

def create_revenue_state_df(_df):
    revenueplot_df = alldata_df.groupby(by="customer_state").payment_value.sum().reset_index()
    return revenueplot_df

def create_SP_product_df(df):
    SP_products = df[df['customer_state'] == 'SP']
    SP_products = SP_products.groupby(by=["product_category_name_english"]).order_id.nunique().reset_index()
    return SP_products

def create_payment_method_df(df):
    payment_counts = alldata_df.groupby(by="payment_type").agg({
    "customer_id": "nunique",}).sort_values("customer_id", ascending=False)
    return payment_counts

def create_creditcard_usage_df(df):
    payment_type_state = df.groupby(by=["payment_type", "customer_state"])['customer_id'].nunique().reset_index()
    credit_card_data = payment_type_state.loc[payment_type_state["payment_type"] == "credit_card"]
    return credit_card_data



def create_bestselling_df(df):
    product_selling=alldata_df.groupby(by="product_category_name_english").agg({
    "order_id" : "nunique"}).sort_values(by="order_id", ascending=True)
    top10_best_selling = product_selling.groupby(level=0)["order_id"].sum().nlargest(5).index.tolist()
    top10_best_selling = product_selling.loc[top10_best_selling]
    return top10_best_selling

def create_worstselling_df(df):
    product_selling=alldata_df.groupby(by="product_category_name_english").agg({
    "order_id" : "nunique"}).sort_values(by="order_id", ascending=True)
    top10_worst_selling = product_selling.groupby(level=0)["order_id"].sum().nsmallest(5).index.tolist()
    top10_worst_selling = product_selling.loc[top10_worst_selling]
    return top10_worst_selling


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/yulin09/ProyekAkhir_AnalisisData_Dicoding/blob/main/Bright%20Colorful%20Playful%20Funny%20Donuts%20Food%20Circle%20Logo.png?raw=true")

st.header("Analisis Data E-Commerce Dashboard")

revenue_state_df = create_revenue_state_df(alldata_df)
SP_product_df = create_SP_product_df(alldata_df)
payment_method_df = create_payment_method_df(alldata_df)
creditcard_usage_df = create_creditcard_usage_df(alldata_df)
bestselling_df = create_bestselling_df(alldata_df)
worstselling_df = create_worstselling_df(alldata_df)



colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
##plot buat pertanyaan 1 
revenue_state_df = revenue_state_df.sort_values(by="payment_value", ascending=False)
st.subheader("E-commerce Revenue in Every State (2016-2018)")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="customer_state", y="payment_value", data=revenue_state_df, palette=colors, ax=ax)
ax.set_ylabel("Revenue(million)", fontsize=15)
ax.set_xlabel("State", fontsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)
st.pyplot(fig)




# Plotting most popular product
top_5_categories= SP_product_df.sort_values(by="order_id", ascending=False)
# Plotting top 5 most popular product categories
st.subheader("Top 5 Most Popular Product Categories in SP")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="product_category_name_english", y="order_id", data=top_5_categories.head(10), palette=colors, ax=ax)
ax.set_ylabel("Number of Orders", fontsize=15)
ax.set_xlabel("Product Category", fontsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10, rotation=45)
st.pyplot(fig)

#plotting top 10 negara pengguna credit card
credit_card_data = creditcard_usage_df.sort_values(by="customer_id", ascending=False)
st.subheader("Top 10 States with Highest Credit Card Usage")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="customer_state", y="customer_id", data=credit_card_data.head(10), palette="viridis", ax=ax)
ax.set_xlabel("State", fontsize=15)
ax.set_ylabel("Number of Credit Card Users", fontsize=15)
ax.set_title("Credit Card Usage by State", fontsize=40)
st.pyplot(fig)



# Plotting performa penjualan product
st.subheader("Best-selling and Worst-selling Product Categories")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Plot best selling
bestselling_df = bestselling_df.sort_values(by="order_id", ascending=False)
sns.barplot(x=bestselling_df.index, y="order_id", data=bestselling_df.head(5), ax=ax[0])
ax[0].set_xlabel("Product Category",fontsize=30)
ax[0].set_ylabel("Number of Orders",fontsize=30)
ax[0].set_title("Best-selling Product Categories",fontsize=55)
ax[0].tick_params(axis='x', labelsize=25,rotation=45)
ax[0].tick_params(axis='y', labelsize=25)

# Plot worst selling
worstselling_df = worstselling_df.sort_values(by="order_id", ascending=False)
sns.barplot(x=worstselling_df.index, y="order_id", data=worstselling_df.head(5), ax=ax[1])
ax[1].set_xlabel("Product Category",fontsize=30)
ax[1].set_ylabel("Number of Orders",fontsize=30)
ax[1].set_title("Worst-selling Product Categories", fontsize=55)
ax[1].tick_params(axis='x', labelsize=25,rotation=45)
ax[1].tick_params(axis='y', labelsize=25)

st.pyplot(fig)



