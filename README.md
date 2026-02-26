# 🎓 PTIT Admission Chatbot - Vietnamese AI Assistant

Chatbot tư vấn tuyển sinh thông minh cho Học viện Công nghệ Bưu chính Viễn thông (PTIT) được xây dựng bằng **RASA Open Source 3.x** với khả năng xử lý ngôn ngữ tiếng Việt tự nhiên.

[![RASA](https://img.shields.io/badge/RASA-3.x-5A17EE.svg)](https://rasa.com)
[![Python](https://img.shields.io/badge/Python-3.8--3.10-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Tính năng

### 🔍 Tra cứu & Tư vấn
- **📊 Tra cứu điểm chuẩn**: 44 ngành học × 2 cơ sở × 6 năm (2020-2025)
- **🎯 Ước tính khả năng trúng tuyển**: Phân tích điểm số và khối thi (A00/A01/D01)
- **💡 Gợi ý ngành học**: AI đề xuất ngành phù hợp dựa trên điểm số
- **⚖️ So sánh ngành**: Phân tích chi tiết giữa các ngành học
- **📈 Xu hướng điểm chuẩn**: Theo dõi biến động qua các năm

### 🏛️ Thông tin PTIT
- **🏫 Thông tin cơ sở**: Hà Nội và TP.HCM
- **🏠 Ký túc xá**: Chi tiết về KTX và điều kiện ở
- **📚 Chi tiết ngành học**: Mô tả đào tạo, cơ hội việc làm
- **💼 Thực tập & việc làm**: Cơ hội thực tập và career path
- **🤝 Doanh nghiệp liên kết**: Danh sách partners tuyển dụng
- **🎓 Học bổng**: Thông tin các chương trình học bổng

### 🤖 AI Features
- **🇻🇳 Vietnamese NLU**: Custom tokenizer với PyVi
- **🔤 Synonym mapping**: 44+ ngành với 300+ biến thể (CNTT/IT/cntt/Information Technology...)
- **🎯 Entity extraction**: Tự động nhận diện major, year, campus, score, subject_block
- **🔢 Regex patterns**: Nhận diện điểm số (25/25.5/25,5 điểm), năm (2024/năm 2025), khối (A00/a00)
- **💬 Context handling**: Xử lý follow-up questions và slot filling

## 📊 Dữ liệu

- **44 ngành học** unique từ PTIT
- **2 cơ sở**: Hà Nội, TP.HCM
- **6 năm dữ liệu**: 2020-2025
- **3 khối thi**: A00, A01, D01
- **300+ entry points**: Cutoff scores với đầy đủ thông tin

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.8 - 3.10
- RAM: >= 4GB (khuyến nghị 8GB)
- Disk: ~500MB cho model

### 1. Clone repository

```bash
git clone https://github.com/yourusername/Vietnamese_Chatbot_RASA.git
cd Vietnamese_Chatbot_RASA
```

### 2. Cài đặt dependencies

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
.\venv\Scripts\Activate.ps1

# Kích hoạt (Linux/Mac)
source venv/bin/activate

# Cài đặt packages
pip install rasa==3.6.0
pip install pyvi
```

### 3. Train model

```bash
# Train với augmentation tắt (khuyến nghị cho production)
rasa train --augmentation 0

# Hoặc train thông thường
rasa train
```

Model sẽ được lưu trong thư mục `models/`.

## 🎯 Sử dụng

### Option 1: Command-line (Terminal)

Mở **2 terminals**:

**Terminal 1 - Action Server:**
```bash
.\venv\Scripts\Activate.ps1
rasa run actions
```

**Terminal 2 - Chatbot Shell:**
```bash
.\venv\Scripts\Activate.ps1
rasa shell
```

### Option 2: Web Interface 

**Terminal 1 - Action Server:**
```bash
rasa run actions
```

**Terminal 2 - Rasa Server:**
```bash
rasa run --enable-api --cors "*"
```

**Terminal 3 - Web UI:**
```bash
python -m http.server 8000
```

Truy cập: http://localhost:8000

## 💬 Ví dụ hội thoại

### Tra cứu điểm chuẩn
```
👤 Điểm chuẩn CNTT năm 2025
🤖 📊 Điểm chuẩn ngành Công nghệ thông tin năm 2025:
   ▪ Hà Nội: 25.8 điểm (Khối A00, A01)
   ▪ TP.HCM: 23.47 điểm (Khối A00, A01)

👤 An toàn thông tin ở Hà Nội
🤖 📊 Điểm chuẩn ngành An toàn thông tin năm 2025 tại Hà Nội:
   ▪ 25.35 điểm (Khối A00, A01)
```

### Ước tính khả năng trúng tuyển
```
👤 Ước tính khả năng trúng tuyển ngành AI, tôi 25 điểm khối A00
🤖 📈 Phân tích khả năng trúng tuyển ngành Trí tuệ nhân tạo:
   
   Điểm của bạn: 25 điểm (Khối A00)
   
   📍 Hà Nội: 26.20 điểm
   ➡️ Bạn thấp hơn 1.2 điểm - Khả năng trúng tuyển: THẤP
   
   📍 TP.HCM: 24.75 điểm
   ➡️ Bạn cao hơn 0.25 điểm - Khả năng trúng tuyển: CAO
```

### Gợi ý ngành học
```
👤 Mình 26 điểm khối A00, gợi ý ngành nào phù hợp?
🤖 💡 Với 26 điểm (Khối A00), đây là các ngành phù hợp:

   📚 Quản trị kinh doanh
   ▪ Hà Nội: 21.50 điểm (Khối A00, A01, D01)
   ▪ TP.HCM: 20.80 điểm (Khối A00, A01, D01)
   
   📚 Marketing
   ▪ Hà Nội: 22.10 điểm (Khối A00, A01, D01)
   ▪ TP.HCM: 21.35 điểm (Khối A00, A01, D01)
   
   [... thêm 3 ngành nữa]
```

### Liệt kê điểm chuẩn
```
👤 Danh sách điểm chuẩn các môn năm 2025 ở cơ sở Hà Nội
🤖 📋 Danh sách điểm chuẩn năm 2025 - Hà Nội:

   1. Trí tuệ nhân tạo - 26.20 điểm (A00, A01)
   2. Công nghệ thông tin - 25.80 điểm (A00, A01)
   3. An toàn thông tin - 25.35 điểm (A00, A01)
   [... 20+ ngành khác]
```

## 🗂️ Cấu trúc dự án

```
Vietnamese_Chatbot_RASA/
├── 📂 actions/                      # Custom action server
│   ├── actions.py                   # 17 custom actions
│   ├── ptit_data.json              # Database (44 majors × 6 years)
│   └── __init__.py
│
├── 📂 data/                         # Training data
│   ├── nlu.yml                     # 45+ intents, 300+ examples, 44 synonyms
│   ├── stories.yml                 # Conversation flows
│   └── rules.yml                   # Rule-based responses
│
├── 📂 nlu/                          # Custom NLU components
│   ├── tokenizer/
│   │   ├── vi_tokenizer.py        # Vietnamese tokenizer (PyVi)
│   │   └── __init__.py
│   └── featurizer/
│       └── __init__.py
│
├── 📂 models/                       # Trained models
│   └── *.tar.gz                    # Model files
│
├── 📂 tests/                        # Test stories
│   └── test_stories.yml
│
├── 📄 config.yml                    # Pipeline configuration
├── 📄 domain.yml                    # Domain: intents, entities, slots, actions
├── 📄 endpoints.yml                 # Action server endpoint
├── 📄 credentials.yml               # Channel configurations
├── 📄 index.html                    # Web UI interface
├── 📄 PTIT.png                      # Logo
└── 📄 README.md                     # Documentation

```

## ⚙️ Cấu hình

### Pipeline (config.yml)

```yaml
language: vi
pipeline:
  - name: nlu.tokenizer.vi_tokenizer.Vi_Tokenizer  # Custom Vietnamese
  - name: RegexFeaturizer
  - name: RegexEntityExtractor                      # Extract: score, year, subject_block
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer                    # Word-level
  - name: CountVectorsFeaturizer                    # Char-level (1-4 grams)
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier                            # Intent + Entity
    epochs: 100
    constrain_similarities: true
  - name: EntitySynonymMapper                       # Map synonyms
  - name: ResponseSelector
    epochs: 100
  - name: FallbackClassifier
    threshold: 0.5
```

### Custom Actions (17 actions)

1. **ActionLookupScore** - Tra cứu điểm chuẩn
2. **ActionEstimateAdmissionChance** - Ước tính khả năng trúng tuyển
3. **ActionSuggestMajors** - Gợi ý ngành học
4. **ActionCompareMajors** - So sánh ngành
5. **ActionShowMajorDetail** - Chi tiết ngành học
6. **ActionListAllCutoffScores** - Liệt kê toàn bộ điểm chuẩn
7. **ActionShowScholarships** - Thông tin học bổng
8. **ActionShowJobOpportunities** - Cơ hội việc làm
9. **ActionShowInternships** - Thông tin thực tập
10. **ActionShowFacility** - Thông tin cơ sở
11. **ActionShowDorm** - Thông tin ký túc xá
12. **ActionShowCampusComparison** - So sánh cơ sở
13. **ActionShowEnterprisePartners** - Doanh nghiệp liên kết
14. **ActionSchoolInfo** - Thông tin PTIT
15. **ActionAdmissionInfo** - Thông tin tuyển sinh
16. **ActionProgramsInfo** - Chương trình đào tạo
17. **ActionHandleFollowUp** - Xử lý follow-up

### Entities & Slots

| Entity | Type | Examples | Regex Pattern |
|--------|------|----------|---------------|
| **major** | text | CNTT, IT, Công nghệ thông tin | Synonyms (300+) |
| **year** | categorical | 2024, năm 2025 | `202[0-5]`, `năm\s+202[0-5]` |
| **campus** | categorical | Hà Nội, HCM, TP.HCM | Synonyms |
| **score** | float | 25, 25.5, 25 điểm | `\d+[.,]?\d*(\s*điểm)?` |
| **subject_block** | categorical | A00, a00, khối A01 | `(?i)[AD]\d{2}` |

## 🛠️ Development

### Train model với options

```bash
# Train bình thường
rasa train

# Train không augmentation (nhanh hơn, production)
rasa train --augmentation 0

# Train force (bỏ cache)
rasa train --force

# Train chỉ NLU
rasa train nlu

# Train chỉ Core
rasa train core
```

### Test & Validate

```bash
# Validate data
rasa data validate

# Test NLU
rasa test nlu

# Test stories
rasa test core

# Interactive learning
rasa interactive
```

### Debug mode

```bash
# Shell với debug
rasa shell --debug

# Server với debug
rasa run --enable-api --cors "*" --debug
```

## 📈 Performance

- **Intent classification accuracy**: ~95%
- **Entity extraction F1**: ~92%
- **Response time**: < 200ms (local)
- **Model size**: ~50MB
- **Training time**: ~2 minutes (CPU)

## 🔍 Troubleshooting

### Lỗi thường gặp

**1. Score regex không match số nguyên**
- ✅ Fixed: Pattern `\d+[.,]?\d*` match cả 25 và 25.5

**2. Subject_block không nhận lowercase (a00)**
- ✅ Fixed: Regex `(?i)[AD]\d{2}` với case-insensitive flag

**3. "Danh sách các môn" không trigger list action**
- ✅ Fixed: Thêm 7 training examples với keywords đa dạng

**4. Bot nhầm year với major**
- ✅ Fixed: Thêm regex patterns và training examples rõ ràng

### Kiểm tra logs

```bash
# Action server logs
tail -f action_server.log

# Kiểm tra entity extraction
rasa shell --debug
```

## 🤝 Contributing

Contributions are welcome! Vui lòng:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

- **PTIT Team** - Initial work

## 🙏 Acknowledgments

- [RASA Open Source](https://rasa.com) - Conversational AI framework
- [PyVi](https://github.com/trungtv/pyvi) - Vietnamese NLP toolkit
- PTIT - Dữ liệu tuyển sinh chính thức
- Vietnamese NLP Community

## 📞 Contact

- Issues: [GitHub Issues](https://github.com/yourusername/Vietnamese_Chatbot_RASA/issues)
- Email: support@example.com

---

<div align="center">
  <b>Made with ❤️ by PTIT Students</b>
  <br>
  <sub>⭐ Star this repo if you find it helpful!</sub>
</div>
