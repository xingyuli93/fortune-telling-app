from fastapi import FastAPI, HTTPException
from datetime import datetime
import random
import sxtwl # 直接导入

# ===== 直接将 bazi.py 和 schemas.py 的内容复制过来 =====

# --- 来自 schemas.py ---
from pydantic import BaseModel
class AnalysisSchema(BaseModel):
    summary: str
    study: str
    career: str
    love: str
    health: str
    wealth: str
    social: str

class DivineResultSchema(BaseModel):
    fortune: str
    analysis: AnalysisSchema

class UserInputSchema(BaseModel):
    name: str
    birthdate: str
    mbti: str

# --- 来自 bazi.py ---
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
Wuxing = {
    "甲": "木", "乙": "木", "寅": "木", "卯": "木",
    "丙": "火", "丁": "火", "巳": "火", "午": "火",
    "戊": "土", "己": "土", "辰": "土", "戌": "土", "丑": "土", "未": "土",
    "庚": "金", "辛": "金", "申": "金", "酉": "金",
    "壬": "水", "癸": "水", "子": "水", "亥": "水",
}
def get_bazi_from_datetime(dt: datetime):
    day = sxtwl.fromSolar(dt.year, dt.month, dt.day)
    year_gan = Gan[day.getYearGZ().tg]
    year_zhi = Zhi[day.getYearGZ().dz]
    month_gan = Gan[day.getMonthGZ().tg]
    month_zhi = Zhi[day.getMonthGZ().dz]
    day_gan = Gan[day.getDayGZ().tg]
    day_zhi = Zhi[day.getDayGZ().dz]
    hour_gz = day.getHourGZ(dt.hour)
    hour_gan = Gan[hour_gz.tg]
    hour_zhi = Zhi[hour_gz.dz]
    bazi_chars = [year_gan, year_zhi, month_gan, month_zhi, day_gan, day_zhi, hour_gan, hour_zhi]
    wuxing_counts = { "木": 0, "火": 0, "土": 0, "金": 0, "水": 0 }
    for char in bazi_chars:
        wuxing_counts[Wuxing[char]] += 1
    return {
        "bazi": {
            "year": f"{year_gan}{year_zhi}", "month": f"{month_gan}{month_zhi}",
            "day": f"{day_gan}{day_zhi}", "hour": f"{hour_gan}{hour_zhi}"
        },
        "wuxing": wuxing_counts,
        "day_master": day_gan
    }

# ===== FastAPI 应用主体 =====

app = FastAPI(
    title="算命先生 API (独立版)",
    description="一个不再依赖外部模块和数据库的独立算命引擎。",
    version="2.0.0",
)

@app.get("/", tags=["通用"])
async def read_root():
    return {"message": "欢迎使用算命先生API(独立版)"}

@app.post("/api/v1/divine", response_model=DivineResultSchema, tags=["算命"])
async def get_divine_result(user_input: UserInputSchema):
    try:
        birth_dt = datetime.strptime(f"{user_input.birthdate} 12:00", "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式不正确，请使用 YYYY-MM-DD 格式。")
    
    bazi_info = get_bazi_from_datetime(birth_dt)
    bazi_str = f"年:{bazi_info['bazi']['year']} 月:{bazi_info['bazi']['month']} 日:{bazi_info['bazi']['day']} 时:{bazi_info['bazi']['hour']}"
    wuxing_str = ", ".join([f"{k}:{v}个" for k, v in bazi_info['wuxing'].items() if v > 0])

    # 返回一个不依赖数据库的、但包含真实计算结果的响应
    final_analysis = AnalysisSchema(
        summary=f"你好 {user_input.name} ({user_input.mbti})。您的八字为：{bazi_str}。日主为‘{bazi_info['day_master']}’，五行分布为：{wuxing_str}。",
        study="【学业】解读服务正在连接知识库...",
        career="【事业】解读服务正在连接知识库...",
        love="【爱情】解读服务正在连接知识库...",
        health="【健康】解读服务正在连接知识库...",
        wealth="【财运】解读服务正在连接知识库...",
        social="【人际】解读服务正在连接知识库..."
    )

    return DivineResultSchema(
        fortune="上上大吉：引擎独立运行中",
        analysis=final_analysis
    )
