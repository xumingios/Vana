import json
import logging
import os
import requests
import random
import time
from typing import Dict, Any

class ProofResponse:
    def __init__(self, dlp_id):
        self.dlp_id = dlp_id
        self.ownership = 0.0
        self.quality = 0.0
        self.click_weight = 0.1  # 初始化权重为一个较小值
        self.score = 0.0
        self.valid = False
        self.attributes = {}
        self.metadata = {}
        self.last_access_time = None  # 用于记录上次获取时间

class Proof:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.proof_response = ProofResponse(dlp_id=config['dlp_id'])

    def generate(self) -> ProofResponse:
        logging.info("Starting proof generation")

        # 假设获取数据的次数
        fetch_count = self.get_fetch_count()

        # 根据获取次数更新权重
        self.update_click_weight(fetch_count)

        # 如果在指定时间内无人获取该数据，衰减权重
        self.decrease_click_weight()

        # 其他生成逻辑...

    def get_fetch_count(self) -> int:
        # 这里可以添加逻辑来计算用户获取数据的次数
        return 3  # 示例值

    def update_click_weight(self, fetch_count: int) -> None:
        self.proof_response.click_weight += fetch_count * 0.1  # 每次获取增加0.1的权重
        self.proof_response.last_access_time = time.time()  # 更新获取时间

    def decrease_click_weight(self) -> None:
        if self.proof_response.last_access_time:
            current_time = time.time()
            time_since_last_access = current_time - self.proof_response.last_access_time
            
            if time_since_last_access > 60:  # 假设设置的衰减时间为60秒
                decay_amount = (time_since_last_access // 60) * 0.1  # 每分钟衰减0.1
                self.proof_response.click_weight = max(0, self.proof_response.click_weight - decay_amount)

        self.proof_response.click_weight = max(self.proof_response.click_weight, 0)

def fetch_random_number() -> float:
    try:
        response = requests.get('https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new')
        return float(response.text.strip())
    except requests.RequestException as e:
        logging.warning(f"获取随机数时出错: {e}. 使用本地随机数。")
        return random.random()
