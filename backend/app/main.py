from fastapi import FastAPI, HTTPException
from datetime import datetime
import random
from pydantic import BaseModel

# ===== 模型定义 =====
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

# ===== 硬编码的知识库 =====
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
            'summary': '您是甲木日主，如同参天大树，正直仁慈，有上进心，是天生的领导者。缺点是内心固执，不易变通。',
            'career': '【事业】作为甲木之人，您适合在稳定的大机构中向上发展，您的毅力和正直会为您赢得尊重。不适合过于投机的行业，稳扎稳打方为上策。',
            'love': '【爱情】您对感情忠诚，但有时缺乏浪漫。您需要一个能理解您理想并给予支持的伴侣，学会更好地表达内在情感是您的课题。'
        },
        '日主乙木': {
            'summary': '您是乙木日主，如藤蔓花草，外表柔顺，内心坚韧。适应力强，善于协调，但有时会显得没有主见。',
            'career': '【事业】您适合从事需要沟通、协调和适应性的工作，如教育、艺术、市场等。与人合作能更好地发挥您的才能。',
            'love': '【爱情】您在感情中体贴温柔，但需要一个能给您提供依靠和方向的伴侣。安全感对您至关重要。'
        },
        'MBTI_INFJ': {
            'summary': '作为INFJ（提倡者），您拥有与生俱来的理想主义和道德感，富有创造力和洞察力。您致力于帮助他人，但有时会因过于理想化而感到疲惫。',
            'social': '【人际】您是深刻而富有同情心的朋友，但社交圈子不大。请务必保护好自己的精力，避免被他人的负面情绪过度消耗。'
        }
    }
}

# ===== 纯Python八字计算引擎 =====
class PureBaziCalculator:
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    def get_bazi(self, dt: datetime):
        day_diff = (dt - datetime(1900, 1, 1)).days
        day_gan_idx = day_diff % 10
        return self.Gan[day_gan_idx]

# ===== FastAPI 应用主体 =====
app = FastAPI(title="算命先生 API (最终版)", version="6.0.0")
calculator = PureBaziCalculator()

@app.post("/api/v1/divine", response_model=DivineResultSchema, tags=["算命"])
async def get_divine_result(user_input: UserInputSchema):
    try:
        birth_dt = datetime.strptime(user_input.birthdate, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式不正确。")
    
    day_master_char = calculator.get_bazi(birth_dt)
    user_tags = [f"日主{day_master_char}", f"MBTI_{user_input.mbti}"]

    analysis_texts = {}
    categories = ['summary', 'study', 'career', 'love', 'health', 'wealth', 'social']
    
    summary_parts = []
    for tag in user_tags:
        if tag in KNOWLEDGE_BASE['interpretations'] and 'summary' in KNOWLEDGE_BASE['interpretations'][tag]:
            summary_parts.append(KNOWLEDGE_BASE['interpretations'][tag]['summary'])
    analysis_texts['summary'] = " ".join(summary_parts) if summary_parts else f"你好 {user_input.name}，暂无与您（{day_master_char}, {user_input.mbti}）匹配的专属解读。"

    for cat in categories:
        if cat == 'summary': continue
        found = False
        for tag in user_tags:
            if tag in KNOWLEDGE_BASE['interpretations'] and cat in KNOWLEDGE_BASE['interpretations'][tag]:
                analysis_texts[cat] = KNOWLEDGE_BASE['interpretations'][tag][cat]
                found = True
                break
        if not found:
            analysis_texts[cat] = f"【{cat.capitalize()}】暂无与您匹配的专属解读。"

    return DivineResultSchema(
        fortune=random.choice(KNOWLEDGE_BASE['fortunes']),
        analysis=AnalysisSchema(**analysis_texts)
    )
