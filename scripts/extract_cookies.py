#!/usr/bin/env python3
"""
🍪 Facebook Cookie Extraction Script
"""

import os
import sys
import json
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validator import Validator

def extract_cookies_from_browser(browser="chrome"):
    """Extract cookies from browser"""
    try:
        import browser_cookie3
        
        print(f"🔍 Extracting cookies from {browser}...")
        
        # Extract cookies based on browser
        if browser.lower() == "chrome":
            cj = browser_cookie3.chrome(domain_name='facebook.com')
        elif browser.lower() == "firefox":
            cj = browser_cookie3.firefox(domain_name='facebook.com')
        elif browser.lower() == "edge":
            cj = browser_cookie3.edge(domain_name='facebook.com')
        elif browser.lower() == "opera":
            cj = browser_cookie3.opera(domain_name='facebook.com')
        elif browser.lower() == "brave":
            cj = browser_cookie3.brave(domain_name='facebook.com')
        else:
            return None, f"Unsupported browser: {browser}"
        
        # Process cookies
        cookies_list = []
        for cookie in cj:
            if 'facebook.com' in cookie.domain:
                cookie_dict = {
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path,
                    'expires': cookie.expires if hasattr(cookie, 'expires') else None,
                    'secure': cookie.secure if hasattr(cookie, 'secure') else False,
                    'httpOnly': getattr(cookie, 'has_nonstandard_attr', lambda x: False)('HttpOnly'),
                    'extracted_at': datetime.now().isoformat(),
                    'browser': browser
                }
                cookies_list.append(cookie_dict)
        
        return cookies_list, None
        
    except ImportError:
        return None, "browser_cookie3 not installed. Run: pip install browser_cookie3"
    except Exception as e:
        return None, f"Error extracting cookies: {e}"

def save_cookies(cookies, output_file="data/cookies/master_cookies.json", encrypt=False):
    """Save cookies to file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Prepare cookie data
        cookie_data = {
            "metadata": {
                "extracted_at": datetime.now().isoformat(),
                "total_cookies": len(cookies),
                "browser": cookies[0]["browser"] if cookies else "unknown",
                "encrypted": encrypt
            },
            "cookies": cookies
        }
        
        # Encrypt if requested
        if encrypt:
            try:
                from utils.encryption import Encryption
                enc = Encryption()
                encrypted_data = enc.encrypt_data(cookie_data)
                cookie_data = {"encrypted": True, "data": encrypted_data}
            except:
                print("⚠️ Encryption failed, saving plain text")
                encrypt = False
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, indent=2, ensure_ascii=False)
        
        # Create backup
        backup_file = f"data/cookies/backup_{int(time.time())}.json"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(cookie_data, f, indent=2, ensure_ascii=False)
        
        return True, f"Saved {len(cookies)} cookies to {output_file}"
        
    except Exception as e:
        return False, f"Error saving cookies: {e}"

def check_cookie_health(cookies):
    """Check cookie health and validity"""
    if not cookies:
        return False, "No cookies to check"
    
    # Essential Facebook cookies
    essential_cookies = ['c_user', 'xs', 'fr', 'datr']
    found_cookies = [c['name'] for c in cookies]
    
    missing = [c for c in essential_cookies if c not in found_cookies]
    
    if missing:
        return False, f"Missing essential cookies: {missing}"
    
    # Check expiration
    current_time = time.time()
    expired_cookies = []
    
    for cookie in cookies:
        if cookie.get('expires'):
            if cookie['expires'] < current_time:
                expired_cookies.append(cookie['name'])
    
    if expired_cookies:
        return False, f"Expired cookies: {expired_cookies[:3]}"
    
    return True, f"✅ All essential cookies present ({len(cookies)} total)"

def test_cookies(cookies):
    """Test cookies by making a request to Facebook"""
    try:
        import requests
        
        # Convert to requests cookie format
        cookie_dict = {c['name']: c['value'] for c in cookies}
        
        # Make test request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(
            'https://www.facebook.com/me',
            cookies=cookie_dict,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            if 'login' in response.url or 'Log In' in response.text:
                return False, "Cookies not working (redirected to login)"
            return True, "✅ Cookies working (logged in)"
        else:
            return False, f"HTTP {response.status_code}: {response.reason}"
            
    except Exception as e:
        return False, f"Test failed: {e}"

def main():
    """Main function"""
    print("\n" + "="*60)
    print("🍪 FACEBOOK COOKIE EXTRACTION TOOL")
    print("="*60)
    print("\n⚠️ IMPORTANT: You must be logged into Facebook in your browser!")
    
    # Browser selection
    print("\nSelect browser to extract cookies from:")
    print("1. Chrome (Recommended)")
    print("2. Firefox")
    print("3. Edge")
    print("4. Opera")
    print("5. Brave")
    print("6. Try all browsers")
    
    try:
        choice = input("\nEnter choice (1-6): ").strip()
        
        browsers = {
            '1': 'chrome',
            '2': 'firefox',
            '3': 'edge',
            '4': 'opera',
            '5': 'brave'
        }
        
        if choice == '6':
            # Try all browsers
            for browser_name in ['chrome', 'firefox', 'edge', 'opera', 'brave']:
                print(f"\nTrying {browser_name}...")
                cookies, error = extract_cookies_from_browser(browser_name)
                
                if cookies and len(cookies) > 0:
                    print(f"✅ Found {len(cookies)} cookies in {browser_name}")
                    break
                else:
                    print(f"❌ No cookies in {browser_name}")
        else:
            browser = browsers.get(choice, 'chrome')
            cookies, error = extract_cookies_from_browser(browser)
            
            if error:
                print(f"\n❌ Error: {error}")
                return
        
        if not cookies:
            print("\n❌ No Facebook cookies found!")
            print("Make sure:")
            print("1. You're logged into Facebook in your browser")
            print("2. The browser is not in private/incognito mode")
            print("3. You have necessary permissions")
            return
        
        print(f"\n✅ Successfully extracted {len(cookies)} cookies")
        
        # Check cookie health
        is_healthy, health_msg = check_cookie_health(cookies)
        print(f"\n🔍 Cookie Health: {health_msg}")
        
        # Ask to test cookies
        test = input("\nTest cookies now? (y/n): ").lower()
        if test == 'y':
            print("\nTesting cookies...")
            is_working, test_msg = test_cookies(cookies)
            print(f"🧪 Test Result: {test_msg}")
        
        # Ask to save
        save = input("\nSave cookies? (y/n): ").lower()
        if save == 'y':
            encrypt = input("Encrypt cookies? (y/n): ").lower() == 'y'
            
            success, message = save_cookies(cookies, encrypt=encrypt)
            if success:
                print(f"\n✅ {message}")
                print(f"📁 Location: data/cookies/master_cookies.json")
                
                # Show cookie details
                print(f"\n📋 Cookie Details:")
                print(f"  Total: {len(cookies)}")
                essential = ['c_user', 'xs', 'fr', 'datr']
                for cookie in essential:
                    found = any(c['name'] == cookie for c in cookies)
                    print(f"  {cookie}: {'✅ Found' if found else '❌ Missing'}")
                
                # Create health report
                health_report = {
                    "checked_at": datetime.now().isoformat(),
                    "total_cookies": len(cookies),
                    "health_status": "healthy" if is_healthy else "unhealthy",
                    "health_message": health_msg,
                    "essential_cookies": {cookie: any(c['name'] == cookie for c in cookies) for cookie in essential}
                }
                
                health_file = "data/cookies/cookie_health.txt"
                with open(health_file, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(health_report, indent=2, ensure_ascii=False))
                
                print(f"\n📝 Health report saved to: {health_file}")
            else:
                print(f"\n❌ {message}")
        else:
            print("\n⚠️ Cookies not saved")
    
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()