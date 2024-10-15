from typing import Dict, Optional, Any

from pydantic import BaseModel

# my_proof/models/proof_response.py

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

