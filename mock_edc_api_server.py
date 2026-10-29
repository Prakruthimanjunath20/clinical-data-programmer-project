"""Local-only mock EDC REST endpoint for training."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path!='/api/v1/visits': self.send_response(404); self.end_headers(); self.wfile.write(b'{"error":"not found"}'); return
  body=(ROOT/'data'/'api_visits.json').read_bytes(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
 def log_message(self,*args): return
if __name__=='__main__':
 server=HTTPServer(('127.0.0.1',8000),Handler); print('Mock API: http://127.0.0.1:8000/api/v1/visits (Ctrl+C to stop)')
 try: server.serve_forever()
 except KeyboardInterrupt: pass
 finally: server.server_close()
