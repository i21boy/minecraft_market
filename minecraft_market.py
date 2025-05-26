import csv
import streamlit as st
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials

def setup_google_sheets():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    credentials = Credentials.from_service_account_file(
        'credentials.json',
        scopes=scopes
    )
    
    gc = gspread.authorize(credentials)
    return gc

def add_items(item, price, seller):
    gc = setup_google_sheets()
    sheet = gc.open('Minecraft Market').sheet1
    sheet.append_row([item, price, seller])

def view_market():
    try:
        gc = setup_google_sheets()
        sheet = gc.open('Minecraft Market').sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
        return pd.DataFrame(columns=["Item", "Price", "Seller"])

def delete_item(index):
    try:
        gc = setup_google_sheets()
        sheet = gc.open('Minecraft Market').sheet1
        sheet.delete_rows(index + 2)
        return True
    except Exception as e:
        st.error(f"Error deleting item: {e}")
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
        # Add delete section
        st.subheader("Delete Item")
        # Create a dropdown with all items
        items_to_delete = [f"{row['Item']} - {row['Price']} coins - {row['Seller']}" for _, row in df.iterrows()]
        selected_item = st.selectbox("Select item to delete:", items_to_delete)
        
        if st.button("Delete Selected Item"):
            # Find the index of the selected item
            selected_index = items_to_delete.index(selected_item)
            if delete_item(selected_index):
                st.success("Item deleted!")
                st.rerun()
        
        # Show the full table
        st.subheader("All Items")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Market is empty. Add some items!")


if __name__ == "__main__":
    main()

            
