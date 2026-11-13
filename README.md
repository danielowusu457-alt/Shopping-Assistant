# AI Shopping Assistant

## 1. Project Overview

The AI Shopping Assistant is a retail application built with Python, Streamlit and Google's Gemini AI.

The application helps customers discover suitable products from a retail product catalogue based on their needs and budget. Customers can browse products, compare available options, build a shopping basket and generate a downloadable order enquiry.

The application combines Python-based product filtering and stock validation with AI-powered recommendations.

## 2. Project Objectives

- Help customers find products that meet their needs.
- Recommend suitable products within a customer's budget.
- Ensure recommendations are based on the actual product catalogue.
- Check product availability and stock quantities.
- Allow customers to compare two products.
- Calculate product subtotals and total basket value.
- Generate downloadable order enquiries.

## 3. Technologies Used

- **Python:** Application logic and calculations.
- **Streamlit:** User interface.
- **Google Gemini AI:** AI-powered product recommendations.
- **Pandas:** Product catalogue loading and data manipulation.
- **CSV:** Product catalogue storage.
- **python-dotenv:** Secure loading of API key configuration.

## 4. Key Features

### Product Catalogue
Customers can browse available products, search by product name or description, filter by category and display only products in stock.

### AI Product Recommendations
Customers describe what they need and enter their maximum budget. Python filters products based on price and stock availability before the eligible catalogue information is provided to Gemini for recommendations.

### Product Comparison
Customers can select two products and compare their categories, descriptions, prices and available stock.

### Shopping Basket
Customers can select products, enter quantities and add items to a shopping basket. The application checks requested quantities against available stock.

### Order Enquiry Generation
Customers can generate and download an order enquiry containing selected products, quantities, unit prices, subtotals and the total amount.

**Note:** An order enquiry is not a confirmed order. The retailer must confirm product availability and final prices.

## 5. Project Structure

```text
Shopping-Assistant/
│
├── src/
│   ├── main.py
│   └── catalogue_utils.py
│
├── data/
│   └── retail_sample_catalogue.csv
│
├── test_catalogue_utils.py
├── test_gemini.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `.env` file is created locally by each user and is not uploaded to GitHub because it contains the private Gemini API key.

## 6. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/danielowusu457-alt/Shopping-Assistant.git
```

### Step 2: Enter the project folder

```bash
cd Shopping-Assistant
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

For Git Bash on Windows:

```bash
source .venv/Scripts/activate
```

### Step 5: Install the required packages

```bash
pip install -r requirements.txt
```

### Step 6: Configure the Gemini API key

Create a file named `.env` in the main project folder (the same folder as `README.md`).

Add your Gemini API key:

```text
GEMINI_API_KEY=your_actual_api_key
```

Replace `your_actual_api_key` with your own API key.

**Security:** Never upload your `.env` file or share your API key publicly.

### Step 7: Run the application


```bash
streamlit run src/main.py
```


Streamlit will open the application in your web browser.

### Running the Automated Tests

The project includes automated tests to check whether the product catalogue validation works correctly.

To run the tests:

1. Activate your virtual environment.
2. Open the Git Bash terminal in the project folder.
3. Run the following command:

```bash
python -m unittest test_catalogue_utils -v
```

The tests check:
- Valid product catalogue.
- Missing required columns.
- Invalid product prices.
- Negative prices.
- Invalid stock quantities.
- Empty product catalogue.

All six tests should pass if the validation function is working correctly.

## 7. Testing

The application can be tested using the following scenarios:

1. Search and filter products in the catalogue.
2. Request headphones within a specified budget.
3. Enter a budget that is too low for any available product.
4. Request a product that is out of stock.
5. Compare two different products.
6. Add products to the shopping basket.
7. Attempt to add a quantity greater than available stock.
8. Calculate the basket total.
9. Generate and download an order enquiry.
10. Test the Gemini API connection and error handling.

To test the Gemini connection separately:

```bash
python test_gemini.py
```

## 8. Important Limitations

- Recommendations depend on the information contained in the product catalogue.
- The AI must not invent products, prices, features or stock information.
- Product prices and stock must be confirmed by the retailer.
- Generating an order enquiry does not mean an order has been confirmed.
- The application does not process payments.

## 9. Conclusion

The AI Shopping Assistant demonstrates how Python, Streamlit and Generative AI can be combined to improve the retail shopping experience.

It helps customers discover suitable products, compare available options, validate quantities and prepare order enquiries using information from a product catalogue.

The project demonstrates the practical application of Python programming, data handling, business rules and AI integration in a retail environment.