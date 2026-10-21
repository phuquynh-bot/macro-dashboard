import os
import json
from google import genai
from google.genai import types

# Khởi tạo client Gemini từ biến môi trường đã lưu ở GitHub Secrets
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

prompt = """
Bạn là một chuyên viên phân tích vĩ mô tài chính Việt Nam.
Hãy tra cứu Google Search về các số liệu thị trường mới nhất trong tuần vừa qua tại Việt Nam:
1. Lãi suất liên ngân hàng kỳ hạn qua đêm (Overnight).
2. Tỷ giá USD/VND niêm yết bán ra tại Vietcombank.
3. Giá vàng miếng SJC bán ra (triệu đồng/lượng) và giá vàng thế giới Spot (USD/oz).
4. Tình hình thanh khoản và diễn biến giá bất động sản tuần qua.

Yêu cầu định dạng:
Chỉ trả về DUY NHẤT một chuỗi JSON hợp lệ, KHÔNG bọc trong markdown codeblock ```json, tuân thủ đúng mẫu sau:
{
  "updated_at": "YYYY-MM-DD",
  "ai_summary": "Tóm tắt 3-4 câu bức tranh tổng quan vĩ mô tuần qua...",
  "interest_rate": {
    "overnight": "x.xx%",
    "delta_percent": "+/-x.x%",
    "detail": "Diễn biến thanh khoản hệ thống ngân hàng..."
  },
  "fx": {
    "rate_vcb": "xx,xxx",
    "delta_percent": "+/-x.x%",
    "detail": "Áp lực tỷ giá và động thái điều hành..."
  },
  "gold": {
    "sjc_price": "xx.x",
    "world_price": "x,xxx",
    "detail": "Diễn biến chênh lệch giá vàng..."
  },
  "real_estate": {
    "liquidity_note": "Ổn định / Tăng nhẹ / Trầm lắng",
    "detail": "Điểm tin phân khúc chung cư và đất nền..."
  }
}
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[{"google_search": {}}],
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )
    
    clean_text = response.text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]

    with open("macro_data.json", "w", encoding="utf-8") as f:
        f.write(clean_text.strip())

    print("Cập nhật thành công file macro_data.json!")
except Exception as e:
    print(f"Lỗi khi cập nhật dữ liệu: {e}")
    raise e
