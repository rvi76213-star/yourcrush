"""
Google Gemini API ইন্টিগ্রেশন
"""

import google.generativeai as genai
import json
import os
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class GeminiHandler:
    """Gemini API হ্যান্ডলার"""
    
    def __init__(self, api_key: str = None):
        """
        Gemini হ্যান্ডলার ইনিশিয়ালাইজ
        
        Args:
            api_key: Gemini API key (ঐচ্ছিক, .env থেকে নেবে)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY in .env")
        
        genai.configure(api_key=self.api_key)
        
        # ডিফল্ট কনফিগ
        self.default_config = {
            "model": "gemini-pro",
            "temperature": 0.7,
            "max_output_tokens": 1000,
            "top_p": 1.0,
            "top_k": 1
        }
        
        logger.info("Gemini handler initialized")
    
    def generate_content(self, 
                        prompt: str, 
                        config: Optional[Dict] = None) -> Dict:
        """
        কন্টেন্ট জেনারেশন API কল
        
        Args:
            prompt: প্রম্পট টেক্সট
            config: কাস্টম কনফিগারেশন
            
        Returns:
            API রেস্পন্স
        """
        try:
            # কনফিগ মার্জ
            final_config = {**self.default_config, **(config or {})}
            
            # মডেল সিলেক্ট
            model_name = final_config.pop("model")
            model = genai.GenerativeModel(model_name)
            
            # জেনারেশন কনফিগ
            generation_config = genai.types.GenerationConfig(**final_config)
            
            # কন্টেন্ট জেনারেট
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # রেস্পন্স প্রসেস
            result = {
                "success": True,
                "content": response.text,
                "model": model_name,
                "usage": {
                    "candidates_count": len(response.candidates),
                    "finish_reason": response.candidates[0].finish_reason if response.candidates else "UNKNOWN"
                }
            }
            
            logger.info(f"Gemini API call successful")
            return result
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            
            # এরর টাইপ চেক
            error_message = str(e).lower()
            
            if "quota" in error_message:
                error_code = "QUOTA_EXCEEDED"
                error_msg = "API quota exceeded. Please try again later."
            elif "key" in error_message or "auth" in error_message:
                error_code = "AUTH_ERROR"
                error_msg = "Authentication failed. Check API key."
            elif "safety" in error_message:
                error_code = "SAFETY_ERROR"
                error_msg = "Content blocked by safety settings."
            elif "rate" in error_message or "limit" in error_message:
                error_code = "RATE_LIMIT"
                error_msg = "Rate limit exceeded."
            else:
                error_code = "API_ERROR"
                error_msg = f"API error: {str(e)}"
            
            return {
                "success": False,
                "error": error_msg,
                "code": error_code
            }
    
    def generate_response(self, 
                         prompt: str, 
                         context: str = "", 
                         config: Optional[Dict] = None) -> str:
        """
        সহজভাবে রেস্পন্স জেনারেট করুন
        
        Args:
            prompt: ইউজার প্রশ্ন
            context: অতিরিক্ত কনটেক্সট
            config: কাস্টম কনফিগ
            
        Returns:
            AI রেস্পন্স
        """
        # প্রম্পট প্রিপেয়ার
        full_prompt = """তুমি YOUR CRUSH AI BOT, একটি বাংলা-ইংরেজি AI সহকারী।
তোমার ব্যক্তিত্ব: বন্ধুত্বপূর্ণ, রোমান্টিক, সহায়ক।
তুমি বাংলা এবং ইংরেজি উভয় ভাষায় উত্তর দিতে পারো।"""
        
        if context:
            full_prompt += f"\n\nContext: {context}"
        
        full_prompt += f"\n\nUser: {prompt}\nAssistant:"
        
        # API কল
        result = self.generate_content(full_prompt, config)
        
        if result["success"]:
            return result["content"]
        else:
            return f"Error: {result['error']}"
    
    def chat_conversation(self, 
                         messages: List[Dict[str, str]], 
                         config: Optional[Dict] = None) -> str:
        """
        চ্যাট কনভারসেশন (মাল্টি-টার্ন)
        
        Args:
            messages: মেসেজ লিস্ট [{"role": "user", "content": "Hello"}]
            config: কাস্টম কনফিগ
            
        Returns:
            AI রেস্পন্স
        """
        try:
            # কনফিগ মার্জ
            final_config = {**self.default_config, **(config or {})}
            
            # মডেল
            model_name = final_config.pop("model")
            model = genai.GenerativeModel(model_name)
            
            # চ্যাট শুরু
            chat = model.start_chat(history=[])
            
            # মেসেজ প্রসেস
            response = None
            for msg in messages:
                if msg["role"] == "user":
                    response = chat.send_message(msg["content"])
            
            if response:
                return response.text
            else:
                return "No response generated"
                
        except Exception as e:
            logger.error(f"Chat conversation error: {e}")
            return f"Error: {str(e)}"
    
    def get_models(self) -> List[str]:
        """উপলব্ধ মডেলের লিস্ট পান"""
        try:
            models = genai.list_models()
            return [model.name for model in models]
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            return ["gemini-pro", "gemini-pro-vision"]
    
    def calculate_cost(self, characters: int, model: str = "gemini-pro") -> float:
        """
        ক্যারেক্টার সংখ্যা থেকে খরচ ক্যালকুলেট করুন
        
        Args:
            characters: ক্যারেক্টার সংখ্যা
            model: মডেল নাম
            
        Returns:
            খরচ (USD)
        """
        # Gemini Pro এর খরচ (প্রতি 1M ক্যারেক্টার)
        # Input: $0.00025 per 1K characters
        # Output: $0.0005 per 1K characters
        # First 60 requests/minute free
        
        if model == "gemini-pro":
            cost_per_1k_chars = 0.0005  # Output cost
        else:
            cost_per_1k_chars = 0.001  # Default for other models
        
        cost = (characters / 1000) * cost_per_1k_chars
        
        return round(cost, 6)
    
    def moderate_content(self, text: str) -> Dict:
        """
        কন্টেন্ট মডারেশন (Gemini এর সেফটি সেটিংস ব্যবহার)
        
        Args:
            text: টেক্সট
            
        Returns:
            মডারেশন রেজাল্ট
        """
        try:
            # Gemini স্বয়ংক্রিয়ভাবে কন্টেন্ট মডারেট করে
            # আমরা শুধু বেসিক চেক করব
            blocked_keywords = [
                "হত্যা", "আত্মহত্যা", "মাদক", "অশ্লীল",
                "kill", "suicide", "drug", "porn"
            ]
            
            flagged = any(keyword in text.lower() for keyword in blocked_keywords)
            
            return {
                "flagged": flagged,
                "categories": {
                    "violence": "violence" in text.lower(),
                    "adult": any(word in text.lower() for word in ["adult", "porn", "sex"]),
                    "harassment": any(word in text.lower() for word in ["harass", "bully", "threat"])
                },
                "safe": not flagged
            }
            
        except Exception as e:
            logger.error(f"Moderation error: {e}")
            return {
                "flagged": False,
                "categories": {},
                "safe": True,
                "error": str(e)
            }

# Singleton instance
_gemini_instance = None

def get_gemini_handler(api_key: str = None) -> GeminiHandler:
    """Gemini হ্যান্ডলার ইনস্ট্যান্স পান"""
    global _gemini_instance
    
    if _gemini_instance is None:
        _gemini_instance = GeminiHandler(api_key)
    
    return _gemini_instance

# ইউটিলিটি ফাংশন
def is_gemini_available() -> bool:
    """Gemini API উপলব্ধ কিনা চেক করুন"""
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        return bool(api_key and len(api_key) > 20)
    except:
        return False

def test_gemini_connection() -> bool:
    """Gemini কানেকশন টেস্ট"""
    try:
        handler = get_gemini_handler()
        response = handler.generate_content("Hello")
        return response["success"]
    except:
        return False

if __name__ == "__main__":
    # টেস্ট কোড
    if is_gemini_available():
        print("✅ Gemini API available")
        
        handler = get_gemini_handler()
        
        # টেস্ট রেস্পন্স
        response = handler.generate_response("হ্যালো, কেমন আছো?")
        print(f"Response: {response}")
        
        # টেস্ট মডেলস
        models = handler.get_models()
        print(f"Available models: {models[:5]}...")
        
        # টেস্ট কস্ট ক্যালকুলেশন
        cost = handler.calculate_cost(1000, "gemini-pro")
        print(f"Cost for 1000 characters: ${cost}")
        
    else:
        print("❌ Gemini API not available. Set GEMINI_API_KEY in .env")