"""
DeepSeek AI API ইন্টিগ্রেশন
"""

import requests
import json
import os
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class DeepSeekHandler:
    """DeepSeek API হ্যান্ডলার"""
    
    def __init__(self, api_key: str = None):
        """
        DeepSeek হ্যান্ডলার ইনিশিয়ালাইজ
        
        Args:
            api_key: DeepSeek API key (ঐচ্ছিক, .env থেকে নেবে)
        """
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        self.base_url = "https://api.deepseek.com"
        
        if not self.api_key:
            raise ValueError("DeepSeek API key not found. Set DEEPSEEK_API_KEY in .env")
        
        # ডিফল্ট কনফিগ
        self.default_config = {
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 2000,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": False
        }
        
        logger.info("DeepSeek handler initialized")
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       config: Optional[Dict] = None) -> Dict:
        """
        Chat completion API কল
        
        Args:
            messages: মেসেজ লিস্ট [{"role": "user", "content": "Hello"}]
            config: কাস্টম কনফিগারেশন
            
        Returns:
            API রেস্পন্স
        """
        try:
            # কনফিগ মার্জ
            final_config = {**self.default_config, **(config or {})}
            
            # API রিকোয়েস্ট প্রিপেয়ার
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": messages,
                **final_config
            }
            
            # API কল
            response = requests.post(
                url, 
                headers=headers, 
                json=payload,
                timeout=30
            )
            
            # রেস্পন্স চেক
            response.raise_for_status()
            data = response.json()
            
            # রেস্পন্স প্রসেস
            result = {
                "success": True,
                "content": data["choices"][0]["message"]["content"],
                "model": data["model"],
                "usage": data.get("usage", {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }),
                "finish_reason": data["choices"][0]["finish_reason"]
            }
            
            logger.info(f"DeepSeek API call successful: {result['usage']['total_tokens']} tokens")
            return result
            
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else 0
            
            if status_code == 401:
                error_msg = "Authentication failed. Check API key."
                error_code = "AUTH_ERROR"
            elif status_code == 429:
                error_msg = "Rate limit exceeded. Please try again later."
                error_code = "RATE_LIMIT"
            elif status_code == 402:
                error_msg = "Insufficient credits. Please top up your account."
                error_code = "INSUFFICIENT_CREDITS"
            else:
                error_msg = f"HTTP error: {str(e)}"
                error_code = "HTTP_ERROR"
            
            logger.error(f"DeepSeek HTTP error: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "code": error_code
            }
            
        except requests.exceptions.Timeout:
            error_msg = "Request timeout. Please try again."
            logger.error(f"DeepSeek timeout error")
            return {
                "success": False,
                "error": error_msg,
                "code": "TIMEOUT"
            }
            
        except requests.exceptions.ConnectionError:
            error_msg = "Connection error. Check your internet connection."
            logger.error(f"DeepSeek connection error")
            return {
                "success": False,
                "error": error_msg,
                "code": "CONNECTION_ERROR"
            }
            
        except Exception as e:
            logger.error(f"DeepSeek unexpected error: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "code": "UNKNOWN_ERROR"
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
        # মেসেজ প্রিপেয়ার
        system_message = """তুমি YOUR CRUSH AI BOT, একটি বাংলা-ইংরেজি AI সহকারী।
তোমার ব্যক্তিত্ব: বন্ধুত্বপূর্ণ, রোমান্টিক, সহায়ক।
তুমি বাংলা এবং ইংরেজি উভয় ভাষায় উত্তর দিতে পারো।"""
        
        if context:
            system_message += f"\n\nContext: {context}"
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        # API কল
        result = self.chat_completion(messages, config)
        
        if result["success"]:
            return result["content"]
        else:
            return f"Error: {result['error']}"
    
    def stream_response(self, 
                       prompt: str, 
                       callback) -> None:
        """
        স্ট্রিমিং রেস্পন্স
        
        Args:
            prompt: ইউজার প্রশ্ন
            callback: প্রতিটি চাংকের জন্য কলব্যাক ফাংশন
        """
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            
            url = f"{self.base_url}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": messages,
                "model": "deepseek-chat",
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": True
            }
            
            # স্ট্রিমিং রেস্পন্স
            with requests.post(url, headers=headers, json=payload, stream=True, timeout=30) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = line[6:]
                            if data != '[DONE]':
                                try:
                                    chunk = json.loads(data)
                                    if 'choices' in chunk and chunk['choices']:
                                        delta = chunk['choices'][0].get('delta', {})
                                        if 'content' in delta:
                                            callback(delta['content'])
                                except json.JSONDecodeError:
                                    continue
                                    
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            callback(f"Error: {str(e)}")
    
    def get_models(self) -> List[str]:
        """উপলব্ধ মডেলের লিস্ট পান"""
        try:
            url = f"{self.base_url}/models"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return [model["id"] for model in data.get("data", [])]
            
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            return ["deepseek-chat", "deepseek-coder"]
    
    def calculate_cost(self, tokens: int, model: str = "deepseek-chat") -> float:
        """
        টোকেন সংখ্যা থেকে খরচ ক্যালকুলেট করুন
        
        Args:
            tokens: টোকেন সংখ্যা
            model: মডেল নাম
            
        Returns:
            খরচ (USD)
        """
        # DeepSeek খরচ (প্রতি 1M টোকেন)
        # Input: $0.14 per 1M tokens
        # Output: $0.28 per 1M tokens
        # First 1M tokens free (প্রোমো)
        
        if model == "deepseek-chat":
            cost_per_1M_tokens = 0.28  # Output cost
        else:
            cost_per_1M_tokens = 0.50  # Default for other models
        
        cost = (tokens / 1000000) * cost_per_1M_tokens
        
        return round(cost, 6)
    
    def get_credits(self) -> Optional[Dict]:
        """
        রিমেইনিং ক্রেডিট তথ্য পান
        
        Returns:
            ক্রেডিট তথ্য বা None
        """
        try:
            url = f"{self.base_url}/billing/credit"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting credits: {e}")
            return None

# Singleton instance
_deepseek_instance = None

def get_deepseek_handler(api_key: str = None) -> DeepSeekHandler:
    """DeepSeek হ্যান্ডলার ইনস্ট্যান্স পান"""
    global _deepseek_instance
    
    if _deepseek_instance is None:
        _deepseek_instance = DeepSeekHandler(api_key)
    
    return _deepseek_instance

# ইউটিলিটি ফাংশন
def is_deepseek_available() -> bool:
    """DeepSeek API উপলব্ধ কিনা চেক করুন"""
    try:
        api_key = os.getenv('DEEPSEEK_API_KEY')
        return bool(api_key and len(api_key) > 20)
    except:
        return False

def test_deepseek_connection() -> bool:
    """DeepSeek কানেকশন টেস্ট"""
    try:
        handler = get_deepseek_handler()
        response = handler.generate_response("Hello")
        return "Error:" not in response
    except:
        return False

if __name__ == "__main__":
    # টেস্ট কোড
    if is_deepseek_available():
        print("✅ DeepSeek API available")
        
        handler = get_deepseek_handler()
        
        # টেস্ট রেস্পন্স
        response = handler.generate_response("হ্যালো, কেমন আছো?")
        print(f"Response: {response}")
        
        # টেস্ট মডেলস
        models = handler.get_models()
        print(f"Available models: {models}")
        
        # টেস্ট ক্রেডিট
        credits = handler.get_credits()
        if credits:
            print(f"Credits: {credits}")
        
        # টেস্ট কস্ট ক্যালকুলেশন
        cost = handler.calculate_cost(1000, "deepseek-chat")
        print(f"Cost for 1000 tokens: ${cost}")
        
    else:
        print("❌ DeepSeek API not available. Set DEEPSEEK_API_KEY in .env")