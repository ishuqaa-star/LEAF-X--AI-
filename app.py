import openai
import streamlit as st
from openai import OpenAI, api_key
import base64
import os

client = OpenAI(api_key=api_key)

# 🔐 Use environment variable (SAFE method)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY is missing. Add it in Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

st.set_page_config(
    page_title="LEAF X - Plant AI",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 LEAF X - Plant AI Assistant")
st.subheader("Upload a plant image or enter plant name")

# INPUTS
plant_name = st.text_input("Enter Plant Name (optional)")
uploaded_file = st.file_uploader("Upload Plant Image", type=["jpg", "jpeg", "png"])


# 🌱 TEXT FUNCTION
def classify_text(plant):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert botanist. Give classification, scientific name, characteristics, uses in simple student-friendly language."
            },
            {
                "role": "user",
                "content": plant
            }
        ]
    )
    return response.choices[0].message.content


# 📸 IMAGE ENCODING
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")


# 🌿 IMAGE FUNCTION
def classify_image(image_file):
    img_base64 = encode_image(image_file)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Identify this plant and give classification, scientific name, characteristics, uses."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content


# ---------------- UI ---------------- #

if st.button("Analyze Plant 🌿"):

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Plant", use_container_width=True)

        with st.spinner("Analyzing image..."):
            result = classify_image(uploaded_file)

        st.success("Analysis Complete!")
        st.markdown(result)

    elif plant_name.strip() != "":
        with st.spinner("Analyzing plant name..."):
            result = classify_text(plant_name)

        st.success("Analysis Complete!")
        st.markdown(result)

    else:
        st.warning("Please enter a plant name or upload an image.")

st.markdown("---")
st.write("🌱 Examples: Neem, Mango, Rose, Tulsi, Aloe Vera, Bamboo")