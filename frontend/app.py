import streamlit as st
import requests
from PIL import Image
import json
import io

# Page configuration
st.set_page_config(
    page_title="Intelligent OCR System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .entity-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API endpoint configuration
    api_url = st.text_input(
        "Backend API URL",
        value="http://localhost:8000",
        help="Enter the backend API URL"
    )
    
    st.markdown("---")
    st.markdown("### 📋 About")
    st.markdown("""
    This Intelligent OCR system:
    - Extracts text from images
    - Analyzes document layout
    - Identifies entities (names, emails, etc.)
    - Provides structured output
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 SPAZORLABS Task 2")
    st.markdown("AI/ML Internship Assignment")

# Main content
st.title("🔍 Intelligent OCR & Document Understanding System")
st.markdown("Upload a document image to extract text, analyze layout, and identify entities")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a document image",
    type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
    help="Upload a scanned document or image containing text"
)

if uploaded_file:
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Original Document")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True, caption=f"Uploaded: {uploaded_file.name}")
        
        # Image info
        st.info(f"**Image Size:** {image.size[0]} x {image.size[1]} pixels")
    
    with col2:
        st.subheader("⚙️ Processing Results")
        
        # Process button
        if st.button("🚀 Process Document", type="primary"):
            with st.spinner("Processing document... This may take a few seconds..."):
                try:
                    # Prepare file for upload
                    uploaded_file.seek(0)
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    
                    # Call API
                    response = requests.post(
                        f"{api_url}/api/process-document",
                        files=files,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("✅ Processing Complete!")
                        
                        # Store result in session state
                        st.session_state['result'] = result
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API. Make sure the backend is running!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Display results if available
if 'result' in st.session_state:
    result = st.session_state['result']
    
    st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Extracted Text", "🎯 Entities", "📊 Layout Analysis", "📈 Statistics"])
    
    with tab1:
        st.subheader("Extracted Text")
        
        # Full text
        full_text = result["ocr"]["full_text"]
        st.text_area(
            "Complete Text",
            full_text,
            height=300,
            help="All text extracted from the document"
        )
        
        # Download button
        st.download_button(
            label="📥 Download Text",
            data=full_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
        
        # Text blocks with confidence
        with st.expander("🔍 View Text Blocks with Confidence Scores"):
            for i, block in enumerate(result["ocr"]["text_blocks"][:10]):  # Show first 10
                confidence_color = "🟢" if block["confidence"] > 0.8 else "🟡" if block["confidence"] > 0.6 else "🔴"
                st.markdown(f"{confidence_color} **Block {i+1}:** {block['text']} (Confidence: {block['confidence']:.2%})")
    
    with tab2:
        st.subheader("🎯 Extracted Entities")
        
        entities = result["entities"]
        total_entities = result["metadata"]["total_entities_found"]
        
        if total_entities > 0:
            st.success(f"Found {total_entities} entities in the document")
            
            # Create columns for different entity types
            ent_col1, ent_col2 = st.columns(2)
            
            with ent_col1:
                if entities["persons"]:
                    st.markdown("**👤 Persons:**")
                    for person in entities["persons"]:
                        st.markdown(f"- {person}")
                
                if entities["organizations"]:
                    st.markdown("**🏢 Organizations:**")
                    for org in entities["organizations"]:
                        st.markdown(f"- {org}")
                
                if entities["locations"]:
                    st.markdown("**📍 Locations:**")
                    for loc in entities["locations"]:
                        st.markdown(f"- {loc}")
                
                if entities["dates"]:
                    st.markdown("**📅 Dates:**")
                    for date in entities["dates"]:
                        st.markdown(f"- {date}")
            
            with ent_col2:
                if entities["emails"]:
                    st.markdown("**📧 Emails:**")
                    for email in entities["emails"]:
                        st.markdown(f"- {email}")
                
                if entities["phones"]:
                    st.markdown("**📞 Phone Numbers:**")
                    for phone in entities["phones"]:
                        st.markdown(f"- {phone}")
                
                if entities["amounts"]:
                    st.markdown("**💰 Amounts:**")
                    for amount in entities["amounts"]:
                        st.markdown(f"- {amount}")
                
                if entities["urls"]:
                    st.markdown("**🔗 URLs:**")
                    for url in entities["urls"]:
                        st.markdown(f"- {url}")
            
            # Download entities as JSON
            st.download_button(
                label="📥 Download Entities (JSON)",
                data=json.dumps(entities, indent=2),
                file_name="extracted_entities.json",
                mime="application/json"
            )
        else:
            st.info("No entities found in the document")
    
    with tab3:
        st.subheader("📊 Layout Analysis")
        
        layout = result["layout"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Blocks", layout["total_blocks"])
            st.metric("Has Tables", "Yes" if layout["has_tables"] else "No")
        
        with col2:
            # Block type distribution
            block_types = {}
            for block in layout["blocks"]:
                block_type = block["type"]
                block_types[block_type] = block_types.get(block_type, 0) + 1
            
            st.markdown("**Block Type Distribution:**")
            for block_type, count in block_types.items():
                st.markdown(f"- {block_type}: {count}")
        
        # Show block details
        with st.expander("🔍 View Block Details"):
            for i, block in enumerate(layout["blocks"][:15]):  # Show first 15
                st.markdown(f"**Block {i+1}:** Type: `{block['type']}`, Area: {block['area']} px²")
    
    with tab4:
        st.subheader("📈 Document Statistics")
        
        # Create metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Word Count",
                result["ocr"]["word_count"]
            )
        
        with col2:
            st.metric(
                "Character Count",
                result["ocr"]["character_count"]
            )
        
        with col3:
            st.metric(
                "OCR Confidence",
                f"{result['ocr']['average_confidence']:.1%}"
            )
        
        with col4:
            st.metric(
                "Entities Found",
                result["metadata"]["total_entities_found"]
            )
        
        # Image metadata
        st.markdown("---")
        st.markdown("**Image Metadata:**")
        metadata = result["metadata"]["image_dimensions"]
        st.json({
            "Width": f"{metadata['width']} px",
            "Height": f"{metadata['height']} px",
            "Channels": metadata['channels'],
            "Aspect Ratio": f"{metadata['width']/metadata['height']:.2f}"
        })
        
        # Download complete results
        st.download_button(
            label="📥 Download Complete Results (JSON)",
            data=json.dumps(result, indent=2),
            file_name="ocr_results.json",
            mime="application/json"
        )

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Intelligent OCR System | SPAZORLABS AI/ML Internship Task 2</p>
        <p>Built with FastAPI, EasyOCR, spaCy, and Streamlit</p>
    </div>
""", unsafe_allow_html=True)
