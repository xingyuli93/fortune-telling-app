from fastapi import FastAPI, HTTPException
from datetime import datetime
import random

from .models.schemas import UserInputSchema, DivineResultSchema, AnalysisSchema
from .core.bazi import get_bazi_from_datetime
from .core.database import get_db_connection, release_db_connection

app = FastAPI(
    title="算命先生 API",
    description="一个结合了姓名、生日和MBTI的专业算命引擎。",
    version="1.0.0",
)

@app.get("/", tags=["通用"])
async def read_root():
    return {"message": "欢迎使用算命先生API"}

@app.post("/api/v1/divine", response_model=DivineResultSchema, tags=["算命"])
async def get_divine_result(user_input: UserInputSchema):
    """
    接收用户信息，连接数据库，返回包含真实解读的算命结果。
    """
    conn = None
    try:
        # 1. 解析用户生日并计算命理信息
        try:
            birth_dt = datetime.strptime(f"{user_input.birthdate} 12:00", "%Y-%m-%d %H:%M")
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式不正确，请使用 YYYY-MM-DD 格式。")
        
        bazi_info = get_bazi_from_datetime(birth_dt)

        # 2. 准备命理标签用于查询
        tags = [
            f"日主{bazi_info['day_master']}",
            f"MBTI_{user_input.mbti}"
        ]
        # 添加五行旺衰标签
        wuxing_max = max(bazi_info['wuxing'], key=bazi_info['wuxing'].get)
        wuxing_min = min(bazi_info['wuxing'], key=bazi_info['wuxing'].get)
        if bazi_info['wuxing'][wuxing_max] >= 4:
            tags.append(f"五行{wuxing_max}旺")
        if bazi_info['wuxing'][wuxing_min] == 0:
            tags.append(f"五行缺{wuxing_min}")

        # 3. 从数据库连接池获取连接
        conn = get_db_connection()
        cursor = conn.cursor()

        # 4. 查询解读文本
        analysis_texts = {}
        categories = ['summary', 'study', 'career', 'love', 'health', 'wealth', 'social']
        for cat in categories:
            cursor.execute(
                "SELECT interpretation_text FROM interpretations WHERE category = %s AND tag = ANY(%s) ORDER BY sentiment_score DESC LIMIT 1",
                (cat, tags)
            )
            result = cursor.fetchone()
            analysis_texts[cat] = result[0] if result else f"【{cat.capitalize()}】暂无与您命理（{', '.join(tags)}）完全匹配的解读。"

        # 5. 随机抽取一条签文
        cursor.execute("SELECT fortune_text FROM fortunes ORDER BY RANDOM() LIMIT 1")
        fortune_text = cursor.fetchone()[0]

        # 6. 组合最终结果
        final_analysis = AnalysisSchema(**analysis_texts)
        return DivineResultSchema(fortune=fortune_text, analysis=final_analysis)

    except Exception as e:
        # 异常处理
        print(f"发生错误: {e}")
        raise HTTPException(status_code=500, detail="服务器内部错误，我们正在紧急处理！")
    finally:
        # 确保数据库连接被释放回连接池
        if conn:
            release_db_connection(conn)

# 在本地开发时，请在 backend 目录下运行: uvicorn app.main:app --reload
