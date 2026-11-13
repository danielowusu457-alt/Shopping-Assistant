# AI Shopping Assistant

## 1. Project Overview

The AI Shopping Assistant is a retail application developed using Python, Streamlit and Google's Gemini AI.

The application helps customers find suitable products from a retail product catalogue based on their needs, preferences and available budget.

It also allows customers to compare products, select items and generate a downloadable order enquiry.

## 2. Project Objectives

- Help customers identify suitable products.
- Recommend products based on customer needs and budget.
- Ensure recommendations are based on actual catalogue information.
- Check product availability and stock quantities.
- Allow customers to compare products.
- Generate downloadable order enquiries.

## 3. Technologies Used

- Python
- Streamlit
- Google Gemini AI
- Pandas
- CSV (Product Catalogue)

## 4. Key Features

- Product catalogue browsing.
- Product search and filtering.
- AI-powered product recommendations.
- Budget-based product selection.
- Product comparison.
- Shopping basket.
- Stock and quantity validation.
- Downloadable order enquiry.
- Error handling for AI service failures.

## 5. Project Structure

```text
Shopping_Assistant/
│
├── src/
│   └── main.py
│
├── data/
│   └── retail_sample_catalogue.csv
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: Adjust this structure if your actual folders or filenames are different.*

## 6. Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Enter the project folder

```bash
cd Shopping_Assistant
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

For Git Bash:

```bash
source .venv/Scripts/activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure the Gemini API key

Add your Gemini API key to your environment configuration. Never publish your API key on GitHub.

### Step 7: Run the application

```bash
streamlit run src/main.py
```

## 7. Testing

The application is tested using different customer scenarios:

- Product recommendation based on customer needs.
- Budget restriction.
- Out-of-stock product requests.
- Product selection and quantity validation.
- Order enquiry generation.
- AI service error handling.

## 8. Important Limitations

- Product recommendations depend on the information available in the catalogue.
- Product prices and stock must be confirmed by the retailer.
- Generating an order enquiry does not mean an order has been confirmed.
- The application does not collect payments.

## 9. Conclusion

The AI Shopping Assistant provides a simple and interactive way for customers to discover products, compare available options and prepare order enquiries.

It combines Python-based validation with AI-powered recommendations to improve the shopping experience.