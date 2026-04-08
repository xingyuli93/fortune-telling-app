from fastapi import FastAPI
from datetime import datetime
from .models.schemas import UserInputSchema, DivineResultSchema, AnalysisSchema
from .core.bazi import get_bazi_from_datetime

app = FastAPI(
    title="算命先生 API",
    description="一个结合了姓名、生日和MBTI的专业算命引擎。",
    version="0.1.0",
)

@app.get("/", tags=["通用"])
async def read_root():
    return {"message": "欢迎使用算命先生API"}

@app.post("/api/v1/divine", response_model=DivineResultSchema, tags=["算命"])
async def get_divine_result(user_input: UserInputSchema):
    """
    接收用户信息，返回详细的算命结果。
    """
    # 1. 解析用户生日
    try:
        # 注意：为了精确计算时柱，我们需要用户的出生时间。这里暂时使用中午12点。
        birth_dt = datetime.strptime(f"{user_input.birthdate} 12:00", "%Y-%m-%d %H:%M")
    except ValueError:
        birth_dt = datetime.now()

    # 2. 计算命理信息
    bazi_info = get_bazi_from_datetime(birth_dt)
    
    # 构造八字字符串
    bazi_str = f"年:{bazi_info['bazi']['year']} 月:{bazi_info['bazi']['month']} 日:{bazi_info['bazi']['day']} 时:{bazi_info['bazi']['hour']}"
    # 构造五行字符串
    wuxing_str = ", ".join([f"{k}:{v}个" for k, v in bazi_info['wuxing'].items() if v > 0])

    # TODO: 在这里实现基于 bazi_info 的数据库查询和文本生成逻辑

    # 临时返回一个包含真实命理信息的模拟结果
    mock_analysis = AnalysisSchema(
        summary=f"你好 {user_input.name} ({user_input.mbti})。您的八字为：{bazi_str}。日主为‘{bazi_info['day_master']}’，五行分布为：{wuxing_str}。",
        study="【学业】基于您的命理，学业分析正在紧张开发中...",
        career="【事业】基于您的命理，事业分析正在紧张开发中...",
        love="【爱情】基于您的命理，爱情分析正在紧张开发中...",
        health="【健康】基于您的命理，健康分析正在紧张开发中...",
        wealth="【财运】基于您的命理，财运分析正在紧张开发中...",
        social="【人际】基于您的命理，人际分析正在紧张开发中..."
    )

    return DivineResultSchema(
        fortune="上上大吉：引擎升级，内功大增",
        analysis=mock_analysis
    )

# 在本地开发时，请在 backend 目录下运行: uvicorn app.main:app --reload
