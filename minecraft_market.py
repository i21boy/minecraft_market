import csv
import streamlit as st
import pandas as pd
import os

def add_items(item, price, seller):
    with open("market_csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([item, price, seller])

def view_market():
    try:
        df = pd.read_csv("market_csv", names=["Item", "Price", "Seller"])
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Item", "Price", "Seller"])
    

def delete_item(index):
    try:
        df = pd.read_csv("market_csv", names=["Item", "Price", "Seller"])
        df = df.drop(index)
        df.to_csv("market_csv", index=False, header=False)
        return True
    except Exception as e:
        st.error("Error deleting item: {e}")
        return False

def main():
    st.title("Minecraft Market")
    
    # Sidebar for adding items
    with st.sidebar:
        st.header("Add New Item")
        item = st.text_input("Item Name")
        price = st.text_input("Price (coins)")
        seller = st.text_input("Seller Name")
        
        if st.button("Add Item"):
            if item and price and seller:
                add_items(item, price, seller)
                st.success("Item added successfully!")
            else:
                st.error("Please fill in all fields")

    # Main area for viewing market
    st.header("Market Items")
    df = view_market()
    if not df.empty:
        for idx, row in df.iterrows():
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"Item: {row['Item']} - Price: {row['Price']} - Seller: {row['Seller']} ")
            with col2:
                if st.button("Delete", key=f"delete_{idx}"):
                    if delete_item(idx):
                        st.success("Item deleted!")
                        st.rerun()
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Market is empty. Add some items!")


if __name__ == "__main__":
    main()

            
