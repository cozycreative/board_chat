import streamlit as st
import streamlit.components.v1 as components

# URL to redirect to
redirect_url = "https://www.stratboard.chat/"

# HTML/JavaScript for redirection
redirect_script = f"""
    <script type="text/javascript">
        window.top.location.href = "{redirect_url}";
    </script>
    <p>Redirecting to <a href="{redirect_url}">{redirect_url}</a>...</p>
"""

# Execute the redirect
components.html(redirect_script, height=100)

# Optionally, add a message in Streamlit as well
st.write(f"Attempting to redirect you to {redirect_url}...")
st.markdown(f"If you are not redirected automatically, [click here]({redirect_url}).")
