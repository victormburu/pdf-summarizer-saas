import re

if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    st.warning("⚠️ Please enter a valid email address.")
else:
    # Proceed with Firebase login
