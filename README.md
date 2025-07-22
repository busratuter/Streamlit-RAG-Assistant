# Streamlit RAG Asistanı

Bu proje, Streamlit tabanlı RAG asistanıdır. PDF dosyalarını yüklemenize, içeriklerini işlemenize ve belgelerle ilgili sorular sormanıza olanak tanır. Asistan, PDF'lerden alınan bilgilere dayanarak yanıtlar üretmek için bir LLM kullanır.

## Teknik Detaylar

-   **Vektör Veritabanı (Vector Database):** Dokümanların anlamsal içeriğini depolamak ve verimli bir şekilde aramak için **ChromaDB** kullanılmaktadır. Kullanıcının sorgusuyla en alakalı metin parçalarını bulmak için vektör gömülmeleri (vector embeddings) üzerinde benzerlik araması yapar.
-   **RAG Pipeline:** **LangChain** kütüphanesi, PDF işleme, metin bölme (text splitting), gömülme (embedding) oluşturma ve LLM ile etkileşim gibi RAG akışının temel adımlarını yönetmek için kullanılır.
-   **Kullanıcı Arayüzü (UI):** Arayüz, hızla etkileşimli veri uygulamaları oluşturmak için popüler bir Python kütüphanesi olan **Streamlit** ile geliştirilmiştir.
-   **Dil Modeli (LLM):** Yanıtların üretilmesi için **Together AI** tarafından sağlanan bir dil modeli entegre edilmiştir.

## Özellikler

-   **PDF İşleme**: İşlenmek ve dizine eklenmek üzere bir veya daha fazla PDF dosyası yükleyin.
-   **Anlamsal Arama**: Soruları doğal dilde sorun ve belgelerden ilgili bağlamı alın.
-   **Sohbet Yapay Zekası**: PDF içeriğine dayalı olarak sorularınızı yanıtlayan bir yapay zeka asistanı ile etkileşim kurun.
-   **Kaynak Gösterimi**: Yanıtı oluşturmak için kullanılan PDF kaynaklarını görüntüleyin.

## Başlarken

### Gereksinimler

-   Python 3.8+
-   [Together AI](https://www.together.ai/) veya başka bir LLM sağlayıcısından bir API anahtarı.

### Kurulum

1.  **Depoyu klonlayın:**
    ```bash
    git clone https://github.com/kullanici-adiniz/Streamlit-RAG-Assistant.git
    cd Streamlit-RAG-Assistant
    ```
    *Not: `kullanici-adiniz` kısmını kendi GitHub kullanıcı adınızla güncellemeyi unutmayın.*

2.  **Sanal bir ortam oluşturun ve etkinleştirin:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # Windows'ta `venv\Scripts\activate` komutunu kullanın.
    ```

3.  **Bağımlılıkları yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ortam değişkenlerinizi ayarlayın:**

    Projenin kök dizininde `.env` adında bir dosya oluşturun ve Together AI API anahtarınızı ekleyin:
    ```
    TOGETHER_API_KEY="api_anahtariniz_buraya_gelecek"
    ```

### Uygulamayı Çalıştırma

1.  **PDF dosyalarınızı** `files` klasörüne yerleştirin.

2.  **Streamlit uygulamasını çalıştırın:**
    ```bash
    streamlit run src/main.py
    ```

3.  Web tarayıcınızı açın ve `http://localhost:8501` adresine gidin.


``` 