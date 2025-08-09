import json,subprocess
chart=json.loads(subprocess.check_output(['node','-e',"const{TYPE_CHART}=require('./hc/calc/data/types.js');console.log(JSON.stringify(TYPE_CHART[9]));"]).decode())

def effect(m,ts):
    v=1
    r=chart.get(m,{})
    for t in ts:
        v*=r.get(t,1)
    return v

def fetch(module,attr,name):
    js="const n=process.argv[1].toLowerCase();const d=require('%s').%s[9];const k=Object.keys(d).find(x=>x.toLowerCase()===n);console.log(JSON.stringify(k?d[k]:{}));"%(module,attr)
    return json.loads(subprocess.check_output(['node','-e',js,name]).decode())

def move_info(n):
    d=fetch('./hc/calc/data/moves.js','MOVES',n)
    return d.get('type',''),d.get('bp',0)

def pokemon_info(n):
    d=fetch('./hc/calc/data/species.js','SPECIES',n)
    ts=d.get('types',[])
    bs=d.get('bs',{})
    return ts,bs.get('at',0),bs.get('df',0),bs.get('sp',0)

name=input()
ability=input()
item=input()
moves=[input() for _ in range(4)]
op_types,_,op_def,_=pokemon_info(name)
op_move_types=[move_info(m)[0] for m in moves]
candidates=[{'name':'Tapu Fini','moves':['Moonblast','Scald']},{'name':'Weavile','moves':['Icicle Crash']},{'name':'Buzzwole','moves':['Ice Punch']}]
for c in candidates:
    ts,atk,df,sp=pokemon_info(c['name'])
    c['types']=ts
    c['attack']=atk
    c['defense']=df
    c['speed']=sp
    c['move_info']=[move_info(m) for m in c['moves']]

def resist(c):
    s=0
    for mt in op_move_types:
        s+=effect(mt,c['types'])
    return s

def ohko(c):
    for mt,pw in c['move_info']:
        st=1.5 if mt in c['types'] else 1
        if c['attack']*pw*st*effect(mt,op_types)>op_def*2:
            return True
    return False

tank=min(candidates,key=resist)
counters=[c for c in candidates if ohko(c)]
counter=max(counters,key=lambda x:x['speed']) if counters else {'name':'none'}
print('tank',tank['name'])
print('counter',counter['name'])
print('combo',tank['name'],counter['name'])
