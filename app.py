import os
import streamlit as st
from google import genai
from PIL import Image

# Page Config
st.set_page_config(page_title="AI Ad Optimizer", page_icon="🎯", layout="wide")
st.title("🎯 AI-Powered Ad Creative Optimizer")
st.write("Upload your Ad Banner to get Instant Feedback & AI Copy Suggestions!")

# API Key Access
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader("Upload Ad Banner (JPG/PNG)", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Ad Banner", use_column_width=True)

        product_type = st.text_input("Product/Service Category", placeholder="e.g. Headphones, Food")
        target_audience = st.text_input("Target Audience", placeholder="e.g. Students, Techies")

        analyze_btn = st.button("🚀 Analyze Ad Creative", type="primary")

    with col2:
        if analyze_btn:
            if not uploaded_file:
                st.error("Please upload an image first!")
            else:
                with st.spinner("Analyzing with Gemini AI..."):
                    prompt = f"""
                    You are an expert Meta Ads Strategist. Analyze this ad image.
                    Product Type: {product_type}
                    Target Audience: {target_audience}

                    Provide:
                    1. **Overall Score** out of 10.
                    2. **Visual & Layout Feedback**: What works well, what needs improvement.
                    3. **Text Clarity & CTA**: Analysis of headline, readability, and Call To Action.
                    4. **3 High-Converting Ad Headlines** to test.
                    5. **3 Actionable Design Suggestions** to boost conversion.
                    """
                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[image, prompt]
                        )
                        st.subheader("📊 Analysis Result")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error: {e}")
else:
    st.error("Gemini API Key is missing! Please set it in Streamlit Secrets.")
