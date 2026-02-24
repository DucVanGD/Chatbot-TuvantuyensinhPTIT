# Vietnamese PTIT Admission Chatbot 🤖

Chatbot tư vấn tuyển sinh cho Học viện Công nghệ Bưu chính Viễn thông (PTIT) được xây dựng bằng RASA framework.

## ✨ Tính năng

- 💬 Tư vấn thông tin tuyển sinh PTIT
- 📊 Tra cứu điểm chuẩn theo ngành và năm (2020-2025)
- 🏫 Hỗ trợ 2 cơ sở: Hà Nội và TP.HCM
- 🇻🇳 Tokenizer tiếng Việt tùy chỉnh
- 🔍 Tự động điền thông tin thiếu (năm mặc định 2025, hiển thị cả 2 cơ sở nếu không chỉ định)

## 📋 Yêu cầu

- Python 3.8 - 3.10
- pip

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/Vietnamese_Chatbot_RASA.git
cd Vietnamese_Chatbot_RASA
```

### 2. Tạo virtual environment

```bash
python -m venv venv
```

### 3. Kích hoạt virtual environment

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Cài đặt dependencies

```bash
pip install rasa
pip install pyvi
```

### 5. Train model

```bash
rasa train
```

## 🎯 Chạy chatbot

Cần mở **2 terminals**:

### Terminal 1 - Action Server

```powershell
# Windows
.\run_actions.ps1

# Hoặc manual
.\venv\Scripts\Activate.ps1
rasa run actions
```

### Terminal 2 - Chatbot

```powershell
# Windows
.\run_shell.ps1

# Hoặc manual
.\venv\Scripts\Activate.ps1
rasa shell
```

## 💡 Ví dụ câu hỏi

```
Bạn: Cho mình điểm chuẩn ngành Công nghệ thông tin
Bot: 📊 Điểm chuẩn ngành Công nghệ thông tin năm 2025:
     ▪ Cơ sở Hà Nội: 25.8 điểm (Khối A00, A01)
     ▪ Cơ sở TP.HCM: 23.47 điểm (Khối A00, A01)

Bạn: Điểm CNTT ở Hà Nội
Bot: 📊 Điểm chuẩn ngành Công nghệ thông tin năm 2025:
     ▪ Cơ sở Hà Nội: 25.8 điểm (Khối A00, A01)

Bạn: An toàn thông tin năm 2024
Bot: 📊 Điểm chuẩn ngành An toàn thông tin năm 2024:
     ▪ Cơ sở Hà Nội: 25.85 điểm (Khối A00, A01)
     ▪ Cơ sở TP.HCM: 24.68 điểm (Khối A00, A01)
```

## 🗂️ Cấu trúc thư mục

```
Vietnamese_Chatbot_RASA/
├── actions/              # Custom actions
│   ├── actions.py       # Logic tra cứu điểm chuẩn
│   └── lookup_data.json # Dữ liệu điểm chuẩn
├── data/                # Training data
│   ├── nlu.yml         # Intent examples & entities
│   ├── stories.yml     # Conversation flows
│   ├── rules.yml       # Rules
│   └── domain.yml      # Domain configuration
├── nlu/                 # Custom NLU components
│   └── tokenizer/      # Vietnamese tokenizer
├── config.yml          # Pipeline configuration
├── domain.yml          # Main domain file
├── endpoints.yml       # Action server endpoint
└── credentials.yml     # Channel credentials
```

## 🔧 Cấu hình

### Config.yml

- **Language**: vi (Vietnamese)
- **Pipeline**: 
  - Custom Vietnamese tokenizer (`nlu.tokenizer.vi_tokenizer.VietnameseTokenizer`)
  - DIETClassifier for intent & entity recognition
  - Entity synonym mapper
- **Policies**: TEDPolicy, RulePolicy, MemoizationPolicy

### Synonyms

Bot hỗ trợ các từ viết tắt:
- CNTT, IT → Công nghệ thông tin
- ATTT → An toàn thông tin
- HN, Ha Noi → Hà Nội
- HCM, Sài Gòn → TP.HCM

## 📊 Dữ liệu điểm chuẩn

File `actions/lookup_data.json` chứa điểm chuẩn của **34 ngành** từ năm **2020-2025**.

Chạy script test để xem danh sách:
```bash
python test_lookup.py
```

## 🛠️ Development

### Train lại model

Sau khi thay đổi NLU data, stories, hoặc domain:
```bash
rasa train --force
```

### Test conversations

```bash
rasa test
```

### Interactive learning

```bash
rasa interactive
```

## 📝 To-do

- [ ] Thêm intent cho các câu hỏi phức tạp hơn
- [ ] Tích hợp Forms cho slot filling
- [ ] Thêm dữ liệu điểm chuẩn năm 2026
- [ ] Deploy lên server
- [ ] Tích hợp Telegram/Facebook Messenger

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- RASA framework
- PTIT admission data
- pyvi Vietnamese tokenizer
