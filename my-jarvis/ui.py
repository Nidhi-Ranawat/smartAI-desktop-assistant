# import streamlit as st
# import multiprocessing

# def run_voice_assistant():
#     from voiceassisstant import main  # Assuming your voice assistant code is in a file named voice_assistant.py
#     main()

# def main():
#     # Set a background image using HTML and CSS
#     st.markdown(
#         """
#         <style>
#             body {
#                 background-image: url('jarvisBG.jpg');  /* Replace with the path to your background image */
#                 background-size: cover;
#                 font-family: 'Helvetica', sans-serif;  /* Adjust the font family as needed */
#             }
#             .stApp {
#                 max-width: 900px;  /* Adjust the max width of the app */
#                 margin: 0 auto;  /* Center the app on the page */
#             }
#             .sidebar .sidebar-content {
#                 background-color: #f0f0f0;  /* Adjust the sidebar background color */
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

#     st.title("Voice Assistant UI")

#     if st.button("Start Voice Assistant"):
#         st.text("Voice Assistant will start in a moment...")
#         # Run the voice assistant in a separate process
#         process = multiprocessing.Process(target=run_voice_assistant)
#         process.start()

#     # Get email information from the user using Streamlit input components
#     st.sidebar.header("Send Email")

#     to_email = st.sidebar.text_input("To Email", key="to_email")
#     subject = st.sidebar.text_input("Subject", key="subject")
    
#     st.sidebar.write("Email Body:")
#     body = st.sidebar.text_area("Body", height=150, key="body")

#     if st.sidebar.button("Send Email"):
#         # Send the email
#         from voiceassisstant import send_email
#         send_email(to_email, subject, body)

# if __name__ == "__main__":
#     main()

import streamlit as st
import multiprocessing

# User database (replace with a more secure method in a real-world application)
user_database = {'password': 'xyz', 'name': 'Nidhi'}  # 'user2': {'password': 'pass456', 'name': 'Jane Smith'},

def authenticate_user(username, password):
    if username in user_database["name"] and user_database['password'] == password:
        return True
    return False

def run_voice_assistant():
    from voiceassisstant import main  # Assuming your voice assistant code is in a file named voice_assistant.py
    main()

def main():
    # Set a background image using HTML and CSS
    st.markdown(
        """
        <style>
            body {
                background-image: url('jarvisBG.jpg');  /* Replace with the path to your background image */
                background-size: cover;
                font-family: 'Helvetica', sans-serif;  /* Adjust the font family as needed */
            }
            .stApp {
                max-width: 900px;  /* Adjust the max width of the app */
                margin: 0 auto;  /* Center the app on the page */
            }
            .sidebar .sidebar-content {
                background-color: #f0f0f0;  /* Adjust the sidebar background color */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Voice Assistant UI")

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        print(f"Attempting login with username: {username}, password: {password}")
        if authenticate_user(username, password):
            st.success(f"Welcome back, {username}!")
            st.text("Voice Assistant will start in a moment...")
            # Rest of the code...
            process = multiprocessing.Process(target=run_voice_assistant)
            process.start()
        else:
            st.error(f"Invalid credentials. Please try again.\n {username} \n {password}")


    # Get email information from the user using Streamlit input components
    st.sidebar.header("Send Email")

    to_email = st.sidebar.text_input("To Email", key="to_email")
    subject = st.sidebar.text_input("Subject", key="subject")
    
    st.sidebar.write("Email Body:")
    body = st.sidebar.text_area("Body", height=150, key="body")

    if st.sidebar.button("Send Email"):
        # Send the email
        from voiceassisstant import send_email
        send_email(to_email, subject, body)

if __name__ == "__main__":
    main()
