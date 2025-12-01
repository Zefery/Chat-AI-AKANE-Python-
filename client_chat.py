import socket
import sys

# --- KOnfigurasi Koneksi ---
# Ganti IP dibawah ini sesuai yang ada di VM Server di GNS3
SERVER_HOST = '127.0.0.1' # Untuk tes lokal 
SERVER_PORT = 9999       # Sesuaikan dengan port di server

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print(f"Mencoba terhubung ke Akane di {SERVER_HOST}:{SERVER_PORT}...")
            s.connect((SERVER_HOST, SERVER_PORT))
            print("Berhasil terhubung!")
            
            # Terima pesan sapaan pertama
            sapaan = s.recv(1024).decode('utf-8')
            print(sapaan, end='') # 'end=""' agar prompt "Anda:" muncul di baris yg sama

        except ConnectionRefusedError:
            print("[ERROR] Koneksi ditolak. Apakah server_chat.py sudah berjalan?")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Gagal terhubung: {e}")
            sys.exit(1)

        # Loop buat input user
        while True:
            try:
                # Dapatkan input dari keyboard (CLI)
                user_input = input() # Prompt "Anda:" sudah dicetak oleh server

                # Cek kata kunci untuk keluar
                if user_input.lower() in ["keluar", "cukup", "selesai"]:
                    print("Memutuskan koneksi... Sampai jumpa!")
                    break # Keluar dari loop
                
                # Kirim pertanyaan ke server
                s.sendall(user_input.encode('utf-8'))
                
                # Terima balasan dari server
                # Buffer 4096 untuk jaga-jaga jika respons AI panjang
                response = s.recv(4096).decode('utf-8')
                
                if not response:
                    print("[Info] Server menutup koneksi.")
                    break

                print(response, end='') # 'end=""' agar prompt "Anda:" tetap rapi

            except KeyboardInterrupt:
                print("\nMemutuskan koneksi... Sampai jumpa!")
                break
            except Exception as e:
                print(f"[ERROR] Koneksi terputus: {e}")
                break

if __name__ == "__main__":
    start_client()