import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
plt.rcParams.update({"font.family":["NanumBarunGothic","DejaVu Sans"],"axes.unicode_minus":False,"figure.dpi":150,"figure.facecolor":"#ffffff","axes.facecolor":"#ffffff"})
mine=json.load(open("claims.json")); cx={x["id"]:x["label"] for x in json.load(open("codex_labels.json"))}
cats=list("FVCHAX"); names={"F":"F 확인된 사실","V":"V 확인 필요","C":"C 인과 주장","H":"H 해석","A":"A 시대착오","X":"X 입증 곤란"}
col={"F":"#2563eb","V":"#f59e0b","C":"#a855f7","H":"#64748b","A":"#ef4444","X":"#991b1b"}
T=["T1","T2","T3","T4","T5","T6"]; tl={"T1":"유신 공고화\n1972–75","T2":"말기 유신\n1979","T3":"공과 평가","T4":"쿠데타 국가\n세계 비교","T5":"한국을 만든\n5가지 동인","T6":"130년\n시민의 역사"}
fig,ax=plt.subplots(figsize=(9.5,5))
for j,t in enumerate(T):
    rows=[m for m in mine if m[0]==t]; n=len(rows); left=0
    for c in cats:
        v=sum(1 for m in rows if m[2]==c)/n*100
        if v: ax.barh(j,v,left=left,color=col[c],height=.6); ax.text(left+v/2,j,c,ha="center",va="center",color="white",fontsize=9,fontweight="bold") if v>=8 else None
        left+=v
    cf=sum(1 for i,m in enumerate(mine) if m[0]==t and cx[i+1]=="F")/n*100
    ax.plot(cf,j,marker="|",ms=22,mew=2.5,color="#111827"); ax.text(101,j,f"n={n}",va="center",fontsize=8.5,color="#64748b")
ax.set_yticks(range(6)); ax.set_yticklabels([tl[t] for t in T],fontsize=9); ax.invert_yaxis(); ax.set_xlim(0,110)
ax.set_xlabel("주장 비율 (%) — 색 막대: Claude 분류 · 검은 세로선: Codex가 F로 본 비율",fontsize=8.5)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=col[c],label=names[c]) for c in cats],ncol=3,fontsize=8,frameon=False,loc="upper center",bbox_to_anchor=(.5,-.14))
ax.set_title("AI가 쓴 한국사 요약 6편, 49개 문장의 확실성",loc="left",fontsize=12.5,fontweight="bold",color="#6366f1")
ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig("fig1_claim_audit.png"); plt.close(fig)
M=np.zeros((6,6),int)
for i,m in enumerate(mine): M[cats.index(m[2]),cats.index(cx[i+1])]+=1
fig,ax=plt.subplots(figsize=(6.2,5.4)); im=ax.imshow(M,cmap="Purples")
for a in range(6):
    for b in range(6):
        if M[a,b]: ax.text(b,a,M[a,b],ha="center",va="center",color="white" if M[a,b]>8 else "#1a1a2e",fontsize=11,fontweight="bold")
ax.set_xticks(range(6)); ax.set_xticklabels(cats); ax.set_yticks(range(6)); ax.set_yticklabels(cats)
ax.set_xlabel("Codex (블라인드)"); ax.set_ylabel("Claude")
n=len(mine); po=np.trace(M)/n; pe=sum(M[k,:].sum()*M[:,k].sum() for k in range(6))/n/n; k=(po-pe)/(1-pe)
ax.set_title(f"두 AI의 판정 일치 — 일치율 {po*100:.1f}%, 카파 {k:.2f}",loc="left",fontsize=11.5,fontweight="bold",color="#6366f1")
fig.tight_layout(); fig.savefig("fig2_agreement.png"); plt.close(fig)
print(round(po,3),round(k,3))
