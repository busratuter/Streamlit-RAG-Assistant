import streamlit as st

from src.config.settings import DEFAULT_MODEL, DEFAULT_SEARCH_RESULTS, MAX_SEARCH_RESULTS

def setup_page_config(title, icon, layout="wide"):
    """Sayfa yapılandırmasını ayarla"""
    st.set_page_config(page_title=title, page_icon=icon, layout=layout)

def render_title(title):
    """Uygulama başlığını göster"""
    st.title(title)

def setup_sidebar():
    """Kenar çubuğu ayarlarını yapılandır"""
    st.sidebar.header("Ayarlar")
    
    # Model seçimi
    model = st.sidebar.selectbox(
        "Model Seçin:",
        [DEFAULT_MODEL]
    )
    
    # PDF'leri yeniden işleme butonu
    if st.sidebar.button("PDF'leri Yeniden İşle"):
        st.session_state.vectorstore = None
        st.session_state.processed_files = set()
    
    # İşlenen PDF'leri göster
    st.sidebar.subheader("İşlenen PDF'ler")
    if "processed_files" in st.session_state and st.session_state.processed_files:
        for file in st.session_state.processed_files:
            st.sidebar.write(f"✅ {file}")
    else:
        st.sidebar.write("Henüz işlenen PDF yok.")
    
    # Sonuç sayısı kaydırıcısı
    n_results = st.sidebar.slider(
        "Gösterilecek Sonuç Sayısı", 
        1, 
        MAX_SEARCH_RESULTS, 
        DEFAULT_SEARCH_RESULTS
    )
    
    return model, n_results

def initialize_session_state():
    """Oturum durumlarını başlat"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
        
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

def render_chat_history():
    """Sohbet geçmişini görüntüle"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def render_search_results(results):
    """Arama sonuçlarını expander içerisinde göster"""
    with st.expander("Bulunan İlgili İçerikler"):
        for i, (doc, score) in enumerate(results):
            st.write(f"**Parça {i+1}** (Sayfa {doc.metadata.get('page', 'Bilinmiyor')})")
            st.write(f"Kaynak: {doc.metadata.get('source', 'Bilinmiyor')}")
            st.write(f"Benzerlik Skoru: {score:.4f}")
            st.markdown(doc.page_content)
            st.divider() 