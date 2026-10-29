"""Fetch local mock EDC API JSON and convert it into a CSV import."""
from urllib.request import urlopen
from pathlib import Path
import json, pandas as pd
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
FIELDS=['visit_id','participant_id','visit_type','planned_date','actual_date','visit_status','protocol_version']
def main():
 try:
  with urlopen('http://127.0.0.1:8000/api/v1/visits',timeout=5) as resp:
   if resp.status!=200: raise RuntimeError(f'HTTP status {resp.status}')
   payload=json.loads(resp.read().decode('utf-8'))
 except Exception as exc: raise SystemExit(f'Could not fetch mock API. Start the server in another terminal. Details: {exc}')
 rows=payload.get('visits')
 if not isinstance(rows,list): raise SystemExit("API JSON must contain a 'visits' list")
 df=pd.DataFrame(rows); missing=[f for f in FIELDS if f not in df.columns]
 if missing: raise SystemExit(f'Missing expected fields: {missing}')
 target=OUT/'api_visits_import.csv'; df[FIELDS].to_csv(target,index=False)
 print(f'Fetched {len(df)} mock records; wrote {target.relative_to(ROOT)}')
 print('This is a mock integration exercise, not a validated EDC connection.')
if __name__=='__main__': main()
