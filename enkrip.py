from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64


def get_mode(mode_name):
    modes = {
        "ECB": AES.MODE_ECB,
        "CBC": AES.MODE_CBC,
        "CFB": AES.MODE_CFB
    }
    return modes.get(mode_name.upper(), None)

def encrypt(plaintext, key, mode):
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(ciphertext).decode(), None
    else:
        iv = get_random_bytes(16)
        cipher = AES.new(key, mode, iv=iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(iv + ciphertext).decode(), iv

def decrypt(ciphertext_b64, key, mode):
    raw = base64.b64decode(ciphertext_b64)
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, mode)
        decrypted = unpad(cipher.decrypt(raw), AES.block_size)
        return decrypted.decode()
    else:
        iv = raw[:16]
        ciphertext = raw[16:]
        cipher = AES.new(key, mode, iv=iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode()

def main():
    print("AES Encryption/Decryption Program")
    action = input("Pilih aksi (encrypt/decrypt): ").strip().lower()
    mode_name = input("Pilih mode (ECB/CBC/CFB): ").strip().upper()
    mode = get_mode(mode_name)
    
    if not mode:
        print("Mode tidak dikenali.")
        return

    key = get_random_bytes(16)  # AES-128
    print(f"Kunci (hex): {key.hex()}")

    if action == "encrypt":
        plaintext = input("Masukkan plaintext: ")
        ciphertext_b64, _ = encrypt(plaintext, key, mode)
        print("Ciphertext (Base64):", ciphertext_b64)

    elif action == "decrypt":
        ciphertext_b64 = input("Masukkan ciphertext (Base64): ")
        try:
            decrypted = decrypt(ciphertext_b64, key, mode)
            print("Hasil dekripsi:", decrypted)
        except Exception as e:
            print("Gagal mendekripsi:", e)
    else:
        print("Aksi tidak dikenali.")

if __name__ == "__main__":
    main()
