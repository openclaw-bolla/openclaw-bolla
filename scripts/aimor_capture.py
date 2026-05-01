"""mitmproxy addon: loggt alle Aimor-API-Requests"""
import json
from mitmproxy import http

LOG = "/home/bolla/workspace/logs/aimor_traffic.log"

class AimorCapture:
    def request(self, flow: http.HTTPFlow):
        host = flow.request.pretty_host
        with open(LOG, "a") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"HOST: {host}\n")
            f.write(f"METHOD: {flow.request.method} {flow.request.pretty_url}\n")
            f.write(f"HEADERS: {dict(flow.request.headers)}\n")
            content = flow.request.content
            if content:
                try:
                    f.write(f"BODY: {json.dumps(json.loads(content), indent=2)}\n")
                except:
                    f.write(f"BODY (raw): {content[:500]}\n")

    def response(self, flow: http.HTTPFlow):
        host = flow.request.pretty_host
        if "aimor" in host or "elink" in host or "frame" in host:
            with open(LOG, "a") as f:
                f.write(f"RESPONSE {flow.response.status_code}: {flow.response.content[:1000]}\n")

addons = [AimorCapture()]
