# !/usr/bin/env python
import copy
import cv2
import base64
from baidubce import bce_base_client
from baidubce.auth import bce_credentials
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce import bce_client_configuration

# 危险行为识别
class RiskyBehaviorApiCenterClient(bce_base_client.BceBaseClient):

    def __init__(self, config=None):
        self.service_id = 'apiexplorer'
        self.region_supported = True
        self.config = copy.deepcopy(bce_client_configuration.DEFAULT_CONFIG)

        if config is not None:
            self.config.merge_non_none_values(config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    def capture_data_as_mp4(self,filepath, width, height, fps, timeseconds):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        vout = cv2.VideoWriter()
        vout.open(filepath, fourcc, fps, sz, True)

        cnt = 0
        while (cnt // fps < timeseconds):
            cnt += 1
            print(cnt)
            ret, frame = cap.read()
            vout.write(frame)
        vout.release()

    def file_str_to_base64(self,filepath):
        video_code = ""
        with open(filepath, "rb") as file:
            video_code = file.read()
            video_code = base64.b64encode(video_code)
        return video_code

    def detect(self,filepath):
        path = b'/rest/2.0/video-classify/v1/body_danger'
        headers = {}
        headers[b'Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'

        params = {}
        body = 'data='+ self.file_str_to_base64(filepath)
        return self._send_request(http_methods.POST, path, body, headers, params)

if __name__ == '__main__':
    endpoint = 'https://aip.baidubce.com'
    ak = 'ewuQ93j9hHxVLs6Mc8F2UkKR'
    sk = '8LzNbOX2NEALA5kxoufiH8uWpMXWtctN'
    config = bce_client_configuration.BceClientConfiguration(credentials=bce_credentials.BceCredentials(ak, sk),
                                                             endpoint=endpoint)
    filepath = "./data.mp4"
    client = RiskyBehaviorApiCenterClient(config)
    # client.capture_data_as_mp4(filepath=filepath, width=680, height=460, fps=30, timeseconds=5)
    res = client.detect(filepath)
    print(res.__dict__['raw_data'])