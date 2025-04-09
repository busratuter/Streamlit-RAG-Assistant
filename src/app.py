"""
Ana sohbet uygulaması
"""
import streamlit as st

from src.config.settings import APP_TITLE, APP_ICON
from src.ui.components import (
    setup_page_config,
    render_title,
    setup_sidebar,
    initialize_session_state,
    render_chat_history,
    render_search_results
)
from src.data_processing.pdf_processor import process_pdfs
from src.models.llm import LLMManager

def run_app():
    """Ana uygulamayı başlat"""
    setup_page_config(APP_TITLE, APP_ICON)
    render_title(APP_TITLE)
    
    initialize_session_state()
    
    model, n_results = setup_sidebar()
    
    llm_manager = LLMManager()
    
    if not st.session_state.vectorstore:
        with st.spinner("PDF dosyaları işleniyor..."):
            vectorstore, file_names = process_pdfs()
            st.session_state.vectorstore = vectorstore
            if vectorstore:
                st.success(f"{len(file_names)} PDF dosyası başarıyla işlendi.")
    
    render_chat_history()
    
    prompt = st.chat_input("Soru sor...")
    if prompt:
        # Kullanıcı mesajını ekle ve göster
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Bağlam araması
        context = ""
        if st.session_state.vectorstore:
            with st.spinner("PDF içerikleri aranıyor..."):
                try:
                    # Semantik arama yap
                    results = st.session_state.vectorstore.similarity_search_with_score(prompt, k=n_results)
                    render_search_results(results)
                    context = "\n\n".join([doc.page_content for doc, _ in results])
                    
                except Exception as e:
                    st.error(f"Arama hatası: {str(e)}")
                    context = "PDF içeriklerinde arama yapılamadı."
        else:
            st.warning("İşlenmiş PDF dosyası bulunamadı.")
        
        # Asistan yanıtı
        with st.chat_message("assistant"):
            with st.spinner("Düşünüyorum..."):
                messages = llm_manager.prepare_messages(st.session_state.messages, context)
   
                assistant_response = llm_manager.get_response(messages, model)

                st.markdown(assistant_response)
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_response}) 