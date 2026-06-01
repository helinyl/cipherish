import streamlit as st

# Force wide layout to fit the 3-column mock-up beautifully
st.set_page_config(page_title="Cipherish App", page_icon="⚿", layout="wide")

# --- CUSTOM CSS FOR THE PINK NOTEBOOK THEME ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght=0,400;0,700;1,400&family=Poppins:wght=300;400;500;600&family=Courier+Prime&display=swap');

    /* Global styling and background color */
    html, body, [class*="css"], label, button, input, textarea {
        font-family: 'Poppins', sans-serif !important;
    }

    .stApp {
        background-color: #FFF0F5 !important; /* Soft blush/lavender pink background */
        color: #C71585 !important; /* Deep pink text */
    }

    /* Target Streamlit's native containers to lock elements inside the borders */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFE4E1 !important; /* Muted pink fill */
        border: 6px solid #FF69B4 !important; /* Thick pink rounded borders */
        border-radius: 30px !important;
        padding: 25px !important;
        color: #C71585 !important;
    }

    /* Keep the center notebook page containers clean without the thick pink panel borders */
    div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
    }

    .panel-title {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.4rem;
        text-align: center;
        color: #FF69B4 !important;
        margin-bottom: 20px;
        letter-spacing: 1.5px;
    }

    /* Main Center Header - CIPHERISH */
    .app-title-container {
        text-align: center;
        margin-top: -10px;
        margin-bottom: 35px;
        width: 100%;
    }

    .app-title {
        font-family: 'Libre Baskerville', serif !important;
        font-size: 4rem;
        font-weight: 400;
        letter-spacing: 12px;
        color: #C71585 !important;
        text-transform: uppercase;
    }

    /* Text areas styled like typewriter paper inside the book */
    textarea {
        font-family: 'Courier Prime', monospace !important;
        background-color: #FFF9FA !important;
        border: 2px solid #FF69B4 !important;
        color: #C71585 !important;
        font-size: 1.05rem !important;
        border-radius: 10px;
    }

    /* Code output block styled like typewriter paper */
    code, .stCodeBlock {
        font-family: 'Courier Prime', monospace !important;
        background-color: #FFF9FA !important;
        border: 2px solid #FF69B4 !important;
        color: #C71585 !important;
        border-radius: 10px;
    }

    /* Style default widget text colors to match themes */
    [data-testid="stWidgetLabel"] p, label p, p, span {
        color: #C71585 !important;
        font-weight: 500 !important;
    }

    hr {
        border-color: #FF69B4 !important;
        opacity: 0.5;
    }
    </style>
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

# --- ALGORITHMS (UNCHANGED) ---
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


# --- 3-COLUMN LAYOUT STRUCTURE ---
col1, col2, col3 = st.columns([1.2, 2.2, 1.2], gap="large")

# --- COLUMN 1: ADJUSTMENTS PANEL ---
with col1:
    # st.container creates a clean block that our CSS targets perfectly to inject the border design
    with st.container():
        st.markdown('<div class="panel-title">AD JUSTMENTS</div>', unsafe_allow_html=True) 
        
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
        input_text = st.text_area(
            label="📖 Input Page:",
            placeholder="After selecting your desired encoding adjustments from the menu on the left, you can type in your message here...", 
            height=430
        )
        
    with page_right:
        st.markdown("<p style='margin-bottom: 8px; font-weight: 500;'>📝 Output Page:</p>", unsafe_allow_html=True)
        if input_text:
            if mode == "Encode":
                result = cipher_encoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
            else:
                result = cipher_decoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
            st.code(result, language="text")
        else:
            st.info("The output will be here...") 

# --- COLUMN 3: WHO ARE WE PANEL ---
with col3:
    with st.container():
        st.markdown('<div class="panel-title">WHO ARE WE?</div>', unsafe_allow_html=True) 
        
        st.markdown(
            """
            <div style="font-size: 1.05rem; line-height: 1.7; text-align: center; margin-top: 10px;">
                <p>Hi!! We created this tool for our <b>Ling360</b> final project.</p>
                <p>You can type in your message below and we will encode it for you.</p>
                <p>Your secret is safe with us &lt;3</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
