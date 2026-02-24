from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import json
import os
import unicodedata

# Đường dẫn đến file lookup trong cùng thư mục actions
LOOKUP_FILE = os.path.join(os.path.dirname(__file__), "lookup_data.json")


def normalize_string(s: str) -> str:
    """Chuẩn hóa string: lowercase, loại bỏ dấu thanh, trim spaces"""
    if not s:
        return ""
    # Lowercase
    s = s.lower()
    # Loại bỏ khoảng trắng thừa
    s = ' '.join(s.split())
    # Normalize Unicode (NFD -> loại bỏ dấu thanh nếu cần)
    # Hoặc giữ nguyên nếu muốn so sánh có dấu
    return s


# --- Hàm tra lookup điểm chuẩn ---
def load_lookup_data() -> List[Dict]:
    """
    Load JSON data chứa điểm chuẩn theo ngành, năm, cơ sở.
    """
    if not os.path.exists(LOOKUP_FILE):
        return []
    with open(LOOKUP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


class ActionLookupScore(Action):
    """
    Action lookup điểm chuẩn theo small JSON lookup_data.json
    """

    def name(self) -> Text:
        return "action_lookup_score"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        # lấy slot để tra
        major = tracker.get_slot("major")
        year = tracker.get_slot("year")
        campus = tracker.get_slot("campus")

        # Logic: thiếu major -> hỏi lại
        if not major:
            dispatcher.utter_message(text="Bạn muốn tra cứu điểm chuẩn ngành gì?")
            return []

        # Chuẩn hóa major
        major_normalized = normalize_string(major)

        # Logic: thiếu year -> mặc định 2025
        if not year:
            year = "2025"

        data = load_lookup_data()

        # Logic: thiếu campus -> tra cả Hà Nội và TP.HCM
        if not campus:
            # Tra cả 2 cơ sở
            results = []
            for item in data:
                item_major = normalize_string(item.get("major", ""))
                if (item_major == major_normalized and 
                    str(item.get("year")) == str(year)):
                    results.append(item)
        else:
            # Tra theo campus cụ thể
            campus_normalized = normalize_string(campus)
            results = []
            for item in data:
                item_major = normalize_string(item.get("major", ""))
                item_campus = normalize_string(item.get("campus", ""))
                if (item_major == major_normalized and 
                    str(item.get("year")) == str(year) and 
                    item_campus == campus_normalized):
                    results.append(item)

        if results:
            # có kết quả
            msg = f"📊 Điểm chuẩn ngành **{major}** năm {year}:\n\n"
            for r in results:
                msg += f"▪ Cơ sở {r.get('campus')}: **{r.get('score')} điểm** (Khối {r.get('subject_groups', 'N/A')})\n"
            dispatcher.utter_message(text=msg)
        else:
            # không có dữ liệu - thêm debug info
            available_years = sorted(set(str(item.get("year")) for item in data))
            dispatcher.utter_message(
                text=f"Xin lỗi, mình không tìm thấy điểm chuẩn ngành '{major}' năm {year}.\n\n"
                     f"Các năm có dữ liệu: {', '.join(available_years[-5:])}\n"
                     f"Hãy thử: 'Điểm chuẩn ngành [tên ngành] năm [năm] cơ sở [Hà Nội/TP.HCM]'"
            )

        return []


# --- Một số Action mẫu trả thông tin chung ---
# Bạn có thể gọi trong stories/rules dạng `utter_info_xxx` nếu cần tự trình bày
# hoặc nâng cấp thành action tùy biến nếu logic phức tạp.

class ActionSchoolInfo(Action):
    """ Trả lại nội dung giới thiệu trường PTIT """

    def name(self) -> Text:
        return "action_ptit_school_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        text = (
            "Học viện Công nghệ Bưu chính Viễn thông (PTIT) là trường đại học công lập trọng điểm "
            "quốc gia về đào tạo kỹ thuật và công nghệ hàng đầu tại Việt Nam, nổi bật với các chương "
            "trình đào tạo Công nghệ thông tin, An toàn thông tin, Khoa học máy tính, Truyền thông đa "
            "phương tiện, và nhiều ngành liên ngành khác. Trường được đánh giá cao về nghiên cứu, đổi "
            "mới sáng tạo và chất lượng đầu ra. Bạn có muốn biết thêm về chương trình, học phí hay học bổng không?"
        )
        dispatcher.utter_message(text=text)
        return []


class ActionAdmissionInfo(Action):
    """ Trả lại thông tin tổng quan về tuyển sinh """

    def name(self) -> Text:
        return "action_ptit_admission_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        # có thể thêm chi tiết hơn từ web
        text = (
            "Các phương thức tuyển sinh đại học PTIT năm 2025 bao gồm xét tuyển dựa trên hồ sơ học sinh giỏi, "
            "chứng chỉ đánh giá năng lực quốc tế, thi đánh giá năng lực/đánh giá tư duy, xét tuyển kết hợp, và "
            "xét tuyển theo kết quả thi tốt nghiệp THPT. Quy trình nộp hồ sơ trực tuyến được hướng dẫn rõ tại "
            "xettuyen.ptit.edu.vn. Bạn muốn mình tra điểm chuẩn ngành cụ thể không?"
        )
        dispatcher.utter_message(text=text)
        return []


class ActionProgramsInfo(Action):
    """ Trả lại danh sách chương trình và ngành đào tạo """

    def name(self) -> Text:
        return "action_ptit_programs_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict]:
        text = (
            "PTIT có nhiều chương trình đào tạo đại học chính quy như:\n"
            "- Công nghệ thông tin\n"
            "- An toàn thông tin\n"
            "- Khoa học máy tính\n"
            "- Truyền thông đa phương tiện\n"
            "- Marketing, Thương mại điện tử\n"
            "- Điện tử viễn thông và nhiều ngành liên ngành khác. "
            "Ngoài ra còn có chương trình chất lượng cao và học bổng hấp dẫn."
        )
        dispatcher.utter_message(text=text)
        return []