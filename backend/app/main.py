from fastapi import FastAPI, HTTPException
from datetime import datetime
import random

# ===== 知识库与模型定义 (不再需要外部文件) =====
from pydantic import BaseModel
import sxtwl

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

# --- 硬编码的知识库 ---
KNOWLEDGE_BASE = {
    'fortunes': [
        '枯木逢春，否极泰来。',
        '天官赐福，心想事成。',
        '风云际会，大展宏图。',
        '渐入佳境，稳步上升。',
        '波澜不惊，平淡是真。',
        '雪上加霜，祸不单行。'
    ],
    'interpretations': {
        '日主甲木': {
            'summary': '您是甲木日主，如同参天大树，正直、仁慈且有上进心。是天生的领导者，但有时会因过于固执而错失良机。',
            'career': '事业上，甲木之人适合在稳定的大机构中向上发展，不适合过于投机的行业。持之以恒，终将成为栋梁之才。',
            'love': '感情中，您需要一个能理解您理想并给予支持的伴侣。您对感情忠诚，但有时缺乏浪漫，需要学习如何更好地表达情感。'
        },
        '五行火旺': {
            'summary': '您的命盘火势旺盛，热情、开朗、有礼貌，精力充沛。但需注意有时会显得急躁、缺乏耐心，容易与人发生口角。',
            'health': '健康方面，火旺之人需注意心血管系统和眼部的问题。建议多吃一些滋阴降火的食物，如银耳、莲子等，并保持平和的心态。'
        },
        'MBTI_INFJ': {
            'summary': '作为INFJ（提倡者），您拥有与生俱来的理想主义和道德感，富有创造力和洞察力。您致力于帮助他人，但有时会因过于理想化而感到疲惫。',
            'social': '人际交往中，您是深刻而富有同情心的朋友，但圈子不大。您需要保护好自己的精力，避免被他人的负面情绪过度消耗。'
        }
    }
}

# --- 核心计算逻辑 ---
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
Wuxing = {
    "甲": "木", "乙": "木", "寅": "木", "卯": "木", "丙": "火", "丁": "火", "巳": "火", "午": "火",
    "戊": "土", "己": "土", "辰": "土", "戌": "土", "丑": "土", "未": "土", "庚": "金", "辛": "金", "申": "金", "酉": "金",
    "壬": "水", "癸": "水", "子": "水", "亥": "水",
}
def get_bazi_from_datetime(dt: datetime):
    day = sxtwl.fromSolar(dt.year, dt.month, dt.day)
    day_master = Gan[day.getDayGZ().tg]
    tags = [f"日主{day_master}", f"MBTI_{user_input.mbti}"] # 假设 user_input 在此作用域可用
    return {"day_master": day_master, "tags": tags}

# ===== FastAPI 应用主体 =====
app = FastAPI(title="算命先生 API (无数据库版)", version="3.0.0")

@app.post("/api/v1/divine", response_model=DivineResultSchema, tags=["算命"])
async def get_divine_result(user_input: UserInputSchema):
    # 核心逻辑：从硬编码的知识库中查找解读
    day_master_char = get_bazi_from_datetime(datetime.strptime(user_input.birthdate, "%Y-%m-%d"))['day_master']
    user_tags = [f"日主{day_master_char}", f"MBTI_{user_input.mbti}"]

    analysis = {}
    categories = ['summary', 'study', 'career', 'love', 'health', 'wealth', 'social']
    for cat in categories:
        found = False
        for tag in user_tags:
            if tag in KNOWLEDGE_BASE['interpretations'] and cat in KNOWLEDGE_BASE['interpretations'][tag]:
                analysis[cat] = KNOWLEDGE_BASE['interpretations'][tag][cat]
                found = True
                break
        if not found:
            analysis[cat] = f"【{cat.capitalize()}】暂无与您（{day_master_char}, {user_input.mbti}）匹配的专属解读。"

    return DivineResultSchema(
        fortune=random.choice(KNOWLEDGE_BASE['fortunes']),
        analysis=AnalysisSchema(**analysis)
    )
