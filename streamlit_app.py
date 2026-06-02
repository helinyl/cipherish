import streamlit as st

# ayarlar
st.set_page_config(page_title="Cipherish App", page_icon="🔑", layout="wide")

# visuals
st.markdown(
    """
    <style>
    /* background */
    .stApp {
        background-color: #FFF0F5 !important;
    }
    
    /* title */
    h1 {
        font-family: 'Georgia', 'Times New Roman', serif !important;
        font-weight: 400 !important;
        letter-spacing: 4px !important;
        color: #C71585 !important;
    }
    
    /* subtitles */
    h2, h3, .stSubheader {
        font-family: 'Georgia', 'Times New Roman', serif !important;
        color: #C71585 !important;
    }
    
    /* text */
    .stApp, p, label, textarea {
        font-family: 'Courier New', Courier, monospace !important;
        color: #C71585 !important;
    }
    
    /* input text */
    textarea {
        color: #C71585 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# title
st.title("CIPHERISH")
st.write("Welcome! From the left side of the page you can change your settings. Then you can type your text in the input box and Cipherish will encode/decode it for you <3")
st.markdown("---")

# colab kodumuz
alphabet = "abcçdefgğhıijklmnoöpqrsştuüvwxyz"

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


# columns
col2, col3 = st.columns([3.5, 1.5], gap="medium")

# adjustments column
with col2:
    # PIN and Mode components are placed neatly side-by-side right above the input box
    settings_left, settings_right = st.columns(2, gap="small")
    
    with settings_left:
        mode = st.radio("Select Mode:", ("Encode", "Decode"), horizontal=True)
        
    with settings_right:
        pin = st.text_input("Enter 4-digit PIN (You can't use 0) :", value="X-X-X-X", max_chars=4)
    
    st.markdown("---")
    
    # parsing the pin elements (same as colab notebook logic)
    if len(pin) == 4 and pin.isdigit():
        shift_value = int(pin[0])
        block_size = int(pin[1])
        
        # reversal logic
        if int(pin[2]) % 2 == 0:
            enable_reversal = True
        else:
            enable_reversal = False
            
        # numbers logic
        if int(pin[3]) % 2 == 0:
            enable_numbers = True
        else:
            enable_numbers = False
    else:
        # standard fallback values if pin is incomplete or invalid
        shift_value = 5
        block_size = 4
        enable_reversal = False
        enable_numbers = False
        st.caption("Please enter your 4-Digit PIN. Pick your numbers between 1-9, you can't use 0.")

# input and output boxes
with col2:
    page_left, page_right = st.columns(2, gap="small")
    
    with page_left:
        with st.container(border=True):
            st.markdown("**Input:**")
            input_text = st.text_area(
                label="input_field",
                placeholder="Type your message here...",
                height=350,
                label_visibility="collapsed"
            )
        
    with page_right:
        with st.container(border=True):
            st.markdown("**Output:**")
            
            if input_text:
                if mode == "Encode":
                    result = cipher_encoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
                else:
                    result = cipher_decoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
                
                st.info(result)
            else:
                st.caption("The output will appear here...")

# get to know us
with col3:
    with st.expander("📷 ABOUT US", expanded=True):
        st.image("zphoto.png", use_container_width=True)
        
        st.info("We are four Linguistics students from Boğaziçi University. We created this tool for Ümit Atlamaz's **Ling360** class as our final project. Our goal was to help people create and receive secret messages. We hope you have fun with it!!")
