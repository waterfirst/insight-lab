import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
plt.rcParams.update({"font.family":["NanumBarunGothic","DejaVu Sans"],"axes.unicode_minus":False,"figure.dpi":150,"figure.facecolor":"#ffffff"})
P,RD,GD,GR,TX,MU,BL="#6366f1","#ef4444","#f59e0b","#22c55e","#1a1a2e","#64748b","#3b82f6"

# ---------- Fig A: Nash bargaining x Alicia's disagreement point
fig,ax=plt.subplots(figsize=(7.2,6.4))
t=np.linspace(0,np.pi/2,400); uA=np.cos(t); uJ=np.sin(t)
ax.plot(uA,uJ,color=TX,lw=2); ax.fill_between(uA,0,uJ,color="#eef2ff")
ax.text(.08,1.03,"검은 곡선 = 가능한 합의의 경계(파레토 경계)",fontsize=9,color=TX)
def nash(d):
    m=(uA>d[0])&(uJ>d[1]); prod=np.where(m,(uA-d[0])*(uJ-d[1]),-1); i=prod.argmax(); return uA[i],uJ[i]
cases=[((0.05,0.30),RD,"1959  결렬점 d₁\n남편 입원·출산 직전\n알리샤의 바깥 선택지 거의 없음"),
       ((0.45,0.10),GR,"1963  결렬점 d₂\n이혼 + 자기 직장\n떠나도 버틸 수 있게 됨")]
for d,c,lab in cases:
    s=nash(d); ax.plot(*d,"o",color=c,ms=10); ax.plot(*s,"*",color=c,ms=17,mec="white")
    ax.annotate("",s,d,arrowprops=dict(arrowstyle="->",color=c,lw=1.4,ls="--"))
    ax.text(d[0]+.02,d[1]-.12 if d[1]>.2 else d[1]+.03,lab,fontsize=8.3,color=c)
    ax.text(s[0]-.09 if c==RD else s[0]+.03,s[1]+.04,f"합의점(별)\n알리샤 몫 {s[0]:.2f}",fontsize=8,color=c,ha="right" if c==RD else "left")
ax.set_xlabel("알리샤의 몫  →",fontsize=10); ax.set_ylabel("존 내시의 몫  →",fontsize=10)
ax.set_xlim(0,1.1); ax.set_ylim(0,1.1); ax.spines[["top","right"]].set_visible(False)
ax.set_title("내시 협상 해법(1950)으로 본 알리샤의 1963년 이혼",loc="left",fontsize=12.5,fontweight="bold",color=P)
fig.text(.02,.015,"규칙: 합의점 = (내 몫 − 결렬 시 내 몫)×(상대 몫 − 결렬 시 상대 몫)을 최대로 하는 점.  결렬점이 오른쪽으로 가면 합의점도 따라간다.\n※ 개념도다. 좌표는 실제 측정값이 아니라 구조를 보이기 위한 가상의 값이다.",fontsize=7.6,color=MU)
fig.subplots_adjust(bottom=.15,top=.93); fig.savefig("A_bargaining_alicia.png"); plt.close(fig)

# ---------- Fig B: two timelines – theory vs life (repeated game)
fig,ax=plt.subplots(figsize=(9,5.2))
ax.set_xlim(1945,2018); ax.set_ylim(-0.6,3.4); ax.axis("off")
ax.set_title("내시가 쓴 이론, 알리샤가 산 이론 — 50년짜리 반복게임",loc="left",fontsize=12.5,fontweight="bold",color=P)
for x in range(1950,2020,10): ax.text(x,-.5,str(x),ha="center",fontsize=8.5,color=MU); ax.plot([x,x],[-.35,3.0],color="#e5e7eb",lw=.6,zorder=0)
# row 3: theory
ax.text(1945,3.3,"존 내시의 이론",fontsize=9.5,fontweight="bold",color=TX)
th=[(1950,"1950 균형점·협상 해법",2.95),(1953,"1953 2인 협조 게임",2.2),(1956,"1956 매장 정리",2.95),(1994,"노벨상",2.2),(2008,"대리인 방법(협력)",2.2),(2015,"아벨상",2.95)]
HA={1950:"right",1956:"left"}
for x,l,yy in th: ax.plot(x,2.45,"o",color=P,ms=7); ax.plot([x,x],[2.45,yy],color=P,lw=.5); ax.text(x+(.5 if x==1956 else (-.5 if x==1950 else 0)),yy,l,ha=HA.get(x,"center"),fontsize=7.6,color=P,va="bottom" if yy>2.45 else "top")
ax.axvspan(1959,1990,ymin=.73,ymax=.86,color="#c7d2fe",alpha=.6); ax.text(1974.5,2.45,"투병 (논문 2편)",ha="center",va="center",fontsize=8,color=TX)
# row 1: Alicia strategy segments
ax.text(1945,1.95,"알리샤의 선택",fontsize=9.5,fontweight="bold",color=TX)
seg=[(1957,1963,RD,"결혼·간병"),(1963,1970,GR,"이혼·독립\n(아들은 계속 양육)"),(1970,2001,GD,"하숙인으로 다시 들임"),(2001,2015,BL,"재혼")]
for a,b,c,l in seg: ax.barh(1.0,b-a,left=a,height=.42,color=c); ax.text((a+b)/2,1.0,l,ha="center",va="center",fontsize=7.6,color="white",fontweight="bold")
ax.barh(0.35,2015-1975,left=1975,height=.22,color="#fca5a5"); ax.text(1976,0.35,"아들 조니 돌봄 (1975년경~)",va="center",fontsize=7.5,color=TX)
# mapping arrows
maps=[(1950,1962,"① 협상 해법: 결렬점을 키우자\n   관계가 다시 짜였다",1936.6),(1953,1970,"② 협조 게임: 재협상(새 계약=하숙)",1972),(2008,2001,"③ 말년의 협력 모형 —\n   그녀가 먼저 도착해 있던 곳",2002.5)]
for x0,x1,l,tx in maps:
    ax.add_patch(FancyArrowPatch((x0,1.95),(x1,1.25),arrowstyle="->",mutation_scale=10,color=MU,lw=.9,ls=(0,(3,2)),connectionstyle="arc3,rad=-0.15"))
    ax.text(tx if tx>1940 else 1945.5,1.72 if x0!=1950 else 1.55,l,fontsize=7.3,color=MU,ha="left")
fig.text(.02,.02,"반복게임: 한 번뿐인 게임에선 배신이 합리적일 수 있어도, 관계가 길고 미래를 중시할수록(할인율 δ↑) 협력이 균형이 된다.\n알리샤의 '지평'은 56년(1959–2015)이었다. 연결 화살표는 해석이며, 내시 본인이 자기 이론을 결혼에 적용했다는 기록은 없다.",fontsize=7.4,color=MU)
fig.subplots_adjust(bottom=.13,top=.92); fig.savefig("B_theory_vs_life.png"); plt.close(fig)

# ---------- Fig C: Trump-Putin-Xi triangle
fig,ax=plt.subplots(figsize=(9,7.4)); ax.set_xlim(0,10); ax.set_ylim(0,9); ax.axis("off")
ax.set_title("트럼프·푸틴·시진핑 — 세 개의 2인 게임이 겹친 3인 게임 (2026년 10월)",loc="left",fontsize=12.5,fontweight="bold",color=P)
N={"US":(5,7.4,"트럼프\n미국",BL),"CN":(8.3,2.3,"시진핑\n중국",RD),"RU":(1.7,2.3,"푸틴\n러시아",GD)}
for k,(x,y,l,c) in N.items(): ax.add_patch(Circle((x,y),.85,color=c,alpha=.95,zorder=3)); ax.text(x,y,l,ha="center",va="center",color="white",fontsize=10.5,fontweight="bold",zorder=4)
def edge(a,b,c,lab,pos,ls="-"):
    (x1,y1),(x2,y2)=N[a][:2],N[b][:2]; ax.plot([x1,x2],[y1,y2],color=c,lw=3,ls=ls,zorder=1); ax.text(*pos,lab,fontsize=8,color=TX,ha="center",va="center",bbox=dict(boxstyle="round,pad=.4",fc="white",ec=c,lw=1.2))
edge("US","CN",RD,"① 반복 관세 게임 (죄수의 딜레마형)\n관세 보복 ↔ 희토류 수출통제\n2025.10 부산 정상회담 → 1년 휴전\n2026 휴전 연장 · 기한은 짧게\n해법: 맞대응(tit-for-tat) + 짧은 계약",(7.9,5.45))
edge("US","RU",GD,"② 우크라이나 협상 게임 (내시 협상형)\n푸틴의 결렬점 = '전쟁 계속'이 견딜 만함\n트럼프의 당근 = 무역 재개\n2026.9 위트코프·쿠슈너 방러, 정상 통화\n공습은 계속 → 약속의 신뢰성 문제",(2.1,5.45),ls="--")
edge("RU","CN",GR,"③ 비대칭 연합 게임\n2026.5 베이징 · 2026.8 비슈케크(SCO)\n교역 +16.1% (1–4월, 전년비)\n러시아가 더 의존하는 동맹",(5,1.05))
ax.text(5,4.2,"중심축은 누구인가?\n\n시진핑은 트럼프(5월 방중)와\n푸틴(그 다음 주 방중)을\n일주일 간격으로 맞았다.\n두 관계를 모두 쥔 쪽이\n3인 게임의 '중심'이다.",ha="center",va="center",fontsize=8.6,color=TX,bbox=dict(boxstyle="round,pad=.6",fc="#f5f3ff",ec=P))
fig.text(.02,.015,"출처: Brookings·CFR·Bruegel(부산 휴전), Al Jazeera·NPR·Bloomberg(2026.9 우크라이나 협상), AP·Caixin(중러 정상회담·교역). 게임 분류는 해석이다.",fontsize=7.3,color=MU)
fig.subplots_adjust(bottom=.05,top=.93); fig.savefig("C_trump_putin_xi.png"); plt.close(fig)
print("ok")
