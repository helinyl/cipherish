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
st.title("˗ˏˋ ꒰ ✉︎ ꒱ ˎˊ˗CIPHERISH˗ˏˋ ꒰ ✉︎ ꒱ ˎˊ˗")
st.write("Welcome! Please choose a 4-digit PIN, the numbers must be between 1-9, you can't use zero. It is important to remember your PIN as it is the key to your message, you'll need it for both the encoding and decoding. Then you can type out your text in the input box and Cipherish will do the job for you <3")
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

with col2:
    # side-by-side configurations
    settings_left, settings_right = st.columns(2, gap="small")
    mode = settings_left.radio("Select Mode:", ("Encode", "Decode"), horizontal=True)
    pin = settings_right.text_input("Please enter your PIN:", value="1111", max_chars=4)
    st.markdown("---")
    
    # parsing the pin elements
    if len(pin) == 4 and pin.isdigit():
        shift_value = int(pin[0])
        block_size = int(pin[1])
        enable_reversal = int(pin[2]) % 2 == 0
        enable_numbers = int(pin[3]) % 2 == 0
    else:
        shift_value, block_size, enable_reversal, enable_numbers = 5, 4, False, False

    # input and output text areas
    page_left, page_right = st.columns(2, gap="small")
    
    # input box
    page_left.markdown("**Input:**")
    input_text = page_left.text_area(label="input_field", placeholder="Type your message here...", height=350, label_visibility="collapsed")
        
    # output box
    page_right.markdown("**Output:**")
    if input_text:
        if mode == "Encode":
            result = cipher_encoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
        else:
            result = cipher_decoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
        page_right.info(result)
    else:
        page_right.caption("The output will appear here...")

# get to know us
with col3:
    with st.expander("˖°📷༘ Who Are We?", expanded=True):
        st.image("zphoto.png", use_container_width=True)
        st.info("We are four Linguistics students from Boğaziçi University. We created this tool for Ümit Atlamaz's **Ling360** class as our final project. Our goal was to help people **create and read secret messages.** We hope you have fun with it!!")
