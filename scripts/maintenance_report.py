"""Render audit-derived recurrent outcome and cost tables; no hidden selection."""
import argparse,collections,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('metrics',type=Path,nargs='+');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
runs=[r for f in a.metrics for r in json.loads(f.read_text())['runs']]
text=['# Maintenance result tables','', 'Generated from independently audited raw runs. These tables do not themselves label development as fresh.','']
for r in runs:
    text += ['## '+r['path'],'', '| Arm | Complete uses | Final complete | Retained | Gained | Lost | Updates | Virtual updates | Scoring forwards |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for arm,c in r['costs'].items():
        ss=[s for s in r['scores'] if s['arm']==arm and s['suite']=='later'];pp=[p for p in r['pairs'] if p['arm']==arm]
        if not ss:continue
        last=ss[-1]
        text += [f"| {arm} | {sum(s['success'] for s in ss)}/{sum(s['total'] for s in ss)} | {last['success']}/{last['total']} | {sum(p['retained'] for p in pp)} | {sum(p['gained'] for p in pp)} | {sum(p['lost'] for p in pp)} | {c['update']['count']} | {c['virtual_update']['count']} | {c['selection_loss']['count']} |"]
    ex=r['explicit'];text += [f"| explicit | {ex['success']}/{ex['total']} | — | — | — | — | 0 | 0 | 0 |",'','### Costs by deployed branch','', '| Arm | Training input / target tokens | Virtual input / target tokens | Scoring input / target tokens | Use prompt / output tokens | Measured training / virtual / scoring / use seconds |','|---|---:|---:|---:|---:|---|']
    for arm,c in r['costs'].items():
        values=[str(c[k]['input_tokens'])+' / '+str(c[k]['target_tokens']) for k in ['update','virtual_update','selection_loss']]
        use=c['use_generation'];values+=[str(use['prompt_tokens'])+' / '+str(use['completion_tokens'])]
        times=' / '.join(f"{c[k]['seconds']:.2f}" for k in ['update','virtual_update','selection_loss','use_generation'])
        text += ['| '+arm+' | '+' | '.join(values)+' | '+times+' |']
    text += ['',f"Explicit archive: peak serialized bytes {ex['peak_archive_bytes']}; lookup comparisons {ex['retrieval_comparisons']}; lookup + execution seconds {ex['seconds']:.6f}.",'', '### Episode pairs','', '| Arm | Episode | Retained | Gained | Lost | Failed both |','|---|---:|---:|---:|---:|---:|']
    for row in r['pairs']:text+=['| '+' | '.join(str(row[k]) for k in ['arm','episode','retained','gained','lost','failed_both'])+' |']
    text+=['']
a.output.write_text('\n'.join(text)+'\n')
