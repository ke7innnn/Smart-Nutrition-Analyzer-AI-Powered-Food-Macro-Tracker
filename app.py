import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Smart Nutrition Analyzer", page_icon="🥗", layout="centered")

st.title("🥗 Smart Nutrition Analyzer")
st.caption("AI-Powered Food Recognition & Nutritional Breakdown")
st.write("Upload a food photo and receive a structured, professional nutritional analysis.")

uploaded_file = st.file_uploader("📸 Upload your meal photo", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Meal", use_column_width=True)

    if st.button("Analyze Nutrition"):
        with st.spinner("Analyzing..."):
            prompt = """
            You are a certified nutritionist. Analyze the uploaded food image and provide a professional nutritional breakdown.
            Format it like this:
            List of items: [Item 1] (quantity), [Item 2] (quantity)
            Calories: [Number] kcal
            Protein: [Number] g
            Carbohydrates: [Number] g
            Fats: [Number] g
            Fiber: [Number] g
            Sugar: [Number] g
            Sodium: [Number] mg
            Only return the information in this format, no extra text.
            """
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content([prompt, image])
                text = response.text.strip()

                if "This is not a food item." in text:
                    st.error(text)
                else:
                    lines = [line for line in text.split("\n") if line.strip()]
       
                    st.subheader("🍽️ Meal Items")
                    st.write(lines[0].replace("List of items:", "").strip())
          
                    st.subheader("⚖️ Nutritional Summary")
                    nutrients = {}
                    for line in lines[1:]:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            nutrients[key.strip()] = value.strip()
          
                    if nutrients:
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Calories", nutrients.get("Calories", "N/A"))
                        col2.metric("Protein", nutrients.get("Protein", "N/A"))
                        col3.metric("Carbs", nutrients.get("Carbohydrates", "N/A"))
                        col4.metric("Fats", nutrients.get("Fats", "N/A"))

                        col1, col2, col3 = st.columns(3)
                        col1.metric("Fiber", nutrients.get("Fiber", "N/A"))
                        col2.metric("Sugar", nutrients.get("Sugar", "N/A"))
                        col3.metric("Sodium", nutrients.get("Sodium", "N/A"))

                    st.success("Nutrition Analysis Complete!")

            except Exception as e:
                st.error("Error analyzing image.")
                st.error(str(e))
