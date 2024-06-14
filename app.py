import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader

# Set the page configuration
st.set_page_config(layout="wide")

# Add custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            padding: 2rem;
        }
        .sidebar .sidebar-content {
            background-color: #d0d4d8;
        }
        .block-container {
            max-width: 1200px;
        }
        .uploaded-file-info {
            font-size: 16px;
            color: #2b2b2b;
        }
        .summary-result {
            background-color: #e8f5e9;
            border-left: 5px solid #66bb6a;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def text_summary(text, maxlength=None):
    summary = Summary()
    result = summary(text)
    return result

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Add a header image
st.image("https://via.placeholder.com/1200x300.png?text=Document+Summarizer+App", use_column_width=True)

# Sidebar choice selection
choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])

if choice == "Summarize Text":
    st.subheader("Summarize Text")
    input_text = st.text_area("Enter your text here")
    if st.button("Summarize Text"):
        if input_text:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("**Your Input Text**")
                st.info(input_text)
            with col2:
                st.markdown("**Summary Result**")
                result = text_summary(input_text)
                st.success(result)
        else:
            st.error("Please enter some text to summarize.")

elif choice == "Summarize Document":
    st.subheader("Summarize Document")
    input_file = st.file_uploader("Upload your document here", type=['pdf'])
    if input_file:
        if st.button("Summarize Document"):
            with open("doc_file.pdf", "wb") as f:
                f.write(input_file.getbuffer())
            col1, col2 = st.columns([1, 1])
            with col1:
                st.info("File uploaded successfully", icon="✅")
                extracted_text = extract_text_from_pdf("doc_file.pdf")
                st.markdown("**Extracted Text is Below:**")
                st.info(extracted_text, icon="📄")
            with col2:
                st.markdown("**Summary Result**")
                doc_summary = text_summary(extracted_text)
                st.success(doc_summary)

# Add a footer
st.markdown("""
    <div style='text-align: center; padding: 10px; margin-top: 20px;'>
        <hr>
        <p style='font-size: 14px;'>Made with ❤️ using Streamlit</p>
    </div>
""", unsafe_allow_html=True)
