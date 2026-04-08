-- 签文总表
CREATE TABLE fortunes (
    id SERIAL PRIMARY KEY,
    level INTEGER NOT NULL, -- 1:上上, 2:上吉, 3:中吉, 4:中平, 5:下下
    fortune_text TEXT NOT NULL
);

-- 解读库
CREATE TABLE interpretations (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL, -- 维度: study, career, love, health, wealth, social
    tag VARCHAR(100) NOT NULL, -- 命理标签: e.g., '日主甲木', '五行缺水', 'MBTI_INFJ'
    interpretation_text TEXT NOT NULL,
    sentiment_score REAL DEFAULT 0 -- 情感倾向: -1.0 (负面) to 1.0 (正面)
);

-- 添加索引以优化查询性能
CREATE INDEX idx_interpretations_tag ON interpretations (tag);
CREATE INDEX idx_interpretations_category ON interpretations (category);

-- 插入一些示例签文
INSERT INTO fortunes (level, fortune_text) VALUES
(1, '枯木逢春，否极泰来。'),
(1, '天官赐福，心想事成。'),
(2, '风云际会，大展宏图。'),
(3, '渐入佳境，稳步上升。'),
(4, '波澜不惊，平淡是真。'),
(5, '雪上加霜，祸不单行。');

-- 插入一些示例解读
INSERT INTO interpretations (category, tag, interpretation_text, sentiment_score) VALUES
-- 日主甲木
('summary', '日主甲木', '您是甲木日主，如同参天大树，正直、仁慈且有上进心。是天生的领导者，但有时会因过于固执而错失良机。', 0.5),
('career', '日主甲木', '事业上，甲木之人适合在稳定的大机构中向上发展，不适合过于投机的行业。持之以恒，终将成为栋梁之才。', 0.6),
('love', '日主甲木', '感情中，您需要一个能理解您理想并给予支持的伴侣。您对感情忠诚，但有时缺乏浪漫，需要学习如何更好地表达情感。', 0.3),

-- 五行火旺
('summary', '五行火旺', '您的命盘火势旺盛，热情、开朗、有礼貌，精力充沛。但需注意有时会显得急躁、缺乏耐心，容易与人发生口角。', 0.2),
('health', '五行火旺', '健康方面，火旺之人需注意心血管系统和眼部的问题。建议多吃一些滋阴降火的食物，如银耳、莲子等，并保持平和的心态。', -0.3),

-- MBTI_INFJ
('summary', 'MBTI_INFJ', '作为INFJ（提倡者），您拥有与生俱来的理想主义和道德感，富有创造力和洞察力。您致力于帮助他人，但有时会因过于理想化而感到疲惫。', 0.7),
('social', 'MBTI_INFJ', '人际交往中，您是深刻而富有同情心的朋友，但圈子不大。您需要保护好自己的精力，避免被他人的负面情绪过度消耗。', 0.1);
