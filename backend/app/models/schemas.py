from pydantic import BaseModel
from typing import Dict

class UserInputSchema(BaseModel):
    """用户输入的模型"""
    name: str
    birthdate: str # 格式应为 YYYY-MM-DD
    mbti: str

class AnalysisSchema(BaseModel):
    """详细分析的模型"""
    summary: str
    study: str
    career: str
    love: str
    health: str
    wealth: str
    social: str

class DivineResultSchema(BaseModel):
    """算命结果的输出模型"""
    fortune: str
    analysis: AnalysisSchema
