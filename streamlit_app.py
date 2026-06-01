import streamlit as st

st.set_page_config(page_title="Cipherish App", page_icon="⚿", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght=0,400;0,700;1,400&family=Poppins:wght=300;400;500;600&display=swap');

    html, body, [class*="css"], label, button, input, textarea {
        font-family: 'Poppins', sans-serif !important;
    }

    .stApp {
        background-color: #E6E6FA !important;
        background-image: none !important;
        color: #4B0082 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #D3D3F3 !important; 
        background-image: none !important;
    }
    
    [data-testid="stSidebar"] [class*="css"], 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #4B0082 !important;
    }

    .sidebar-hint {
        position: fixed;
        top: 13px;
        left: 55px;
        z-index: 999999;
        font-size: 0.82rem;
        font-weight: 500;
        color: #4B0082 !important;
        background-color: rgba(75, 0, 130, 0.12);
        padding: 4px 12px;
        border-radius: 20px;
        pointer-events: none;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }

    .app-title-container {
        text-align: center;
        margin-top: 10px;
        margin-bottom: 25px;
        width: 100%;
    }

    .app-title {
        font-family: 'Libre Baskerville', serif !important;
        font-size: 3.5rem;
        font-weight: 400;
        letter-spacing: 1px;
        color: #4B0082 !important;
    }

    .project-intro {
        font-family: 'Libre Baskerville', serif !important;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 5px;
        color: #4B0082 !important;
    }
    
    label, [data-testid="stMarkdownHint"] p, [data-testid="stRadio"] label p, p, span {
        color: #4B0082 !important;
    }

    code {
        color: #4B0082 !important;
        background-color: rgba(75, 0, 130, 0.08) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="sidebar-hint">⬅️ Click here to change your encoder settings</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="app-title-container">
        <div class="app-title">⚿ cipherish</div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("### ⚙️ Adjustments")
    mode = st.radio("Select Mode:", ("Encode", "Decode"), horizontal=True)
    
    st.markdown("---")
    shift_value = st.slider("Shift Amount:", min_value=1, max_value=15, value=5, step=1)
    block_size = st.slider("Block Size:", min_value=2, max_value=10, value=4, step=1)
    
    st.markdown("---")
    enable_reversal = st.checkbox("Enable Word Reversal", value=False)
    enable_numbers = st.checkbox("Enable Number Layer", value=False)

st.markdown('<p class="project-intro">Hi!! We created this tool for our Ling360 final project.</p>', unsafe_allow_html=True)
st.markdown('<p class="project-intro">You can type in your message below and we will encode it for you.</p>', unsafe_allow_html=True)
st.markdown('<p class="project-intro">Your secret is safe with us &lt;3</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

alphabet = "abcçdefgğhıijklmnoöprsştuüvxyz"

def cipher_encoder(text, shift, block, use_reversal, use_numbers):
    if not text:
        return ""
    new_text = ""
    for char in text.lower():
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index + shift) % len(alphabet)
            new_text += alphabet[new_index]
        else:
            new_text += char

    if use_numbers:
        temp_text = ""
        counter = 1
        for char in new_text:
            temp_text += char
            if char != " ":
                temp_text += str(counter)
                counter += 1
        new_text = temp_text

    words = new_text.split()
    if use_reversal:
        encoded_words = []
        for i in range(0, len(words), block):
            current_block = words[i:i+block]
            current_block.reverse()
            encoded_words.extend(current_block)
        words = encoded_words

    final_output = ""
    for word in words:
        if final_output == "":
            final_output += word
        else:
            final_output += " " + word
    return final_output

def cipher_decoder(text, shift, block, use_reversal, use_numbers):
    if not text:
        return ""
    if use_reversal:
        words = text.split()
        restored_words = []
        for i in range(0, len(words), block):
            current_block = words[i:i+block]
            current_block.reverse()
            restored_words.extend(current_block)
        text = " ".join(restored_words)

    if use_numbers:
        cleaned_text = ""
        for char in text:
            if not char.isdigit():
                cleaned_text += char
        text = cleaned_text

    words = text.split()
    text_to_shift = ""
    for word in words:
        if text_to_shift == "":
            text_to_shift += word
        else:
            text_to_shift += " " + word

    new_text = ""
    for char in text_to_shift.lower():
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index - shift) % len(alphabet)
            new_text += alphabet[new_index]
        else:
            new_text += char
    return new_text

input_text = st.text_area(
    label="Enter your text below:",
    placeholder="Type something here...",
    height=140
)

st.markdown("<br>", unsafe_allow_html=True)

if input_text:
    if mode == "Encode":
        result = cipher_encoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
    else:
        result = cipher_decoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
        
    st.code(result, language="text")
