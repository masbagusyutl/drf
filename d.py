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
    response_text = response.text

    # Cari informasi akun menggunakan regex
    user_nick = re.search(r'"user_nick":"(.*?)"', response_text)
    total_drft_claims = re.search(r'"total_drft_claims":(\d+)', response_text)
    total_daily_claims = re.search(r'"total_daily_claims":(\d+)', response_text)
    drft = re.search(r'"drft":"(.*?)"', response_text)
    last_claimed_task_id = re.search(r'"last_claimed_task_id":(\d+)', response_text)
    last_claim_task_time = re.search(r'"last_claim_task_time":"(\d+)"', response_text)
    last_claim_drft_time = re.search(r'"last_claim_drft_time":"(\d+)"', response_text)

    print("Informasi Akun:")
    print(f"Username: {user_nick.group(1) if user_nick else 'N/A'}")
    print(f"Total DRFT Claims: {total_drft_claims.group(1) if total_drft_claims else 'N/A'}")
    print(f"Total Daily Claims: {total_daily_claims.group(1) if total_daily_claims else 'N/A'}")
    print(f"DRFT: {drft.group(1) if drft else 'N/A'}")
    print(f"Last Claimed Task ID: {last_claimed_task_id.group(1) if last_claimed_task_id else 'N/A'}")

    # Konversi Unix timestamp ke datetime
    def unix_to_datetime(timestamp):
        return datetime.utcfromtimestamp(int(timestamp))

    last_claim_task_time = unix_to_datetime(last_claim_task_time.group(1)) if last_claim_task_time else None
    last_claim_drft_time = unix_to_datetime(last_claim_drft_time.group(1)) if last_claim_drft_time else None

    print(f"Last Claim Task Time: {last_claim_task_time if last_claim_task_time else 'N/A'}")
    print(f"Last Claim DRFT Time: {last_claim_drft_time if last_claim_drft_time else 'N/A'}")

    return {
        "total_daily_claims": int(total_daily_claims.group(1)) if total_daily_claims else 0,
        "last_claimed_task_id": int(last_claimed_task_id.group(1)) if last_claimed_task_id else 0,
        "last_claim_task_time": last_claim_task_time,
        "last_claim_drft_time": last_claim_drft_time
    }

# Fungsi untuk memproses tugas
def process_task(token, cookie, task_id):
    url = f"https://drftparty.fibrum.com/set-task?task_id={task_id}"
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
    response_text = response.text

    # Cari informasi claimedDRFT dari respon
    claimed_drft = re.search(r'"claimedDRFT":"(\d+)"', response_text)
    if claimed_drft:
        print(f"Jumlah DRFT yang didapat: {claimed_drft.group(1)}")
    else:
        print("Data claimedDRFT tidak ditemukan.")

    if response.status_code == 200:
        print("Tugas berhasil diambil hari ini.")
    else:
        print(f"Tugas gagal atau sudah diambil hari ini. Status kode: {response.status_code}")

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
            account_info = info_account(token, cookie)
            
            # Proses cek in harian
            current_time = datetime.now()
            if account_info["last_claim_task_time"]:
                next_check_in_time = account_info["last_claim_task_time"] + timedelta(days=1)
                if current_time >= next_check_in_time:
                    print("Waktunya cek in harian.")
                    check_in_task_id = 101 + account_info["total_daily_claims"]
                    if check_in_task_id > 112:
                        check_in_task_id = 112  # Maksimal task_id untuk cek in
                    process_task(token, cookie, check_in_task_id)
                else:
                    print("Belum waktunya cek in harian.")
            else:
                print("Belum ada data cek in sebelumnya.")
            
            # Proses ambil hadiah harian
            print("Memproses tugas ambil hadiah harian.")
            process_task(token, cookie, 201)
            
            time.sleep(5)  # Jeda 5 detik sebelum memproses akun berikutnya
        else:
            print(f"Login gagal. Status kode: {login_status}")
    
    print("Semua akun telah diproses. Memulai hitung mundur 1 hari.")
    countdown_one_day()
    print("Memulai ulang proses.")
    main()

if __name__ == "__main__":
    main()
