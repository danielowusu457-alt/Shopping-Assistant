
import pandas as pd
import streamlit as st
from pathlib import Path
import os
from catalogue_utils import validate_catalogue

from dotenv import load_dotenv
from google import genai

def reset_app():
    st.session_state.basket = []
    st.session_state.basket_product = None

# Load the secret API key
load_dotenv()

# Set up the application
st.set_page_config(page_title="Shopping Assistant")

st.title("My Shopping Assistant")
st.write("Welcome! Browse and search our available products.")

# Locate the product catalogue
catalogue_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "retail_sample_catalogue.csv"
)

# Load the product catalogue
@st.cache_data
def load_catalogue(file_path, file_modified_time):
    return pd.read_csv(file_path, sep="\t")


# Load and validate the product catalogue
try:
    products = load_catalogue(
    str(catalogue_path),
    catalogue_path.stat().st_mtime
)

except FileNotFoundError:
    st.error("Product catalogue file could not be found.")
    st.stop()

except pd.errors.ParserError:
    st.error("There is a problem with the product catalogue format.")
    st.stop()

# Check that all required columns exist
try:
    products = validate_catalogue(products)

except ValueError as error:
    st.error(str(error))
    st.stop()
# Check that the catalogue is not empty
if products.empty:
    st.error("The product catalogue is empty.")
    st.stop()

# Convert price and stock columns into numbers
products["price_ghs"] = pd.to_numeric(
    products["price_ghs"], errors="coerce"
)

products["stock_qty"] = pd.to_numeric(
    products["stock_qty"], errors="coerce"
)

# Validate product prices
if products["price_ghs"].isna().any() or (products["price_ghs"] < 0).any():
    st.error("Product prices must be valid, non-negative numbers.")
    st.stop()

# Validate stock quantities
if (
    products["stock_qty"].isna().any()
    or (products["stock_qty"] < 0).any()
    or (products["stock_qty"] % 1 != 0).any()
):
    st.error("Stock quantities must be non-negative whole numbers.")
    st.stop()


# Create the search box and category filter
st.subheader("Our Product Catalogue")

col1, col2 = st.columns(2)

with col1:
    search_text = st.text_input("Search for a product")

with col2:
    categories = ["All categories"] + sorted(
        products["category"].dropna().unique().tolist()
    )
    selected_category = st.selectbox("Choose a category", categories)

# Create an in-stock checkbox
show_available = st.checkbox("Show only products in stock")

# Make a copy of the catalogue for filtering
filtered_products = products.copy()

# Filter by product name or description
if search_text:
    filtered_products = filtered_products[
        filtered_products["name"].str.contains(
            search_text, case=False, na=False
        )
        | filtered_products["description"].str.contains(
            search_text, case=False, na=False
        )
    ]

# Filter by category
if selected_category != "All categories":
    filtered_products = filtered_products[
        filtered_products["category"] == selected_category
    ]

# Filter by stock availability
if show_available:
    filtered_products = filtered_products[
        filtered_products["stock_qty"] > 0
    ]

# Display the results
st.write(f"Products found: {len(filtered_products)}")
st.dataframe(filtered_products, use_container_width=True, hide_index=True)


# --------------------------------
# CUSTOMER PRODUCT RECOMMENDATION
# --------------------------------

st.subheader("Find Products Within Your Budget")

# Ask the customer what they need
customer_need = st.text_input(
    "What product are you looking for?",
    placeholder="Example: headphones"
)

# Ask the customer for their budget
customer_budget = st.number_input(
    "What is your maximum budget (GH¢)?",
    min_value=0.0,
    value=250.0,
    step=10.0
)

# Search for matching products
if st.button("Find Suitable Products"):

    if customer_need.strip() == "":
        st.warning("Please enter the product you are looking for.")

    else:
        # Check the product name and description
        matching_products = products[
            products["name"].str.contains(
                customer_need, case=False, na=False
            )
            | products["description"].str.contains(
                customer_need, case=False, na=False
            )
        ]

        # Keep only products that are in stock
        matching_products = matching_products[
            matching_products["stock_qty"] > 0
        ]

        # Keep only products within the customer's budget
        matching_products = matching_products[
            matching_products["price_ghs"] <= customer_budget
        ]

        # Display suitable products
        if matching_products.empty:
            st.warning(
                "Sorry, no available products match your needs and budget."
            )
        else:
            st.success("We found products that match your requirements!")

            st.dataframe(
                matching_products,
                use_container_width=True,
                hide_index=True
            )


# --------------------------------
# PRODUCT COMPARISON
# --------------------------------

st.subheader("Compare Two Products")

# Get the names of all products
product_names = products["name"].tolist()

# Create two selection boxes
col1, col2 = st.columns(2)

with col1:
    product_one = st.selectbox(
        "Choose your first product",
        product_names,
        key="compare_product_one"
    )

with col2:
    product_two = st.selectbox(
        "Choose your second product",
        product_names,
        index=1 if len(product_names) > 1 else 0,
        key="compare_product_two"
    )

# Find the selected products in the catalogue
first_product = products[
    products["name"] == product_one
].iloc[0]

second_product = products[
    products["name"] == product_two
].iloc[0]

# Display the comparison
if product_one == product_two:
    st.warning("Please select two different products.")

else:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### {first_product['name']}")
        st.write(f"**Category:** {first_product['category']}")
        st.write(f"**Description:** {first_product['description']}")
        st.write(f"**Price:** GH¢{first_product['price_ghs']:,.2f}")
        st.write(f"**Available stock:** {first_product['stock_qty']}")

    with col2:
        st.markdown(f"### {second_product['name']}")
        st.write(f"**Category:** {second_product['category']}")
        st.write(f"**Description:** {second_product['description']}")
        st.write(f"**Price:** GH¢{second_product['price_ghs']:,.2f}")
        st.write(f"**Available stock:** {second_product['stock_qty']}")

    # Compare prices
    if first_product["price_ghs"] < second_product["price_ghs"]:
        st.info(f"{first_product['name']} is cheaper.")

    elif first_product["price_ghs"] > second_product["price_ghs"]:
        st.info(f"{second_product['name']} is cheaper.")

    else:
        st.info("Both products have the same price.")


# --------------------------------
# SHOPPING BASKET
# --------------------------------

st.subheader("Build Your Shopping Basket")

if st.button("Reset / Start Over"):
    reset_app()
    st.rerun()

# Create a basket that remembers items during the session
if "basket" not in st.session_state:
    st.session_state.basket = []

# Let the customer select a product
selected_item = st.selectbox(
    "Select a product to add",
    products["name"].tolist(),
    key="basket_product"
)

# Retrieve the selected product details
matching_products = products[
    products["name"] == selected_item
]

if not matching_products.empty:
    item_details = matching_products.iloc[0]

    available_stock = int(item_details["stock_qty"])
    item_price = float(item_details["price_ghs"])

    # Show product information
    st.write(f"**Price:** GH¢{item_price:,.2f}")
    st.write(f"**Available stock:** {available_stock}")

else:
    st.warning("Please select a valid product.")
# Ask for quantity
quantity = st.number_input(
    "Enter quantity",
    min_value=1,
    max_value=100,
    value=1,
    step=1,
    key="basket_quantity"
)

# Add product to basket
if st.button("Add to Basket"):

    if available_stock == 0:
        st.error("Sorry, this product is out of stock.")

    else:
        # Check whether the product is already in the basket
        existing_item = next(
            (
                item for item in st.session_state.basket
                if item["product_id"] == item_details["product_id"]
            ),
            None
        )

        current_quantity = (
            existing_item["quantity"] if existing_item else 0
        )

        requested_quantity = current_quantity + quantity

        # Validate the requested quantity against available stock
        if requested_quantity > available_stock:
            st.error(
                f"Insufficient stock! Only {available_stock} units "
                "are available."
            )

        else:
            if existing_item:
                existing_item["quantity"] = requested_quantity

            else:
                st.session_state.basket.append({
                    "product_id": item_details["product_id"],
                    "name": item_details["name"],
                    "price": item_price,
                    "quantity": quantity
                })

            st.success("Product successfully added to your basket!")

# Display shopping basket
st.subheader("Your Shopping Basket")

if st.session_state.basket:

    basket_df = pd.DataFrame(st.session_state.basket)

    # Calculate the amount for each product
    basket_df["subtotal"] = (
        basket_df["price"] * basket_df["quantity"]
    )

    st.dataframe(
        basket_df,
        use_container_width=True,
        hide_index=True
    )

    # Calculate the total amount
    total_amount = basket_df["subtotal"].sum()

    st.metric("Total Amount", f"GH¢{total_amount:,.2f}")

    # Clear the basket
    if st.button("Clear Basket"):
        st.session_state.basket = []
        st.rerun()

else:
    st.info("Your shopping basket is currently empty.")


# --------------------------------
# DOWNLOADABLE ORDER ENQUIRY
# --------------------------------

st.subheader("Prepare Your Order Enquiry")

if st.session_state.basket:

    # Ask for the customer's name
    customer_name = st.text_input(
        "Customer name (optional)",
        placeholder="Enter your name"
    )

    # Calculate the total amount
    total_amount = sum(
        item["price"] * item["quantity"]
        for item in st.session_state.basket
    )

    # Prepare the enquiry document
    from datetime import datetime

    enquiry_lines = []

    enquiry_lines.append("SHOPPING ORDER ENQUIRY")
    enquiry_lines.append("=" * 35)
    enquiry_lines.append(f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    enquiry_lines.append(f"Customer: {customer_name or 'Not provided'}")
    enquiry_lines.append("")
    enquiry_lines.append("SELECTED PRODUCTS")
    enquiry_lines.append("-" * 35)

    for item in st.session_state.basket:

        subtotal = item["price"] * item["quantity"]

        enquiry_lines.append(f"Product: {item['name']}")
        enquiry_lines.append(f"Product ID: {item['product_id']}")
        enquiry_lines.append(f"Quantity: {item['quantity']}")
        enquiry_lines.append(f"Unit Price: GH¢{item['price']:,.2f}")
        enquiry_lines.append(f"Subtotal: GH¢{subtotal:,.2f}")
        enquiry_lines.append("-" * 35)

    enquiry_lines.append(f"TOTAL AMOUNT: GH¢{total_amount:,.2f}")
    enquiry_lines.append("")
    enquiry_lines.append(
        "IMPORTANT: This is an order enquiry only, not a confirmed order."
    )
    enquiry_lines.append(
        "The shop must confirm product availability and final prices."
    )

    # Convert the enquiry into downloadable text
    enquiry_document = "\n".join(enquiry_lines)

    # Create the download button
    st.download_button(
        label="Download Order Enquiry",
        data=enquiry_document,
        file_name="shopping_order_enquiry.txt",
        mime="text/plain"
    )

else:
    st.info(
        "Please add at least one product to your basket "
        "before preparing an order enquiry."
    )


# --------------------------------
# AI SHOPPING ASSISTANT
# --------------------------------

st.subheader("Ask Our AI Shopping Assistant")

# Get the customer's request
ai_customer_request = st.text_area(
    "Describe what you are looking for",
    placeholder="Example: I need comfortable wireless headphones for online classes."
)

# Get the customer's budget
ai_budget = st.number_input(
    "What is your maximum budget? (GH¢)",
    min_value=0.0,
    value=250.0,
    step=10.0,
    key="ai_budget"
)

# Ask Gemini to recommend products
if st.button("Ask Gemini", key="ask_gemini"):

    if not ai_customer_request.strip():
        st.warning("Please describe what you are looking for.")

    else:
        # Python checks stock and budget first
        eligible_products = products[
            (products["stock_qty"] > 0)
            & (products["price_ghs"] <= ai_budget)
        ]

        if eligible_products.empty:
            st.warning(
                "There are no available products within your budget."
            )

        else:
            # Check that the API key is available
            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                st.error("Gemini API key was not found.")

            else:
                # Prepare the catalogue for Gemini
                catalogue_information = eligible_products[
                    [
                        "product_id",
                        "name",
                        "category",
                        "description",
                        "price_ghs",
                        "stock_qty"
                    ]
                ].to_string(index=False)

                # Prepare instructions for Gemini
                prompt = f"""
                You are a professional shopping assistant for a retail store.
                
                Your job is to recommend products based on customer's actual needs.

                Customers Request:
                {ai_customer_request}

                Customers Maximum Budget GH¢{ai_budget}.

                Available Products:

                {catalogue_information}

               IMPORTANT RULES:
                1. Understand exactly what the customer is looking for.
                2. Recommend only products that directly match the customer's request.
                3. Do not recommend a product simply because it is within the budget.
                4. Consider the product name, category and description when deciding whether it matches.
                5. Recommend only products provided in the available product list.
                6. Do not invent product names, prices, features, discounts or stock information.
                7. Do not recommend products that are unrelated to the customer's request.
                8. If no available product matches the customer's needs, clearly say that no suitable product was found.
                9. If several products match, compare their advantages and disadvantages.
                10. Explain why each recommended product is suitable.
                11. Keep your response clear, friendly and easy to understand.

                Important Exmaples
                If a customer requests headphones for online classes:
                - Headphones and headsets may be suitable.
                - A headset with a microphone may be especially useful for online classes.
                - A webcam is NOT a suitable replacement for headphones, even if it is within budget.
                
                Your final recommendation must satisfy BOTH the customer's needs and budget.
                """

                try:
                    # Connect to Gemini
                    client = genai.Client(api_key=api_key)

                    # Send the customer request to Gemini
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )

                    # Display Gemini's recommendation
                    st.subheader("Gemini's Recommendations")
                    st.write(response.text)

                    client.close()

                except Exception as error:
                   error_message = str(error)

                   if "503" in error_message or "UNAVAILABLE" in error_message:
                       st.warning(
                           "Our AI assistant is temporarily busy. "
                           "Please wait a moment and try again."
                        )

                   elif "API_KEY_INVALID" in error_message or "401" in error_message:
                        st.error(
                            "The AI service could not authenticate. "
                            "Please check the API configuration."
                        )

                   else:
                      st.error(
                          "Sorry, something went wrong while generating "
                          "your recommendation. Please try again later."
                        )

