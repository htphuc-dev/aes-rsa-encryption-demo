import base64
import os
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def average_microseconds(operation, repetitions: int) -> float:
    start = time.perf_counter()
    for _ in range(repetitions):
        operation()
    return (time.perf_counter() - start) * 1_000_000 / repetitions


def main() -> None:
    plaintext = input("Nhập dữ liệu cần mã hóa: ").encode("utf-8")

    # Mỗi lần chạy tạo một khóa mới. Không in khóa bí mật ra màn hình.
    aes_key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(aes_key)
    nonce = os.urandom(12)
    ciphertext_and_tag = aes.encrypt(nonce, plaintext, None)

    print("\n=== AES-256-GCM ===")
    print("Nonce (Base64):", to_base64(nonce))
    print("Bản mã + thẻ xác thực (Base64):", to_base64(ciphertext_and_tag))
    decrypted = aes.decrypt(nonce, ciphertext_and_tag, None)
    print("Sau giải mã:", decrypted.decode("utf-8"))

    # RSA chỉ mã hóa khóa AES ngắn; AES mã hóa nội dung thông điệp.
    rsa_private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rsa_public = rsa_private.public_key()
    oaep = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
    encrypted_aes_key = rsa_public.encrypt(aes_key, oaep)
    restored_aes_key = rsa_private.decrypt(encrypted_aes_key, oaep)
    restored_message = AESGCM(restored_aes_key).decrypt(
        nonce, ciphertext_and_tag, None
    )

    print("\n=== Kết hợp RSA + AES ===")
    print("Khóa AES đã bọc bằng RSA (Base64):", to_base64(encrypted_aes_key))
    print("Giải mã thông điệp bằng khóa AES đã khôi phục:",
          restored_message.decode("utf-8"))

    # So sánh cùng một mẫu 32 byte, không tính thời gian tạo cặp khóa RSA.
    sample = os.urandom(32)
    sample_nonce = os.urandom(12)
    sample_aes_ciphertext = aes.encrypt(sample_nonce, sample, None)
    sample_rsa_ciphertext = rsa_public.encrypt(sample, oaep)
    measurements = (
        ("AES-GCM mã hóa", lambda: aes.encrypt(os.urandom(12), sample, None), 2000),
        ("AES-GCM giải mã", lambda: aes.decrypt(sample_nonce, sample_aes_ciphertext, None), 2000),
        ("RSA-OAEP mã hóa", lambda: rsa_public.encrypt(sample, oaep), 200),
        ("RSA-OAEP giải mã", lambda: rsa_private.decrypt(sample_rsa_ciphertext, oaep), 200),
    )

    print("\n=== Thời gian trung bình, mẫu riêng 32 byte ===")
    for label, operation, repetitions in measurements:
        elapsed = average_microseconds(operation, repetitions)
        print(f"{label}: {elapsed:.2f} µs/lần ({repetitions} lần)")


if __name__ == "__main__":
    main()
