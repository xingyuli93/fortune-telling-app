from fastapi import FastAPI, HTTPException
from datetime import datetime
import random

from .models.schemas import UserInputSchema, DivineResultSchema, AnalysisSchema
from .core.bazi import get_bazi_from_datetime
from .core.database import get_db_connection, release_db_connection

app = FastAPI(
    title="算命先生 API",
    description="一个结合了姓名、生日和MBTI的专业算命引擎。",
    version="1.0.1", # 版本升级
)

@app.get("/", tags=["通用"])
async def read_root():
    return {"message": "欢迎使用算命先生API"}

@app.post("/api/v1/divine", response_model=DivineResultSchema, tags=["算命"])
async def get_divine_result(user_input: UserInputSchema):
    """
    接收用户信息，尝试连接数据库返回真实解读，如果失败则返回优雅降级的结果。
    """
    # 1. 解析用户生日并计算命理信息
    try:
        birth_dt = datetime.strptime(f"{user_input.birthdate} 12:00", "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式不正确，请使用 YYYY-MM-DD 格式。")
    
    bazi_info = get_bazi_from_datetime(birth_dt)
    bazi_str = f"年:{bazi_info['bazi']['year']} 月:{bazi_info['bazi']['month']} 日:{bazi_info['bazi']['day']} 时:{bazi_info['bazi']['hour']}"
    wuxing_str = ", ".join([f"{k}:{v}个" for k, v in bazi_info['wuxing'].items() if v > 0])

    # 2. 尝试从数据库获取真实解读
    conn = None
    try:
        tags = [
            f"日主{bazi_info['day_master']}",
            f"MBTI_{user_input.mbti}"
        ]
        wuxing_max = max(bazi_info['wuxing'], key=bazi_info['wuxing'].get)
        if bazi_info['wuxing'][wuxing_max] >= 4:
            tags.append(f"五行{wuxing_max}旺")

        conn = get_db_connection()
        cursor = conn.cursor()

        analysis_texts = {}
        categories = ['summary', 'study', 'career', 'love', 'health', 'wealth', 'social']
        for cat in categories:
            cursor.execute(
                "SELECT interpretation_text FROM interpretations WHERE category = %s AND tag = ANY(%s) ORDER BY sentiment_score DESC LIMIT 1",
                (cat, tags)
            )
            result = cursor.fetchone()
            # 如果数据库有结果，就用数据库的；否则，提供一个包含命理信息的默认文本
            if result:
                analysis_texts[cat] = result[0]
            else:
                analysis_texts[cat] = f"【{cat.capitalize()}】暂无与您命理（{bazi_info['day_master']}, {user_input.mbti}）完全匹配的解读。"

        cursor.execute("SELECT fortune_text FROM fortunes ORDER BY RANDOM() LIMIT 1")
        fortune_text = cursor.fetchone()[0]

        final_analysis = AnalysisSchema(**analysis_texts)
        return DivineResultSchema(fortune=fortune_text, analysis=final_analysis)

    except Exception as e:
        # 如果数据库查询失败，打印错误日志，并返回降级版结果
        print(f"数据库查询失败，返回降级结果。错误: {e}")
        mock_analysis = AnalysisSchema(
            summary=f"你好 {user_input.name} ({user_input.mbti})。您的八字为：{bazi_str}。日主为‘{bazi_info['day_master']}’，五行分布为：{wuxing_str}。",
            study="【学业】解读服务暂不可用，请稍后重试。",
            career="【事业】解读服务暂不可用，请稍后重试。",
            love="【爱情】解读服务暂不可用，请稍后重试。",
            health="【健康】解读服务暂不可用，请稍后重试。",
            wealth="【财运】解读服务暂不可用，请稍后重试。",
            social="【人际】解读服务暂不可用，请稍后重试。"
        )
        return DivineResultSchema(fortune="服务升级中，请稍后再试", analysis=mock_analysis)

    finally:
        if conn:
            release_db_connection(conn)
