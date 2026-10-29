from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
def read_csv(name): return pd.read_csv(DATA/name,dtype=str,keep_default_na=True)
def as_date(x):
    if pd.isna(x) or str(x).strip()=='': return None
    try: return pd.to_datetime(x,errors='raise').date()
    except Exception: return None
def add(issues,dataset,rec,field,rule,severity,value,msg):
    issues.append({'dataset':dataset,'record_id':str(rec),'field':field,'rule_id':rule,'severity':severity,'observed_value':'' if pd.isna(value) else str(value),'message':msg,'status':'OPEN'})
def validate_data(p,a,v,o,c):
    issues=[]; pids=set(p.participant_id.dropna().astype(str)); vids=set(v.visit_id.dropna().astype(str))
    for pid in p.loc[p.participant_id.duplicated(keep=False),'participant_id'].dropna().unique(): add(issues,'participants',pid,'participant_id','DM001','ERROR',pid,'Duplicate participant identifier; investigate.')
    consent={str(r.participant_id):as_date(r.consent_date) for r in p.itertuples()}
    for r in p.itertuples():
        age=pd.to_numeric(r.age_years,errors='coerce')
        if pd.isna(age) or age<18 or age>100: add(issues,'participants',r.participant_id,'age_years','DM002','ERROR',r.age_years,'Age outside the fictional range 18–100; verify against source.')
        if as_date(r.consent_date) is None: add(issues,'participants',r.participant_id,'consent_date','DM003','CRITICAL',r.consent_date,'Consent date missing/invalid; verify before relying on record.')
        con,en=as_date(r.consent_date),as_date(r.enrolment_date)
        if con and en and en<con: add(issues,'participants',r.participant_id,'enrolment_date','DM004','ERROR',r.enrolment_date,'Enrolment precedes consent; investigate chronology.')
    armc=c[c.element_type=='ARM']; visitc=c[c.element_type=='VISIT']
    for r in a.itertuples():
        if str(r.participant_id) not in pids: add(issues,'treatment_assignments',r.assignment_id,'participant_id','DM005','ERROR',r.participant_id,'Assignment refers to unknown participant.')
        matches=armc[(armc.code.astype(str)==str(r.arm_code))&(armc.protocol_version.astype(str)==str(r.protocol_version))]; dt=as_date(r.assignment_date)
        if matches.empty or dt is None: add(issues,'treatment_assignments',r.assignment_id,'arm_code','DM006','ERROR',r.arm_code,'Arm not configured for this version or assignment date invalid.')
        else:
            starts=[as_date(x) for x in matches.available_from]; starts=[x for x in starts if x]
            if not starts or dt<min(starts): add(issues,'treatment_assignments',r.assignment_id,'assignment_date','DM006','ERROR',r.assignment_date,'Arm assigned before configured effective date.')
    seen={}
    for r in v.itertuples():
        if str(r.participant_id) not in pids: add(issues,'visits',r.visit_id,'participant_id','DM007','ERROR',r.participant_id,'Visit refers to unknown participant.')
        matches=visitc[(visitc.code.astype(str)==str(r.visit_type))&(visitc.protocol_version.astype(str)==str(r.protocol_version))]
        planned,actual=as_date(r.planned_date),as_date(r.actual_date)
        if matches.empty: add(issues,'visits',r.visit_id,'visit_type','DM008','ERROR',r.visit_type,'Visit not configured for this protocol version.')
        elif planned:
            starts=[as_date(x) for x in matches.available_from]; starts=[x for x in starts if x]
            if starts and planned<min(starts): add(issues,'visits',r.visit_id,'planned_date','DM008','ERROR',r.planned_date,'Visit planned before configured effective date.')
        if str(r.visit_status).lower()=='completed' and actual is None: add(issues,'visits',r.visit_id,'actual_date','DM009','ERROR',r.actual_date,'Completed visit has no valid actual date.')
        key=(str(r.participant_id),str(r.visit_type),str(r.protocol_version))
        if key in seen: add(issues,'visits',r.visit_id,'participant_id + visit_type','DM010','REVIEW','/'.join(key),f'Possible duplicate; also inspect {seen[key]}. Repeats may be allowed.')
        else: seen[key]=r.visit_id
        con=consent.get(str(r.participant_id))
        if con and actual and actual<con: add(issues,'visits',r.visit_id,'actual_date','DM013','ERROR',r.actual_date,'Visit precedes consent; investigate chronology.')
    for r in o.itertuples():
        if str(r.visit_id) not in vids: add(issues,'assessments',r.assessment_id,'visit_id','DM011','ERROR',r.visit_id,'Assessment refers to unknown visit.')
        score=pd.to_numeric(r.fatigue_score,errors='coerce')
        if pd.isna(score) or score<0 or score>10 or float(score)!=int(score): add(issues,'assessments',r.assessment_id,'fatigue_score','DM012','ERROR',r.fatigue_score,'Score must be integer 0–10 in this fictional study.')
    has_assessment=set(o.visit_id.dropna().astype(str))
    for r in v.itertuples():
        if str(r.visit_status).lower()=='completed' and str(r.visit_id) not in has_assessment: add(issues,'visits',r.visit_id,'assessment','DM014','REVIEW','','Completed visit has no assessment in this simple demo.')
    cols=['dataset','record_id','field','rule_id','severity','observed_value','message','status']
    return pd.DataFrame(issues,columns=cols)
def build_listing(p,a,v):
    ass=a.sort_values('assignment_date').drop_duplicates('participant_id',keep='last')
    counts=v.groupby('participant_id').agg(visits_recorded=('visit_id','count'),visits_completed=('visit_status',lambda s:(s.str.lower()=='completed').sum()),visits_missed=('visit_status',lambda s:(s.str.lower()=='missed').sum())).reset_index()
    out=p.merge(ass[['participant_id','arm_code','assignment_date','protocol_version']],on='participant_id',how='left').merge(counts,on='participant_id',how='left')
    for col in ['visits_recorded','visits_completed','visits_missed']: out[col]=out[col].fillna(0).astype(int)
    return out
def run():
    p,a,v,o,c=[read_csv(n) for n in ['participants.csv','treatment_assignments.csv','visits.csv','assessments.csv','study_config.csv']]
    issues=validate_data(p,a,v,o,c); listing=build_listing(p,a,v)
    metrics=pd.DataFrame([('participants_total',len(p),'Participant records'),('visits_total',len(v),'Visit records'),('visits_completed',int((v.visit_status.str.lower()=='completed').sum()),'Completed visits'),('visits_missed',int((v.visit_status.str.lower()=='missed').sum()),'Missed visits'),('open_findings_total',int((issues.status=='OPEN').sum()),'Open findings needing review'),('critical_findings',int((issues.severity=='CRITICAL').sum()),'Critical findings')],columns=['metric','value','definition'])
    sv=v.merge(p[['participant_id','site_id']],on='participant_id',how='left')
    sites=p.groupby('site_id').agg(participants=('participant_id','nunique')).reset_index().merge(sv.groupby('site_id').agg(visits=('visit_id','count'),completed=('visit_status',lambda s:(s.str.lower()=='completed').sum()),missed=('visit_status',lambda s:(s.str.lower()=='missed').sum())).reset_index(),on='site_id',how='left')
    issues.to_csv(OUT/'validation_issues.csv',index=False); listing.to_csv(OUT/'participant_listing.csv',index=False); metrics.to_csv(OUT/'quality_metrics.csv',index=False); sites.to_csv(OUT/'site_metrics.csv',index=False)
    db=OUT/'raw_study_data.sqlite'
    if db.exists(): db.unlink()
    with sqlite3.connect(db) as con:
        for name,df in zip(['participants','treatment_assignments','visits','assessments','study_config'],[p,a,v,o,c]): df.to_sql(name,con,index=False,if_exists='replace')
        con.execute('CREATE VIEW v_visit_counts AS SELECT participant_id, COUNT(*) AS visits_recorded FROM visits GROUP BY participant_id')
    print('Pipeline complete. Review outputs/: validation_issues.csv, participant_listing.csv, quality_metrics.csv, site_metrics.csv, raw_study_data.sqlite')
    print(f'{len(issues)} findings to investigate. Do not silently correct source data.')
if __name__=='__main__': run()
