import streamlit as st
import threading
from PIL import Image

# Function to run the main logic in a separate thread
def run_main_logic():
    import voiceassisstant  # Replace with the actual name of your main script
    voiceassisstant.main()

# Set page title and icon
st.set_page_config(page_title="Personal Assistant", page_icon="🤖")

# Main Streamlit UI
st.title("Personal Assistant")

# Run the main logic in a separate thread
if st.button("Start Personal Assistant"):
    st.text("Your personal assistant is starting. Please wait...")
    t = threading.Thread(target=run_main_logic)
    t.start()

# Display some information about the project
st.markdown("""
    #### About the Project
    This is a simple personal assistant implemented in Python. It can perform various tasks such as sending emails, playing music, providing weather information, and more.
    """)

# Display an image or GIF related to your project
image = Image.open("jarvis.jpg")  # Replace with the actual path to your image or GIF
st.image(image, caption="Your Personal Assistant", use_column_width=True)

# Additional sections for displaying project details, credits, etc., can be added here
# st.write("## Project Details")
# st.write("...")
