import streamlit as st

# Sayfa ayarları - Mobilde ve PC'de dengeli durması için centered yaptık
st.set_page_config(page_title="Cipherish App", page_icon="🔑", layout="centered")

# --- FONT VE STİL AYARLARI ---
# Dışarıdan kütüphane eklemeden, tamamen yerel bileşenlerin fontunu Anonymous Pro yapmak için basit bir CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Anonymous+Pro:ital,wght=0,400;0,700;1,400;1,700&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seasons');

    /* Tüm standart Streamlit elementlerinin fontunu Anonymous Pro yapıyoruz */
    html, body, [class*="css"], label, button, input, textarea, p, span, div, small {
        font-family: 'Anonymous Pro', monospace !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- UYGULAMA BAŞLIĞI (The Seasons Fontu ile) ---
st.markdown(
    """
    <h1 style="font-family: 'Seasons', serif; font-weight: bold; letter-spacing: 3px; margin-bottom: 0px;">
        🔑 CIPHERISH
    </h1>
    """, 
    unsafe_allow_html=True
)
st.write("Welcome! We created this tool for our **Ling360** final project. Your secret is safe with us <3")
st.markdown("---")

# --- COLAB KODUNUZ (Algoritma Mantığı) ---
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


# --- SEKMELİ EKRAN DÜZENİ ---
# İstediğin gibi: Sol sekme Ayarlar, Orta ana ekran Şifreleme Kutusu, Sağ sekme Görselimiz
tab_left, tab_center, tab_right = st.tabs(["⚙️ Adjustments", "📝 Cipher Box", "📷 About Us"])

# --- SOL SEKME: AYARLAR PANELİ ---
with tab_left:
    st.subheader("Configure Settings")
    mode = st.radio("Select Mode:", ("Encode", "Decode"), horizontal=True)
    st.markdown("---")
    
    shift_value = st.slider("Shift Amount:", min_value=1, max_value=15, value=5)
    block_size = st.slider("Block Size:", min_value=2, max_value=10, value=4)
    st.markdown("---")
    
    enable_reversal = st.checkbox("Word Reversal", value=False)
    enable_numbers = st.checkbox("Number Layers", value=False)

# --- ORTA SEKME (ANA EKRAN): GİRDİ VE ÇIKTI KUTUSU ---
with tab_center:
    st.subheader("Type & Transform")
    
    # Giriş seviyesine en uygun, mobilde de taşma yapmayan dikey düzen
    input_text = st.text_area(
        label="Input Text:",
        placeholder="Type your message here...",
        height=180
    )
    
    st.markdown("**Output Text:**")
    if input_text:
        if mode == "Encode":
            result = cipher_encoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
        else:
            result = cipher_decoder(input_text, shift_value, block_size, enable_reversal, enable_numbers)
        
        # Tamamen güvenli ve yerel yerleşik çıktı kutusu
        st.info(result)
    else:
        st.caption("The output will appear here after you type something...")

# --- SAĞ SEKME: GÖRSEL VE PROJE BİLGİSİ ---
with tab_right:
    st.subheader("Ling360 Project")
    # Görseli yüklüyoruz, mobil ekran genişliğine otomatik uyum sağlar
    st.image("zphoto.png", use_container_width=True)
    
    st.info("💡 **Tip:** Try combining *Word Reversal* and *Number Layers* for a more complex encryption!")
