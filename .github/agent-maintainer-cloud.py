"""Trusted Actions bridge. Credentials are scoped to separate workflow steps."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.request import Request, urlopen

REPOS={'trinayhari/agent-maintainer-sentry-skills','trinayhari/agent-maintainer-azure-skills'}
OUT=Path('artifacts/cloud-run')

def gh(path,method='GET',body=None):
    args=['gh','api',path,'--method',method]
    if body is not None: args+=['--input','-']
    result=subprocess.run(args,input=json.dumps(body) if body is not None else None,text=True,capture_output=True,check=True,timeout=60)
    return json.loads(result.stdout) if result.stdout.strip() else {}

def identity():
    event=json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text());pr=event['pull_request'];repo=event['repository']['full_name']
    if repo not in REPOS or pr['head']['repo']['full_name']!=repo or pr['base']['repo']['full_name']!=repo or pr.get('draft'): raise ValueError('Unsupported PR')
    return dict(repository=repo,pr=pr['number'],sha=pr['head']['sha'],runId=os.environ['GITHUB_RUN_ID'])

def callback(route,body):
    url=os.environ['CLOUD_URL'].rstrip('/')
    if not url.startswith('https://'): raise ValueError('HTTPS required')
    raw=json.dumps(body).encode()
    for attempt in range(5):
        try:
            with urlopen(Request(url+'/worker/'+route,data=raw,headers={'Authorization':'Bearer '+os.environ['CLOUD_WORKER_TOKEN'],'Content-Type':'application/json'}),timeout=60) as response: return json.load(response)
        except Exception:
            if attempt==4: raise
            time.sleep(2**attempt)

def claim():
    body=identity(); repo=body['repository'];number=body['pr']
    current=gh(f'repos/{repo}/pulls/{number}')
    if current['state']!='open' or current['head']['sha']!=body['sha']: raise ValueError('Stale PR event')
    paths=[];page=1
    while True:
        batch=gh(f'repos/{repo}/pulls/{number}/files?per_page=100&page={page}')
        paths.extend(p for f in batch for p in [f['filename'],f.get('previous_filename',f['filename'])])
        if len(batch)<100:break
        page+=1
        if page>30:raise ValueError('Changed files truncated')
    body['paths']=paths
    response=callback('claim',body)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'claim.json').write_text(json.dumps({**body,**response}))
    with open(os.environ['GITHUB_OUTPUT'],'a') as output:
        output.write('execute='+str(response.get('execute',False)).lower()+'\n')
        output.write('publish='+str(response.get('execute',False) or bool(response.get('saved'))).lower()+'\n')
        output.write('evaluate='+str(response.get('execute',False) and response.get('decision')=='evaluate').lower()+'\n')
    if response.get('execute'):
        gh(f'repos/{repo}/statuses/{body["sha"]}','POST',dict(state='pending',context='Agent Maintainer / cloud screening',description='Cloud skill task evaluation started',target_url=f'https://github.com/{repo}/actions/runs/{body["runId"]}'))
    print('Cloud reservation:',response.get('reason'))

def evaluate():
    # No publisher or callback token is supplied to this process by the workflow.
    claim=json.loads((OUT/'claim.json').read_text())
    if not claim.get('execute') or claim['decision']!='evaluate':raise ValueError('No paid reservation')
    from agent_maintainer.automatic import Worker
    from agent_maintainer.ci import run_ci,write_report
    worker=Worker(OUT/'local.sqlite',OUT/'unused.sqlite',Path.cwd())
    directory=OUT.resolve();repo=claim['repository'];sha=claim['sha']
    config=worker.prepare(repo,{'head':{'sha':sha}},directory)
    bundle=run_ci(config,Path.cwd(),api_key=os.environ.get('OPENAI_API_KEY'))
    summary=write_report(bundle,OUT,control_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
    status='INCOMPLETE' if claim.get('uncovered') else bundle['status']
    if claim.get('uncovered'):summary='# Coverage — INCOMPLETE\n\nOther changed skills have no runnable task mapping.\n\n'+summary
    (OUT/'evidence.json').write_text(json.dumps(dict(status=status,result=bundle['result'],suite=worker.store.get_suite(config['suiteId']),summary=summary)))

def sync():
    body=identity();claim=json.loads((OUT/'claim.json').read_text())
    if claim.get('saved'):
        evidence=claim['saved']
    elif not claim.get('execute'):
        print('Existing or blocked reservation; no paid replay.');return
    elif (OUT/'evidence.json').exists(): evidence=json.loads((OUT/'evidence.json').read_text())
    else:
        decision=claim['decision'];status='NOT_APPLICABLE' if decision=='not-applicable' else 'INCOMPLETE'
        explanation='No changed skill paths matched this connection.' if status=='NOT_APPLICABLE' else 'No complete evaluation evidence. A task mapping is missing or the runner stopped. No behavioral pass.'
        evidence=dict(status=status,summary=f'# Skill evaluation — {status}\n\nPR head: `{body["sha"]}`\n\n{explanation}')
    repo=body['repository'];number=body['pr'];sha=body['sha']
    run_url=f'https://github.com/{repo}/actions/runs/{body["runId"]}'
    if not claim.get('saved'): evidence['summary']+=f'\n\n[Actions evidence]({run_url}) · [Cloud dashboard]({os.environ["CLOUD_URL"]}/#jobs)\n\nScreening only; no merge, release, or policy approval.\n'
    # Persist evidence before PR publication; rerunning only this step is safe.
    callback('complete',{**body,'evidence':evidence})
    publish(body,evidence)

def publish(body,evidence):
    repo=body['repository'];number=body['pr'];sha=body['sha']
    run_url=f'https://github.com/{repo}/actions/runs/{body["runId"]}'
    current=gh(f'repos/{repo}/pulls/{number}')
    if current['state']!='open' or current['head']['sha']!=sha:
        print('Evidence saved; stale PR head will not receive a passing status.');return
    marker='<!-- agent-maintainer-cloud:'+sha+' -->'
    text=marker+'\n'+evidence['summary'];page=1;existing=None
    while True:
        comments=gh(f'repos/{repo}/issues/{number}/comments?per_page=100&page={page}')
        existing=next((c for c in comments if c['user']['login']=='github-actions[bot]' and c['body'].startswith(marker)),None)
        if existing or len(comments)<100:break
        page+=1
    if existing:gh(f'repos/{repo}/issues/comments/{existing["id"]}','PATCH',{'body':text[:60000]})
    else:gh(f'repos/{repo}/issues/{number}/comments','POST',{'body':text[:60000]})
    status=evidence['status']
    gh(f'repos/{repo}/statuses/{sha}','POST',dict(state='success' if status in ('PASS','NOT_APPLICABLE') else 'failure',context='Agent Maintainer / cloud screening',description=status+' — bounded screening only',target_url=run_url))
    callback('published',body)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as output:output.write(evidence['summary'])
    print('Evidence saved and PR synchronized:',status)

def reconcile():
    repo=os.environ['GITHUB_REPOSITORY']
    if repo not in REPOS:raise ValueError('Unknown repository')
    for run in callback('pending',{'repository':repo})['runs']:
        publish(run,run['evidence'])

if __name__=='__main__':
    # This file is also installed under the trusted fork's .github directory.
    sys.path.insert(0,str(Path.cwd()))
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['claim','evaluate','sync','reconcile']);args=parser.parse_args()
    {'claim':claim,'evaluate':evaluate,'sync':sync,'reconcile':reconcile}[args.command]()
