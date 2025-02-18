# Shopping Helper Agent

## AI Shopping Partner

A Streamlit-based application that uses Google's Gemini AI to analyze product images and provide shopping recommendations.

## Setup Instructions

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   - Create a `.env` file in the project root
   - Add your Google API key: `GOOGLE_API_KEY=your_key_here`
   - Add your Fircrawl API key: `FIRCRAWL_API_KEY=your_key_here`

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Features

- Image upload and analysis
- Product identification using Gemini AI
- Custom search parameters:
  - Color preference
  - Purpose/use case
  - Budget constraints
- Provides shopping recommendations with direct product links

## Requirements

- Python 3.8+
- Streamlit
- Google Gemini AI API access
- PIL (Python Imaging Library)
- Other dependencies listed in requirements.txt

> **Note**: Ensure you have valid API keys for both Google Gemini services and Fircrawl.
