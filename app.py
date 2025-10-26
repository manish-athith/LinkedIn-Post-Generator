import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'venv', 'Lib', 'site-packages'))

# Load environment variables
load_dotenv()

# Set up the page
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="centered"
)

# Title and description
st.title("🚀 LinkedIn Post Generator")
st.markdown("Create engaging LinkedIn posts in seconds!")

# Sidebar for API key input
with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("Enter your Groq API Key:", type="password")
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.warning("⚠️ Please enter your Groq API key to continue")
    else:
        st.success("✅ API key loaded!")
    
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("1. Enter your Groq API key")
    st.markdown("2. Fill in the topic and preferences")
    st.markdown("3. Click Generate!")
    st.markdown("4. Copy and post to LinkedIn")

# Main input form
with st.form("post_form"):
    st.subheader("📝 Create Your Post")
    
    topic = st.text_input(
        "What's your post about?",
        placeholder="e.g., AI in healthcare, career tips, project success..."
    )
    
    tone = st.selectbox(
        "Select tone:",
        ["Professional", "Casual", "Inspirational", "Technical", "Storytelling"]
    )
    
    length = st.selectbox(
        "Post length:",
        ["Short (1-2 paragraphs)", "Medium (3-4 paragraphs)", "Long (5+ paragraphs)"]
    )
    
    include_hashtags = st.checkbox("Include relevant hashtags", value=True)
    include_emoji = st.checkbox("Include emojis", value=True)
    
    generate_button = st.form_submit_button("✨ Generate Post")

# Function to generate LinkedIn post using Groq directly
def generate_linkedin_post(topic, tone, length, include_hashtags, include_emoji, api_key):
    try:
        # Initialize Groq client
        client = Groq(api_key=api_key)
        
        # Create the prompt
        prompt = f"""
        Create a professional LinkedIn post about: {topic}
        
        Requirements:
        - Tone: {tone}
        - Length: {length}
        - Include hashtags: {include_hashtags}
        - Include emojis: {include_emoji}
        
        Make it engaging and professional:
        - Start with an attention-grabbing hook
        - Provide valuable insights or information  
        - End with a question or call-to-action
        - Use proper line breaks for readability
        - { "Include 3-5 relevant hashtags at the end" if include_hashtags else "No hashtags" }
        - { "Use 2-3 relevant emojis appropriately" if include_emoji else "No emojis" }
        
        LinkedIn Post:
        """
        
        # Generate the post
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error generating post: {str(e)}"

# Handle form submission
if generate_button:
    if not api_key:
        st.error("❌ Please enter your Groq API key in the sidebar!")
    elif not topic:
        st.error("❌ Please enter a topic for your post!")
    else:
        with st.spinner("🤖 Generating your amazing LinkedIn post..."):
            post = generate_linkedin_post(
                topic, tone, length, include_hashtags, include_emoji, api_key
            )
        
        # Display the generated post
        st.success("✅ Post generated successfully!")
        st.subheader("📋 Your LinkedIn Post:")
        
        # Create a nice container for the post
        st.text_area(
            "Generated Post",
            post,
            height=300,
            key="generated_post"
        )
        
        # Copy button functionality
        if st.button("📋 Copy to Clipboard"):
            st.write("📋 **Pro tip**: Select the text above and press Ctrl+C to copy!")
        
        # Tips for posting
        with st.expander("💡 Tips for Posting on LinkedIn"):
            st.markdown("""
            - **Post at optimal times**: Weekdays 9-11 AM or 1-3 PM
            - **Engage with comments**: Reply to comments to boost visibility
            - **Add relevant media**: Images/videos increase engagement
            - **Use 3-5 hashtags**: For better discoverability
            - **Tag relevant people/companies**: When appropriate
            """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using LLaMA 3.2, Groq, and Streamlit by Manish Choudhary")