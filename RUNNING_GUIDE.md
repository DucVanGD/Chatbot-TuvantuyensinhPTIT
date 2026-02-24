# Hướng dẫn chạy RASA Chatbot

## Cách chạy (2 terminals)

### Terminal 1 - Chạy Action Server
```powershell
.\run_actions.ps1
```
Hoặc:
```powershell
& ".\venv\Scripts\Activate.ps1"
rasa run actions
```

### Terminal 2 - Chạy Chatbot
```powershell
.\run_shell.ps1
```
Hoặc:
```powershell
& ".\venv\Scripts\Activate.ps1"
rasa shell
```

## Test câu hỏi mẫu

- "Cho mình điểm chuẩn ngành Công nghệ thông tin"
- "Điểm chuẩn An toàn thông tin năm 2024"
- "Điểm chuẩn CNTT ở Hà Nội"
- "Ngành Khoa học máy tính điểm chuẩn bao nhiêu"
- "Điểm chuẩn Marketing cơ sở TP.HCM"

## Cách hoạt động

- **Thiếu năm**: Tự động dùng năm 2025
- **Thiếu cơ sở**: Hiển thị điểm cả Hà Nội và TP.HCM
- **Thiếu ngành**: Bot sẽ hỏi lại

## Danh sách ngành có dữ liệu năm 2025

Chạy script test để xem danh sách:
```powershell
python test_lookup.py
```

## Lỗi thường gặp

### 1. "Cannot connect to action server"
➜ Action server chưa chạy. Mở terminal khác và chạy `.\run_actions.ps1`

### 2. "Không tìm thấy điểm chuẩn"
➜ Kiểm tra tên ngành có đúng không bằng cách chạy `python test_lookup.py`

### 3. Entity không được trích xuất
➜ Cần train lại model: `rasa train`

## Train lại model

Khi thay đổi NLU data, stories, rules, hoặc domain:
```powershell
& ".\venv\Scripts\Activate.ps1"
rasa train
```
