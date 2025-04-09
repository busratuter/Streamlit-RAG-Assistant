from together import Together

from src.config.settings import TOGETHER_API_KEY

class LLMManager:
    """LLM modeli ve etkileşimlerini yöneten sınıf"""
    
    def __init__(self):
        """LLM istemcisini başlat"""
        if not TOGETHER_API_KEY:
            raise ValueError("TOGETHER_API_KEY bulunamadı! Lütfen .env dosyasına API anahtarınızı ekleyin.")
        
        self.client = Together(api_key=TOGETHER_API_KEY)
    
    def get_response(self, messages, model):
        """LLM'den yanıt al"""
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        return response.choices[0].message.content
    
    def prepare_messages(self, user_messages, context=None):
        """Kullanıcı mesajlarını ve bağlamı birleştirerek LLM için mesaj formatını hazırla"""
        system_prompt = """
        Sen yardımcı bir yapay zeka asistanısın. Kullanıcıların sorularını en iyi şekilde yanıtlamak için:
        
        1. Eğer sorular PDF belgeleri hakkındaysa ve belge içeriği verilmişse, öncelikle bu belge içeriğini kullanarak yanıt ver.
        2. Eğer belgelerde bulunan içerik soruyu tam olarak yanıtlamıyorsa veya belge içeriği yoksa, kendi genel bilgi tabanını kullanarak yanıtla.
        3. Belge içeriğiyle genel bilgini birleştirerek kapsamlı yanıtlar oluşturabilirsin.
        
        Belge içeriği verildiyse, bunu açıkça belirt: "Belgelerinize göre..." şeklinde başlayarak kullanıcıya hangi bilginin belgelerden geldiğini bildir.
        
        Belgelerde bilgi bulamadığında: "Belgelerinizde bu konuda spesifik bilgi bulamadım, ancak genel olarak..." şeklinde açıkla.
        
        Her zaman doğru, yardımcı ve bilgilendirici yanıtlar ver.
        """

        formatted_messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        if context:
            formatted_messages.append({
                "role": "system", 
                "content": f"Belge İçeriği:\n{context}"
            })
        
        # Kullanıcı ve asistan mesajlarını ekle
        for m in user_messages:
            if m["role"] == "user" or m["role"] == "assistant":
                formatted_messages.append(m)
        
        return formatted_messages 