#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sxtwl
from datetime import datetime

# 天干
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# 地支
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 五行
Wuxing = {
    "甲": "木", "乙": "木", "寅": "木", "卯": "木",
    "丙": "火", "丁": "火", "巳": "火", "午": "火",
    "戊": "土", "己": "土", "辰": "土", "戌": "土", "丑": "土", "未": "土",
    "庚": "金", "辛": "金", "申": "金", "酉": "金",
    "壬": "水", "癸": "水", "子": "水", "亥": "水",
}

# 纳音
NaYin = {
    "甲子乙丑": "海中金", "丙寅丁卯": "炉中火", "戊辰己巳": "大林木", "庚午辛未": "路旁土", "壬申癸酉": "剑锋金",
    "甲戌乙亥": "山头火", "丙子丁丑": "涧下水", "戊寅己卯": "城头土", "庚辰辛巳": "白蜡金", "壬午癸未": "杨柳木",
    "甲申乙酉": "泉中水", "丙戌丁亥": "屋上土", "戊子己丑": "霹雳火", "庚寅辛卯": "松柏木", "壬辰癸巳": "长流水",
    "甲午乙未": "沙中金", "丙申丁酉": "山下火", "戊戌己亥": "平地木", "庚子辛丑": "壁上土", "壬寅癸卯": "金箔金",
    "甲辰乙巳": "覆灯火", "丙午丁未": "天河水", "戊申己酉": "大驿土", "庚戌辛亥": "钗钏金", "壬子癸丑": "桑柘木",
}

def get_nayin(gan_zhi_pair: str) -> str:
    """根据天干地支获取纳音"""
    for key, value in NaYin.items():
        if gan_zhi_pair in key:
            return value
    return ""

def get_bazi_from_datetime(dt: datetime):
    """根据公历日期和时间计算生辰八字、五行、纳音等信息"""
    day = sxtwl.fromSolar(dt.year, dt.month, dt.day)
    
    # 年柱
    year_gan_idx = day.getYearGZ().tg
    year_zhi_idx = day.getYearGZ().dz
    year_gan = Gan[year_gan_idx]
    year_zhi = Zhi[year_zhi_idx]
    year_pillar = f"{year_gan}{year_zhi}"

    # 月柱
    month_gan_idx = day.getMonthGZ().tg
    month_zhi_idx = day.getMonthGZ().dz
    month_gan = Gan[month_gan_idx]
    month_zhi = Zhi[month_zhi_idx]
    month_pillar = f"{month_gan}{month_zhi}"

    # 日柱 (日主)
    day_gan_idx = day.getDayGZ().tg
    day_zhi_idx = day.getDayGZ().dz
    day_gan = Gan[day_gan_idx]
    day_zhi = Zhi[day_zhi_idx]
    day_pillar = f"{day_gan}{day_zhi}"

    # 时柱
    hour_gz = day.getHourGZ(dt.hour)
    hour_gan_idx = hour_gz.tg
    hour_zhi_idx = hour_gz.dz
    hour_gan = Gan[hour_gan_idx]
    hour_zhi = Zhi[hour_zhi_idx]
    hour_pillar = f"{hour_gan}{hour_zhi}"

    # 计算五行
    bazi_chars = [year_gan, year_zhi, month_gan, month_zhi, day_gan, day_zhi, hour_gan, hour_zhi]
    wuxing_counts = { "木": 0, "火": 0, "土": 0, "金": 0, "水": 0 }
    for char in bazi_chars:
        wuxing_counts[Wuxing[char]] += 1

    return {
        "bazi": {
            "year": year_pillar,
            "month": month_pillar,
            "day": day_pillar,
            "hour": hour_pillar
        },
        "wuxing": wuxing_counts,
        "nayin": {
            "year": get_nayin(year_pillar),
            "month": get_nayin(month_pillar),
            "day": get_nayin(day_pillar),
            "hour": get_nayin(hour_pillar)
        },
        "day_master": day_gan # 日主，即日柱的天干
    }
