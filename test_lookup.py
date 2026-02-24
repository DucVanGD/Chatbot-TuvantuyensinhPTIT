"""Script để test tra cứu điểm chuẩn trực tiếp từ JSON"""
import json
import os

def normalize_string(s):
    """Chuẩn hóa string: lowercase, loại bỏ khoảng trắng thừa"""
    if not s:
        return ""
    s = s.lower()
    s = ' '.join(s.split())
    return s

def load_lookup_data():
    """Load JSON data"""
    lookup_file = os.path.join("actions", "lookup_data.json")
    with open(lookup_file, "r", encoding="utf-8") as f:
        return json.load(f)

def search_score(major, year="2025", campus=None):
    """Tìm điểm chuẩn"""
    data = load_lookup_data()
    major_normalized = normalize_string(major)
    
    results = []
    for item in data:
        item_major = normalize_string(item.get("major", ""))
        item_year = str(item.get("year"))
        
        if campus:
            item_campus = normalize_string(item.get("campus", ""))
            campus_normalized = normalize_string(campus)
            if (item_major == major_normalized and 
                item_year == str(year) and 
                item_campus == campus_normalized):
                results.append(item)
        else:
            if (item_major == major_normalized and 
                item_year == str(year)):
                results.append(item)
    
    return results

if __name__ == "__main__":
    # Test cases
    print("=== TEST 1: Công nghệ thông tin năm 2025 ===")
    results = search_score("Công nghệ thông tin", "2025")
    print(f"Tìm thấy {len(results)} kết quả:")
    for r in results:
        print(f"  - {r['campus']}: {r['score']} điểm")
    
    print("\n=== TEST 2: Công nghệ thông tin năm 2025 Hà Nội ===")
    results = search_score("Công nghệ thông tin", "2025", "Hà Nội")
    print(f"Tìm thấy {len(results)} kết quả:")
    for r in results:
        print(f"  - {r['campus']}: {r['score']} điểm")
    
    print("\n=== TEST 3: An toàn thông tin năm 2024 ===")
    results = search_score("An toàn thông tin", "2024")
    print(f"Tìm thấy {len(results)} kết quả:")
    for r in results:
        print(f"  - {r['campus']}: {r['score']} điểm")
    
    print("\n=== Tất cả các ngành năm 2025 ===")
    data = load_lookup_data()
    majors_2025 = set()
    for item in data:
        if str(item.get("year")) == "2025":
            majors_2025.add(item.get("major"))
    
    print(f"Có {len(majors_2025)} ngành trong năm 2025:")
    for major in sorted(majors_2025):
        print(f"  - {major}")
