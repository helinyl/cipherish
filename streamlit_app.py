import streamlit as st

st.set_page_config(page_title="Cipherish App", page_icon="🔑", layout="wide")

# --- SIMPLIFIED PRACTICAL STYLING ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Anonymous+Pro:ital,wght=0,400;0,700;1,400;1,700&family=Cinzel:wght@400;500;600&display=swap');

    /* Global Uniform Font Sizing & Base Theme */
    html, body, [class*="css"], label, button, input, textarea, p, span, div {
        font-family: 'Anonymous Pro', monospace !important;
        font-size: 1rem !important;
    }

    .stApp {
        background-color: #FFF0F5 !important;
        color: #C71585 !important;
    }

    /* Target native Streamlit borders to style them pink with a soft background fill */
    [data-testid="stContainerBorder"] {
        background-color: #FFE4E1 !important;
        border: 6px solid #FF69B4 !important;
        border-radius: 30px !important;
        padding: 25px !important;
    }

    /* Premium Heading Styles */
    .panel-title {
        font-family: 'Cinzel', serif !important;
        font-weight: 500 !important;
        font-size: 1.5rem !important;
        text-align: center;
        color: #FF69B4 !important;
        margin-bottom: 20px;
        letter-spacing: 3px;
    }

    .app-title-container {
        text-align: center;
        margin-top: -10px;
        margin-bottom: 35px;
        width: 100%;
    }

    .app-title {
        font-family: 'Cinzel', serif !important;
        font-size: 4rem !important;
        font-weight: 400;
        letter-spacing: 14px;
        color: #C71585 !important;
        text-transform: uppercase;
    }

    /* Typewriter Paper Text Area Inputs - Perfectly aligned with output */
    textarea {
        font-family: 'Anonymous Pro', monospace !important;
        background-color: #FFF9FA !important;
        border: 2px solid #FF69B4 !important;
        color: #C71585 !important;
        font-size: 1rem !important;
        border-radius: 10px;
        margin-top: 0px !important;
    }

    /* Typewriter Paper Auto-Expanding Outputs - Perfectly aligned with input */
    .dynamic-output-box {
        font-family: 'Anonymous Pro', monospace !important;
        background-color: #FFF9FA !important;
        border: 2px solid #FF69B4 !important;
        color: #C71585 !important;
        font-size: 1rem !important;
        border-radius: 10px;
        padding: 10px 14px;
        min-height: 430px;
        max-height: 430px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-all;
        margin-top: 0px !important;
    }

    /* Enforce deep pink label coloring across all core sliders and text fields */
    [data-testid="stWidgetLabel"] p, label p, p, span {
        color: #C71585 !important;
        font-weight: 700 !important;
    }

    hr {
        border-color: #FF69B4 !important;
        opacity: 0.5;
    }

    /* Heart shape avatar styling container */
    .avatar-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        margin-top: 25px;
        justify-items: center;
    }

    .heart-avatar-container {
        position: relative;
        width: 80px;
        height: 80px;
        background-color: #FF69B4;
        clip-path: url(#heart-path);
    }

    .heart-avatar-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* Placeholder design until jpegs arrive */
    .heart-placeholder {
        width: 100%;
        height: 100%;
        background-color: #FFB6C1;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFF;
        font-weight: bold;
        font-size: 0.8rem;
    }
    </style>

    <svg width="0" height="0">
      <defs>
        <clipPath id="heart-path" clipPathUnits="objectBoundingBox">
          <path d="M 0.5, 0.24 C 0.45, 0.06, 0.25, 0, 0.1, 0.15 C -0.05, 0.3, 0, 0.6, 0.5, 0.95 C 1, 0.6, 1.05, 0.3, 0.9, 0.15 C 0.75, 0, 0.55, 0.06, 0.5, 0.24 Z" />
        </clipPath>
      </defs>
    </svg>
    """,
    unsafe_allow_html=True
)

# --- APP HEADER ---
st.markdown(
    """
    <div class="app-title-container">
        <div class="app-title">Cipherish</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- ALGORITHMS ---
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


# --- 3-COLUMN STRUCTURE ---
col1, col2, col3 = st.columns([1.2, 2.2, 1.2], gap="large")

# --- COLUMN 1: ADJUSTMENTS PANEL ---
with col1:
    with st.container(border=True):
        st.markdown('<div class="panel-title">ADJUSTMENTS</div>', unsafe_allow_html=True)
        
        mode = st.radio("Select Mode:", ("Encode", "Decode"), horizontal=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        shift_value = st.slider("Shift Amount:", min_value=1, max_value=15, value=5, step=1)
        block_size = st.slider("Block Size:", min_value=2, max_value=10, value=4, step=1)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        enable_reversal = st.checkbox("Word Reversal", value=False)
        enable_numbers = st.checkbox("Number Layers", value=False)

# --- COLUMN 2: THE OPEN BOOK (INPUT / OUTPUT) ---
with col2:
    page_left, page_right = st.columns(2, gap="medium")
    
    with page_left:
        # label set to empty string to keep page top completely clean and aligned
        input_text = st.text_area(
            label="",
            placeholder="After selecting your desired encoding adjustments from the menu on the left, you can type in your message here...",
            height=430
        )
        
    with page_right:
        # Added a tiny spacer to push the output wrapper exactly to the same top level as text_area
        st.markdown('<div style="margin-top: 13px;"></div>', unsafe_allow_html=True)
        if input_text:
            if mode == "Encode":
                result = cipher_encoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
            else:
                result = cipher_decoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
            
            st.markdown(f'<div class="dynamic-output-box">{result}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="dynamic-output-box" style="color: rgba(199, 21, 133, 0.5);">The output will be here...</div>', unsafe_allow_html=True)

# --- COLUMN 3: INTRO TEXT & HEART AVATARS PANEL ---
with col3:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align: left; margin-top: 5px;">
                <p>Hi!! We created this tool for our <b>Ling360</b> final project.</p>
                <p>You can type in your message below and we will encode it for you.</p>
                <p>Your secret is safe with us &lt;3</p>
            </div>
            
            <div class="avatar-grid">
                <div class="heart-avatar-container">
                    <div class="heart-placeholder">✨</div>
                </div>
                <div class="heart-avatar-container">
                    <div class="heart-placeholder">✨</div>
                </div>
                <div class="heart-avatar-container">
                    <div class="heart-placeholder">✨</div>
                </div>
                <div class="heart-avatar-container">
                    <div class="heart-placeholder">✨</div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
