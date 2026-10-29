from src.pipeline import read_csv, validate_data, run, OUT
def inputs(): return [read_csv(n) for n in ['participants.csv','treatment_assignments.csv','visits.csv','assessments.csv','study_config.csv']]
def test_pipeline_outputs():
 run(); assert (OUT/'validation_issues.csv').exists(); assert (OUT/'quality_metrics.csv').exists(); assert (OUT/'raw_study_data.sqlite').exists()
def test_invalid_age_flagged():
 p,a,v,o,c=inputs(); x=validate_data(p,a,v,o,c); assert ((x.rule_id=='DM002')&(x.record_id=='P006')).any()
def test_out_of_range_score_flagged():
 p,a,v,o,c=inputs(); x=validate_data(p,a,v,o,c); assert ((x.rule_id=='DM012')&(x.record_id=='OUT004')).any()
def test_arm_before_effective_date_flagged():
 p,a,v,o,c=inputs(); x=validate_data(p,a,v,o,c); assert ((x.rule_id=='DM006')&(x.record_id=='ASG005')).any()
def test_visit_not_in_protocol_version_flagged():
 p,a,v,o,c=inputs(); x=validate_data(p,a,v,o,c); assert ((x.rule_id=='DM008')&(x.record_id=='V012')).any()
