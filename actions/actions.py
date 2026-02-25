from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import json
import os
import unicodedata

# Đường dẫn đến file data duy nhất
PTIT_DATA_FILE = os.path.join(os.path.dirname(__file__), "ptit_data.json")


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


def load_ptit_data() -> Dict:
    """
    Load JSON data chứa toàn bộ thông tin PTIT.
    """
    ptit_file = os.path.abspath(PTIT_DATA_FILE)
    if not os.path.exists(ptit_file):
        return {}
    with open(ptit_file, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_admission_estimate(user_score: float, cutoff_score: float) -> tuple:
    """
    Đánh giá khả năng trúng tuyển dựa trên chênh lệch điểm.
    Returns: (percentage, message)
    """
    diff = user_score - cutoff_score
    
    if diff >= 2.0:
        return (95, "Khả năng trúng tuyển RẤT CAO! Bạn có điểm vượt xa điểm chuẩn.")
    elif diff >= 1.0:
        return (85, "Khả năng trúng tuyển CAO! Bạn có điểm tốt hơn điểm chuẩn đáng kể.")
    elif diff >= 0.5:
        return (70, "Khả năng trúng tuyển TỐT. Bạn có điểm cao hơn điểm chuẩn.")
    elif diff >= 0:
        return (50, "Khả năng trúng tuyển TRUNG BÌNH. Điểm của bạn ngang ngửa với điểm chuẩn năm trước.")
    elif diff >= -0.5:
        return (30, "Khả năng trúng tuyển THẤP. Điểm của bạn thấp hơn điểm chuẩn một chút.")
    else:
        return (10, "Khả năng trúng tuyển RẤT THẤP. Bạn nên cân nhắc các ngành khác hoặc cơ sở khác.")


class ActionLookupScore(Action):
    """
    Action lookup điểm chuẩn từ ptit_data.json
    """

    def name(self) -> Text:
        return "action_lookup_score"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        major = tracker.get_slot("major")
        year = tracker.get_slot("year")
        campus = tracker.get_slot("campus")

        if not major:
            dispatcher.utter_message(text="Bạn muốn tra cứu điểm chuẩn ngành gì?")
            return []

        if not year:
            year = "2025"

        data = load_ptit_data()
        cutoff_scores = data.get("cutoff_scores", [])

        major_normalized = normalize_string(major)
        results = []

        for item in cutoff_scores:
            item_major = normalize_string(item.get("major", ""))
            if item_major == major_normalized and str(item.get("year")) == str(year):
                if campus:
                    campus_normalized = normalize_string(campus)
                    item_campus = normalize_string(item.get("campus", ""))
                    if item_campus == campus_normalized:
                        results.append(item)
                else:
                    results.append(item)

        if results:
            msg = f"📊 Điểm chuẩn ngành **{major}** năm {year}:\n\n"
            for r in results:
                blocks = ", ".join(r.get("subject_blocks", []))
                msg += f"▪ Cơ sở {r.get('campus')}: **{r.get('score')} điểm** (Khối {blocks})\n"
            dispatcher.utter_message(text=msg)
        else:
            available_years = sorted(set(str(item.get("year")) for item in cutoff_scores))
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


# ================================================================
# ===== NEW ADVANCED ACTIONS USING PTIT_DATA.YML =====
# ================================================================




class ActionEstimateAdmissionChance(Action):
    """Ước tính khả năng trúng tuyển của thí sinh"""
    
    def name(self) -> Text:
        return "action_estimate_admission_chance"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        major = tracker.get_slot("major")
        score_str = tracker.get_slot("score")
        campus = tracker.get_slot("campus")
        
        if not major or not score_str:
            dispatcher.utter_message(
                text="Để dự đoán khả năng trúng tuyển, bạn cần cho mình biết ngành và điểm số của bạn nhé!"
            )
            return []
        
        try:
            # Xử lý điểm số: loại bỏ chữ "điểm" và thay dấu phẩy bằng dấu chấm
            score_cleaned = score_str.replace("điểm", "").replace(",", ".").strip()
            user_score = float(score_cleaned)
        except:
            dispatcher.utter_message(text="Điểm số không hợp lệ. Vui lòng nhập số điểm đúng định dạng (ví dụ: 27.5)")
            return []
        
        data = load_ptit_data()
        cutoff_scores = data.get("cutoff_scores", [])
        
        major_normalized = normalize_string(major)
        year = "2025"  # Năm mặc định
        
        matching_cutoffs = []
        for item in cutoff_scores:
            item_major = normalize_string(item.get("major", ""))
            if item_major == major_normalized and str(item.get("year")) == str(year):
                if campus:
                    campus_normalized = normalize_string(campus)
                    item_campus = normalize_string(item.get("campus", ""))
                    if item_campus == campus_normalized:
                        matching_cutoffs.append(item)
                else:
                    matching_cutoffs.append(item)
        
        if not matching_cutoffs:
            dispatcher.utter_message(
                text=f"Mình không tìm thấy điểm chuẩn ngành {major} năm {year}."
            )
            return []
        
        # Hiển thị kết quả cho từng cơ sở
        msg = f"📊 Dự đoán khả năng trúng tuyển ngành **{major}** với {user_score} điểm:\n\n"
        
        for cutoff in matching_cutoffs:
            cutoff_score = cutoff.get("score")
            campus_name = cutoff.get("campus")
            percentage, message = compute_admission_estimate(user_score, cutoff_score)
            
            msg += f"**Cơ sở {campus_name}** (Điểm chuẩn {year}: {cutoff_score}):\n"
            msg += f"  • Khả năng: {percentage}%\n"
            msg += f"  • Nhận xét: {message}\n\n"
        
        dispatcher.utter_message(text=msg)
        return []


class ActionSuggestMajors(Action):
    """Gợi ý các ngành phù hợp dựa trên điểm số"""
    
    def name(self) -> Text:
        return "action_suggest_majors"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        score_str = tracker.get_slot("score")
        
        if not score_str:
            dispatcher.utter_message(text="Bạn có thể cho mình biết điểm số của bạn để mình gợi ý không?")
            return []
        
        try:
            # Xử lý điểm số: loại bỏ chữ "điểm" và thay dấu phẩy bằng dấu chấm
            score_cleaned = score_str.replace("điểm", "").replace(",", ".").strip()
            user_score = float(score_cleaned)
        except:
            dispatcher.utter_message(text="Điểm số không hợp lệ.")
            return []
        
        data = load_ptit_data()
        cutoff_scores = data.get("cutoff_scores", [])
        year = "2025"  # Sử dụng điểm chuẩn năm 2025 làm tham khảo
        
        # Tính hiệu số và lọc các ngành trong phạm vi
        all_candidates = []
        for item in cutoff_scores:
            if str(item.get("year")) == str(year):
                cutoff = item.get("score")
                diff = cutoff - user_score  # Hiệu số (điểm chuẩn - điểm user)
                
                # Lọc các ngành có khoảng cách <= 4 điểm
                if abs(diff) <= 4:
                    percentage, message = compute_admission_estimate(user_score, cutoff)
                    all_candidates.append({
                        "major": item.get("major"),
                        "campus": item.get("campus"),
                        "cutoff": cutoff,
                        "diff": diff,
                        "percentage": percentage,
                        "message": message
                    })
        
        if not all_candidates:
            dispatcher.utter_message(
                text="Điểm bạn vượt ngoài phạm vi điểm của trường, bạn nên cân nhắc chọn trường khác phù hợp với khả năng của bản thân hơn."
            )
            return []
        
        # Tách thành 2 nhóm: dương (điểm chuẩn > điểm user) và âm (điểm chuẩn < điểm user)
        positive_group = [m for m in all_candidates if m["diff"] >= 0]  # diff >= 0
        negative_group = [m for m in all_candidates if m["diff"] < 0]   # diff < 0
        
        suitable_majors = []
        
        # Lấy 1 ngành gần nhất từ nhóm dương (diff nhỏ nhất)
        if positive_group:
            positive_group.sort(key=lambda x: x["diff"])
            suitable_majors.append(positive_group[0])
        
        # Lấy tất cả ngành từ nhóm âm, sắp xếp theo diff giảm dần (gần 0 nhất lên đầu)
        if negative_group:
            negative_group.sort(key=lambda x: x["diff"], reverse=True)  # -0.5, -1, -2...
            suitable_majors.extend(negative_group)
        
        msg = f"Gợi ý các ngành phù hợp với {user_score} điểm (dựa trên điểm chuẩn năm {year}):\n\n"
        for i, major in enumerate(suitable_majors, 1):
            msg += f"{i}. {major['major']} - {major['campus']}\n"
            if major['diff'] >= 0:
                msg += f"   Điểm chuẩn {year}: {major['cutoff']} (cần thêm {major['diff']:.2f} điểm)\n"
            else:
                msg += f"   Điểm chuẩn {year}: {major['cutoff']} (vượt {abs(major['diff']):.2f} điểm)\n"
            msg += f"   Khả năng: {major['percentage']}% - {major['message']}\n\n"
        
        msg += f"\nLưu ý: Dựa trên điểm chuẩn năm {year}, điểm năm 2026 có thể thay đổi."
        
        dispatcher.utter_message(text=msg)
        return []


class ActionCompareMajors(Action):
    """So sánh 2 ngành"""
    
    def name(self) -> Text:
        return "action_compare_majors"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        # Lấy các entity major từ tracker
        entities = tracker.latest_message.get("entities", [])
        majors = [e["value"] for e in entities if e["entity"] == "major"]
        
        if len(majors) < 2:
            dispatcher.utter_message(
                text="Bạn muốn so sánh 2 ngành nào? Ví dụ: 'So sánh CNTT và ATTT'"
            )
            return []
        
        major1, major2 = majors[0], majors[1]
        data = load_ptit_data()
        all_majors = data.get("majors", [])
        
        major1_normalized = normalize_string(major1)
        major2_normalized = normalize_string(major2)
        
        info1 = next((m for m in all_majors if normalize_string(m.get("name", "")) == major1_normalized or 
                      normalize_string(m.get("code", "")) == major1_normalized), None)
        info2 = next((m for m in all_majors if normalize_string(m.get("name", "")) == major2_normalized or 
                      normalize_string(m.get("code", "")) == major2_normalized), None)
        
        if not info1 or not info2:
            dispatcher.utter_message(text="Xin lỗi, mình không tìm thấy thông tin về một trong hai ngành bạn hỏi.")
            return []
        
        msg = f"📊 So sánh **{info1['name']}** và **{info2['name']}**:\n\n"
        
        msg += f"**{info1['name']} ({info1['code']})**\n"
        msg += f"• Mô tả: {info1['description']}\n"
        msg += f"• Lương TB: {info1.get('average_salary', 'N/A')}\n\n"
        
        msg += f"**{info2['name']} ({info2['code']})**\n"
        msg += f"• Mô tả: {info2['description']}\n"
        msg += f"• Lương TB: {info2.get('average_salary', 'N/A')}\n\n"
        
        dispatcher.utter_message(text=msg)
        return []


class ActionShowMajorDetail(Action):
    """Hiển thị thông tin chi tiết về 1 ngành"""
    
    def name(self) -> Text:
        return "action_show_major_detail"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        major = tracker.get_slot("major")
        
        if not major:
            dispatcher.utter_message(text="Bạn muốn tìm hiểu về ngành nào?")
            return []
        
        data = load_ptit_data()
        all_majors = data.get("majors", [])
        
        major_normalized = normalize_string(major)
        info = next((m for m in all_majors if normalize_string(m.get("name", "")) == major_normalized or 
                     normalize_string(m.get("code", "")) == major_normalized), None)
        
        if not info:
            dispatcher.utter_message(text=f"Xin lỗi, mình không tìm thấy thông tin về ngành {major}.")
            return []
        
        msg = f"🎓 **{info['name']} ({info['code']})**\n\n"
        msg += f"**Giới thiệu:**\n{info['description']}\n\n"
        
        msg += f"**Cơ hội nghề nghiệp:**\n"
        for job in info.get("career_opportunities", [])[:5]:
            msg += f"• {job}\n"
        
        msg += f"\n**Mức lương:**\n{info.get('average_salary', 'N/A')}\n\n"
        
        dispatcher.utter_message(text=msg)
        return []


class ActionShowScholarships(Action):
    """Hiển thị thông tin học bổng"""
    
    def name(self) -> Text:
        return "action_show_scholarships"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        data = load_ptit_data()
        scholarships = data.get("scholarships", [])
        
        if not scholarships:
            dispatcher.utter_message(text="Xin lỗi, mình không có thông tin về học bổng.")
            return []
        
        msg = "🎓 **Các loại học bổng tại PTIT:**\n\n"
        
        for sch in scholarships:
            msg += f"**{sch['name']}**\n"
            msg += f"• Mô tả: {sch['description']}\n"
            msg += f"• Giá trị: {sch['value']}\n"
            msg += f"• Điều kiện:\n"
            for cond in sch.get("conditions", []):
                msg += f"  - {cond}\n"
            
            if "partners" in sch:
                msg += f"• Đối tác: {', '.join(sch['partners'])}\n"
            msg += "\n"
        
        dispatcher.utter_message(text=msg)
        return []


class ActionShowJobOpportunities(Action):
    """Hiển thị cơ hội việc làm"""
    
    def name(self) -> Text:
        return "action_show_job_opportunities"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        major = tracker.get_slot("major")
        data = load_ptit_data()
        
        if major:
            # Hiển thị cơ hội việc làm cho ngành cụ thể
            all_majors = data.get("majors", [])
            major_normalized = normalize_string(major)
            info = next((m for m in all_majors if normalize_string(m.get("name", "")) == major_normalized or 
                        normalize_string(m.get("code", "")) == major_normalized), None)
            
            if info:
                msg = f"💼 **Cơ hội việc làm ngành {info['name']}:**\n\n"
                for job in info.get("career_opportunities", []):
                    msg += f"• {job}\n"
                msg += f"\n**Mức lương:**\n{info.get('average_salary', 'N/A')}"
                dispatcher.utter_message(text=msg)
            else:
                dispatcher.utter_message(text=f"Không tìm thấy thông tin về ngành {major}.")
        else:
            # Hiển thị thông tin chung
            msg = "💼 **Cơ hội việc làm tại PTIT:**\n\n"
            msg += "Sinh viên PTIT có tỷ lệ có việc làm cao sau tốt nghiệp (>90%).\n\n"
            msg += "**Các công ty đối tác:**\n"
            
            partners = data.get("internship_partners", [])
            for partner in partners:
                msg += f"• {partner.get('company')}\n"
            
            dispatcher.utter_message(text=msg)
        
        return []


class ActionShowInternships(Action):
    """Hiển thị thông tin thực tập"""
    
    def name(self) -> Text:
        return "action_show_internships"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        data = load_ptit_data()
        partners = data.get("internship_partners", [])
        
        if not partners:
            dispatcher.utter_message(text="Xin lỗi, mình không có thông tin về thực tập.")
            return []
        
        msg = "💼 **Các đối tác thực tập của PTIT:**\n\n"
        
        for partner in partners:
            msg += f"**{partner['company']}**\n"
            msg += f"• Vị trí: {', '.join(partner.get('positions', []))}\n"
            msg += f"• Mô tả: {partner['description']}\n\n"
        
        dispatcher.utter_message(text=msg)
        return []


class ActionShowFacility(Action):
    """Hiển thị thông tin cơ sở vật chất theo campus"""
    
    def name(self) -> Text:
        return "action_show_facility"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        campus = tracker.get_slot("campus")
        
        if not campus:
            dispatcher.utter_message(
                text="PTIT có nhiều cơ sở vật chất hiện đại như thư viện, phòng thí nghiệm, ký túc xá, sân thể thao và căng tin. Bạn muốn biết về cơ sở nào: Hà Nội hay TP.HCM?"
            )
            return []
        
        data = load_ptit_data()
        campuses = data.get("campuses", [])
        
        campus_normalized = normalize_string(campus)
        
        matching_campus = None
        for c in campuses:
            if normalize_string(c.get("name", "")) == campus_normalized:
                matching_campus = c
                break
        
        if not matching_campus:
            dispatcher.utter_message(
                text=f"Xin lỗi, mình không tìm thấy thông tin về cơ sở {campus}."
            )
            return []
        
        msg = f"🏫 **Cơ sở {matching_campus['name']}**\n\n"
        msg += f"📍 Địa chỉ: {matching_campus.get('address')}\n"
        msg += f"👥 Số sinh viên: ~{matching_campus.get('student_count', 'N/A'):,} sinh viên\n\n"
        msg += "**Cơ sở vật chất:**\n\n"
        
        for facility in matching_campus.get("facilities", []):
            msg += f"▪ **{facility['name']}**: {facility['description']}\n\n"
        
        dispatcher.utter_message(text=msg)
        return []


class ActionShowDorm(Action):
    """Hiển thị thông tin ký túc xá"""
    
    def name(self) -> Text:
        return "action_show_dorm"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        campus = tracker.get_slot("campus")
        
        data = load_ptit_data()
        campuses = data.get("campuses", [])
        
        if campus:
            campus_normalized = normalize_string(campus)
            matching_campus = None
            for c in campuses:
                if normalize_string(c.get("name", "")) == campus_normalized:
                    matching_campus = c
                    break
            
            if matching_campus and matching_campus.get("dorms"):
                msg = f"Thông tin ký túc xá cơ sở {matching_campus['name']}:\n\n"
                for dorm in matching_campus.get("dorms", []):
                    msg += f"** {dorm['name']}**\n"
                    msg += f"- Sức chứa: {dorm['capacity']} sinh viên\n"
                    msg += f"- Loại phòng: {dorm['room_type']}\n"
                    msg += f"- Giá: {dorm['price']}\n"
                    msg += f"- Tiện nghi: {', '.join(dorm['amenities'])}\n"
                    if dorm.get('note'):
                        msg += f"- Ghi chú: {dorm['note']}\n"
                    msg += "\n"
                
                if matching_campus.get("dorm_payment_note"):
                    msg += f"Lưu ý thanh toán: {matching_campus['dorm_payment_note']}"
                
                dispatcher.utter_message(text=msg)
                return []
        
        # Nếu không có campus hoặc không tìm thấy, hiển thị tất cả
        msg = "Thông tin ký túc xá PTIT:\n\n"
        
        for campus in campuses:
            if campus.get("dorms"):
                msg += f"**Cơ sở {campus['name']}:**\n"
                for dorm in campus.get("dorms", []):
                    msg += f"- {dorm['name']}: {dorm['room_type']}, {dorm['price']}\n"
                msg += "\n"
            else:
                msg += f"**Cơ sở {campus['name']}:**\n"
                msg += "Không có thông tin ký túc xá tại cơ sở này.\n\n"
        
        dispatcher.utter_message(text=msg)
        return []


class ActionShowCampusComparison(Action):
    """So sánh 2 cơ sở Hà Nội và TP.HCM"""
    
    def name(self) -> Text:
        return "action_show_campus_comparison"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        data = load_ptit_data()
        campuses = data.get("campuses", [])
        
        if len(campuses) < 2:
            dispatcher.utter_message(text="Xin lỗi, mình không đủ thông tin để so sánh.")
            return []
        
        msg = "📊 **So sánh 2 cơ sở PTIT:**\n\n"
        
        for campus in campuses:
            msg += f"**{campus['name']}**\n"
            msg += f"• Địa chỉ: {campus.get('address')}\n"
            msg += f"• Số sinh viên: ~{campus.get('student_count', 0):,} người\n"
            msg += f"• Số cơ sở vật chất: {len(campus.get('facilities', []))} hạng mục\n\n"
        
        msg += "💡 **Lưu ý:** Cả 2 cơ sở đều có chất lượng đào tạo tương đương, chỉ khác về quy mô và số lượng sinh viên. Cơ sở Hà Nội là trụ sở chính với quy mô lớn hơn, cơ sở TP.HCM tập trung vào phát triển CNTT và ĐTVT tại miền Nam."
        
        dispatcher.utter_message(text=msg)
        return []


class ActionListAllCutoffScores(Action):
    """Liệt kê điểm chuẩn tất cả các ngành trong một năm"""
    
    def name(self) -> Text:
        return "action_list_all_cutoff_scores"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        year = tracker.get_slot("year")
        campus = tracker.get_slot("campus")
        
        if not year:
            year = "2025"
        
        data = load_ptit_data()
        cutoff_scores = data.get("cutoff_scores", [])
        
        # Lọc theo năm và campus (nếu có)
        filtered_scores = []
        for item in cutoff_scores:
            if str(item.get("year")) == str(year):
                if campus:
                    campus_normalized = normalize_string(campus)
                    item_campus = normalize_string(item.get("campus", ""))
                    if item_campus == campus_normalized:
                        filtered_scores.append(item)
                else:
                    filtered_scores.append(item)
        
        if not filtered_scores:
            dispatcher.utter_message(
                text=f"Xin lỗi, mình không tìm thấy điểm chuẩn năm {year}."
            )
            return []
        
        # Sắp xếp theo campus và điểm giảm dần
        filtered_scores.sort(key=lambda x: (x.get("campus", ""), -x.get("score", 0)))
        
        campus_text = f" cơ sở {campus}" if campus else ""
        msg = f"Điểm chuẩn tất cả các ngành{campus_text} năm {year}:\n\n"
        
        current_campus = None
        for item in filtered_scores:
            item_campus = item.get("campus", "")
            if item_campus != current_campus:
                current_campus = item_campus
                msg += f"\n**Cơ sở {current_campus}:**\n"
            
            msg += f"- {item.get('major')}: {item.get('score')} điểm"
            if item.get('subject_blocks'):
                msg += f" (Khối: {', '.join(item['subject_blocks'])})"
            msg += "\n"
        
        dispatcher.utter_message(text=msg)
        return []


class ActionShowEnterprisePartners(Action):
    """Hiển thị thông tin các doanh nghiệp liên kết"""
    
    def name(self) -> Text:
        return "action_show_enterprise_partners"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[Dict]:
        data = load_ptit_data()
        partners = data.get("internship_partners", [])
        
        if not partners:
            dispatcher.utter_message(text="Xin lỗi, mình không có thông tin về các doanh nghiệp liên kết.")
            return []
        
        msg = "Các doanh nghiệp liên kết với PTIT:\n\n"
        msg += "PTIT có quan hệ đối tác chiến lược với nhiều doanh nghiệp lớn trong và ngoài nước, mang lại cơ hội thực tập và việc làm cho sinh viên:\n\n"
        
        for partner in partners:
            msg += f"**{partner['company']}**\n"
            msg += f"- Vị trí thực tập/tuyển dụng: {', '.join(partner.get('positions', []))}\n"
            msg += f"- Mô tả: {partner['description']}\n\n"
        
        msg += "\nNgoài ra, PTIT còn hợp tác với nhiều doanh nghiệp khác như Samsung, Mobifone, CMC, TMA Solutions, VNG, Sendo, Tiki... tạo cơ hội rộng mở cho sinh viên."
        
        dispatcher.utter_message(text=msg)
        return []