import streamlit as st

# ayarlar
st.set_page_config(page_title="Cipherish App", page_icon="🔑", layout="wide")

# başlık
# Karmaşık HTML div'leri yerine Streamlit'in kendi başlık fonksiyonu
st.title("🔑 CIPHERISH")
st.write("Welcome! We created this tool for our **Ling360** final project. Your secret is safe with us <3")
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


# sayfa sütunları
col1, col2, col3 = st.columns([1.5, 2.5, 1.5], gap="medium")

# ayarlar sütunu
with col1:
    with st.container(border=True):
        st.subheader("ADJUSTMENTS")
        
        mode = st.radio("Select Mode:", ("Encode", "Decode"), horizontal=True)
        st.markdown("---")
        
        shift_value = st.slider("Shift Amount:", min_value=1, max_value=15, value=5)
        block_size = st.slider("Block Size:", min_value=2, max_value=10, value=4)
        st.markdown("---")
        
        enable_reversal = st.checkbox("Word Reversal", value=False)
        enable_numbers = st.checkbox("Number Layers", value=False)

# input ve output kutusu
with col2:
    page_left, page_right = st.columns(2, gap="small")
    
    with page_left:
        with st.container(border=True):
            st.markdown("**Input Text:**")
            input_text = st.text_area(
                label="input_field",
                placeholder="Type your message here...",
                height=350,
                label_visibility="collapsed"
            )
        
    with page_right:
        with st.container(border=True):
            st.markdown("**Output Text:**")
            
            # Algoritmayı çalıştırıp doğrudan Streamlit kutusunda gösteriyoruz
            if input_text:
                if mode == "Encode":
                    result = cipher_encoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
                else:
                    result = cipher_decoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
                
                # Başlangıç seviyesine uygun, tertemiz bir native çıktı alanı
                st.info(result)
            else:
                st.caption("The output will appear here...")

# bizi tanıyın
with col3:
    with st.container(border=True):
        # Görseli yüklüyoruz
        st.image("zphoto.png", use_container_width=True)
        
        st.info("💡 **Tip:** Try combining *Word Reversal* and *Number Layers* for a more complex encryption!")
