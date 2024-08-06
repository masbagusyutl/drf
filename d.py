import time
import requests
from datetime import datetime, timedelta
import re

# Fungsi untuk membaca data dari file
def read_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        accounts = []
        for i in range(0, len(lines), 2):
            token = lines[i].strip()
            cookie = lines[i+1].strip()
            accounts.append((token, cookie))
    return accounts

# Fungsi untuk login akun
def login_account(token, cookie):
    url = "https://drftparty.fibrum.com/auth"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Cookie": cookie,
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://drftparty.fibrum.com/game",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Token": token
    }
    
    response = requests.get(url, headers=headers)
    return response.status_code

# Fungsi untuk mendapatkan informasi akun
def info_account(token, cookie):
    url = "https://drftparty.fibrum.com/get-user"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Cookie": cookie,
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://drftparty.fibrum.com/game",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Token": token
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_text = response.text
        print(f"Respons: {response_text}")
        
        # Cari informasi akun menggunakan regex
        user_nick = re.search(r'"user_nick":"(.*?)"', response_text)
        total_drft_claims = re.search(r'"total_drft_claims":(\d+)', response_text)
        total_daily_claims = re.search(r'"total_daily_claims":(\d+)', response_text)
        drft = re.search(r'"drft":"(.*?)"', response_text)

        print("Informasi Akun:")
        print(f"Username: {user_nick.group(1) if user_nick else 'N/A'}")
        print(f"Total DRFT Claims: {total_drft_claims.group(1) if total_drft_claims else 'N/A'}")
        print(f"Total Daily Claims: {total_daily_claims.group(1) if total_daily_claims else 'N/A'}")
        print(f"DRFT: {drft.group(1) if drft else 'N/A'}")
    else:
        print(f"Gagal mendapatkan informasi akun. Status kode: {response.status_code}")

# Fungsi untuk memproses akun
def process_account(token, cookie):
    url = "https://drftparty.fibrum.com/set-task?task_id=201"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Cookie": cookie,
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://drftparty.fibrum.com/game",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Token": token
    }
    
    response = requests.get(url, headers=headers)
    return response.status_code

# Fungsi untuk menampilkan hitung mundur satu hari
def countdown_one_day():
    end_time = datetime.now() + timedelta(days=1)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"Hitung mundur: {remaining_time}", end='\r')
        time.sleep(1)

# Fungsi utama untuk menjalankan seluruh proses
def main():
    accounts = read_data('data.txt')
    total_accounts = len(accounts)
    print(f"Total akun: {total_accounts}")
    
    for idx, (token, cookie) in enumerate(accounts):
        print(f"Memproses akun ke-{idx+1} dari {total_accounts}")
        login_status = login_account(token, cookie)
        if login_status == 200:
            info_account(token, cookie)
            status_code = process_account(token, cookie)
            print(f"Status kode: {status_code}")
        else:
            print(f"Gagal login. Status kode: {login_status}")
        time.sleep(5)
    
    print("Semua akun telah diproses. Memulai hitung mundur 1 hari.")
    countdown_one_day()
    print("Memulai ulang proses.")
    main()

if __name__ == "__main__":
    main()
