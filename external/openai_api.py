"""
OpenAI API ইন্টিগ্রেশন
"""

import openai
import json
import os
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class OpenAIHandler:
    """OpenAI API হ্যান্ডলার"""
    
    def __init__(self, api_key: str = None):
        """
        OpenAI হ্যান্ডলার ইনিশিয়ালাইজ
        
        Args:
            api_key: OpenAI API key (ঐচ্ছিক, .env থেকে নেবে)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # ডিফল্ট কনফিগ
        self.default_config = {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        logger.info("OpenAI handler initialized")
    
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
            
            # API কল
            response = self.client.chat.completions.create(
                messages=messages,
                **final_config
            )
            
            # রেস্পন্স প্রসেস
            result = {
                "success": True,
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "finish_reason": response.choices[0].finish_reason
            }
            
            logger.info(f"OpenAI API call successful: {result['usage']['total_tokens']} tokens")
            return result
            
        except openai.AuthenticationError as e:
            logger.error(f"OpenAI authentication error: {e}")
            return {
                "success": False,
                "error": "Authentication failed. Check API key.",
                "code": "AUTH_ERROR"
            }
            
        except openai.RateLimitError as e:
            logger.error(f"OpenAI rate limit error: {e}")
            return {
                "success": False,
                "error": "Rate limit exceeded. Please try again later.",
                "code": "RATE_LIMIT"
            }
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "success": False,
                "error": f"API error: {str(e)}",
                "code": "API_ERROR"
            }
            
        except Exception as e:
            logger.error(f"OpenAI unexpected error: {e}")
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
            
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    callback(chunk.choices[0].delta.content)
                    
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            callback(f"Error: {str(e)}")
    
    def get_models(self) -> List[str]:
        """উপলব্ধ মডেলের লিস্ট পান"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            logger.error(f"Error fetching models: {e}")
            return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
    
    def calculate_cost(self, tokens: int, model: str = "gpt-3.5-turbo") -> float:
        """
        টোকেন সংখ্যা থেকে খরচ ক্যালকুলেট করুন
        
        Args:
            tokens: টোকেন সংখ্যা
            model: মডেল নাম
            
        Returns:
            খরচ (USD)
        """
        # প্রতি 1K টোকেনের খরচ (USD)
        cost_per_1k = {
            "gpt-3.5-turbo": 0.002,  # $0.002 per 1K tokens
            "gpt-4": 0.03,            # $0.03 per 1K tokens
            "gpt-4-turbo-preview": 0.01,
            "gpt-4-32k": 0.06
        }
        
        base_cost = cost_per_1k.get(model, cost_per_1k["gpt-3.5-turbo"])
        cost = (tokens / 1000) * base_cost
        
        return round(cost, 6)
    
    def moderate_content(self, text: str) -> Dict:
        """
        কন্টেন্ট মডারেশন
        
        Args:
            text: টেক্সট
            
        Returns:
            মডারেশন রেজাল্ট
        """
        try:
            response = self.client.moderations.create(input=text)
            result = response.results[0]
            
            return {
                "flagged": result.flagged,
                "categories": result.categories,
                "category_scores": result.category_scores,
                "safe": not result.flagged
            }
            
        except Exception as e:
            logger.error(f"Moderation error: {e}")
            return {
                "flagged": False,
                "categories": {},
                "category_scores": {},
                "safe": True,
                "error": str(e)
            }

# Singleton instance
_openai_instance = None

def get_openai_handler(api_key: str = None) -> OpenAIHandler:
    """OpenAI হ্যান্ডলার ইনস্ট্যান্স পান"""
    global _openai_instance
    
    if _openai_instance is None:
        _openai_instance = OpenAIHandler(api_key)
    
    return _openai_instance

# ইউটিলিটি ফাংশন
def is_openai_available() -> bool:
    """OpenAI API উপলব্ধ কিনা চেক করুন"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        return bool(api_key and api_key.startswith('sk-'))
    except:
        return False

def test_openai_connection() -> bool:
    """OpenAI কানেকশন টেস্ট"""
    try:
        handler = get_openai_handler()
        response = handler.chat_completion([
            {"role": "user", "content": "Hello"}
        ])
        return response["success"]
    except:
        return False

if __name__ == "__main__":
    # টেস্ট কোড
    if is_openai_available():
        print("✅ OpenAI API available")
        
        handler = get_openai_handler()
        
        # টেস্ট রেস্পন্স
        response = handler.generate_response("হ্যালো, কেমন আছো?")
        print(f"Response: {response}")
        
        # টেস্ট মডেলস
        models = handler.get_models()
        print(f"Available models: {models[:5]}...")
        
        # টেস্ট কস্ট ক্যালকুলেশন
        cost = handler.calculate_cost(1000, "gpt-3.5-turbo")
        print(f"Cost for 1000 tokens: ${cost}")
        
    else:
        print("❌ OpenAI API not available. Set OPENAI_API_KEY in .env")