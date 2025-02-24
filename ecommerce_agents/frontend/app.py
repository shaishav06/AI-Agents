import sys
import os
import streamlit as st

# Add the root directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.inventory_agent import InventoryAgent
from agents.payment_agent import PaymentAgent

st.title("E-Commerce AI Agents")

option = st.selectbox("Select Agent", ["Inventory", "Payment"])

if option == "Inventory":
    product_id = st.text_input("Enter Product ID")
    if st.button("Check Stock"):
        agent = InventoryAgent()
        st.write(agent.check_stock(product_id))

elif option == "Payment":
    user_id = st.text_input("Enter User ID")
    amount = st.number_input("Enter Amount", min_value=1)
    if st.button("Process Payment"):
        agent = PaymentAgent()
        st.write(agent.process_payment(user_id, amount))
