# Cài đặt và minh họa AES và RSA

Bài tập môn **An toàn và bảo mật thông tin**. Chương trình Python nhận văn bản từ bàn phím, mã hóa và giải mã bằng AES-256-GCM, dùng RSA-OAEP để bảo vệ khóa AES, rồi đo thời gian xử lý của hai thuật toán.

## Chạy chương trình

Yêu cầu Python 3.10 trở lên. Trong thư mục chứa các tệp, chạy:

```powershell
py -3.14 -m pip install -r requirements.txt
py -3.14 aes.py
```

Nếu dùng phiên bản Python khác, thay `py -3.14` bằng lệnh gọi đúng phiên bản đó (ví dụ `python`).

## Kết quả hiển thị

1. Nhập một đoạn văn bản bất kỳ.
2. Chương trình in **nonce** và **bản mã kèm thẻ xác thực** dưới dạng Base64, rồi in nội dung sau giải mã.
3. Chương trình dùng RSA-OAEP mã hóa khóa AES; giải mã khóa và dùng khóa đó khôi phục thông điệp.
4. Chương trình in thời gian trung bình (µs/lần) của mã hóa và giải mã AES-GCM, RSA-OAEP.
---
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/bef8a5a8-e484-4cff-8acd-0a46aacebb67" />

---
Phần đo thời gian dùng một mẫu **32 byte riêng**, không dùng văn bản đã nhập; không tính thời gian sinh cặp khóa RSA. Kết quả phụ thuộc vào máy chạy và môi trường Python.

## Vai trò các thuật toán

- **AES-256-GCM:** mã hóa nội dung và kiểm tra tính toàn vẹn. Mỗi lần mã hóa với cùng khóa phải dùng nonce khác nhau.
- **RSA-OAEP:** mã hóa khóa AES để người có khóa bí mật RSA khôi phục; không dùng RSA để mã hóa cả thông điệp dài.
- Chương trình này **chưa xác thực danh tính người gửi**. Bài toán đó cần thêm chữ ký số và xác minh khóa công khai.

Chương trình tạo khóa mới mỗi lần chạy và không lưu khóa ra tệp. Vì vậy, dữ liệu từ một lần chạy không thể giải mã ở lần chạy sau bằng chương trình hiện tại. Đây là bản minh họa phục vụ học tập.

## Cấu trúc

```text
.
├── aes.py            # Mã hóa, giải mã, kết hợp RSA và đo thời gian
├── requirements.txt  # Thư viện Python cần cài
└── README.md         # Hướng dẫn
```


