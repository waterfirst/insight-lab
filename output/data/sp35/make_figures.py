import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":["NanumBarunGothic","DejaVu Sans"],"axes.unicode_minus":False,"figure.dpi":150,"figure.facecolor":"#ffffff","axes.facecolor":"#ffffff"})
P,RD,GD,GR,TX,MU,BL="#6366f1","#ef4444","#f59e0b","#22c55e","#1a1a2e","#64748b","#3b82f6"
# NATO membership (NATO official accession dates)
steps=[(1949,12),(1952,14),(1955,15),(1982,16),(1999,19),(2004,26),(2009,28),(2017,29),(2020,30),(2023,31),(2024,32)]
xs=[s[0] for s in steps]+[2026.8]; ys=[s[1] for s in steps]+[32]
fig,ax=plt.subplots(figsize=(9,4.8))
ax.step(xs,ys,where="post",color=P,lw=2.4)
ax.fill_between(xs,ys,step="post",color="#eef2ff")
for x,y,l,ha in [(1999,19,"+3","left"),(2004,26,"+7","left"),(2009,28,"+2","left"),(2017,29,"+1","left"),(2020,30,"+1","left"),(2023,31,"핀란드 +1","right"),(2024,32,"스웨덴 +1","right")]:
    ax.text(x+(.3 if ha=="left" else -.3),y+.5,l,fontsize=8,color=P,ha=ha)
ev=[(1990,"1990 독일 통일\n구두 확약·2+4 조약",GD),(1994,"1994 부다페스트 각서",GD),(1997,"1997 나토-러시아\n기본협정",GD),(2008,"2008 부쿠레슈티\n'장차 회원국'",GD),(2014,"2014 크림 병합",RD),(2022,"2022 전면 침공",RD)]
POS={1990:(1.0,"right"),1994:(8.0,"right"),1997:(3.6,"left"),2008:(10.5,"right"),2014:(3.6,"right"),2022:(10.5,"right")}
for x,l,c in ev:
    yy,ha=POS[x]; ax.axvline(x,color=c,lw=.9,ls=":"); ax.text(x+(.4 if ha=="left" else -.4),yy,l,fontsize=7.6,color=c,ha=ha,va="bottom")
ax.axvspan(1991,1991.99,color="#fee2e2"); ax.text(1991.5,34.2,"1991 소련·바르샤바조약 해체",fontsize=7.6,color=RD,ha="center")
ax.set_xlim(1947,2027); ax.set_ylim(0,36); ax.set_ylabel("나토 회원국 수",fontsize=9)
ax.set_title("나토 회원국 수와 30년의 약속들 (1949–2026)",loc="left",fontsize=12.5,fontweight="bold",color=P)
ax.spines[["top","right"]].set_visible(False)
fig.text(.01,.01,"자료: NATO 공식 가입 연표. 2023·2024년 가입(핀란드·스웨덴)은 전면 침공 이후다.",fontsize=7.5,color=MU)
fig.tight_layout(rect=(0,.03,1,1)); fig.savefig("fig1_nato_members.png"); plt.close(fig)

# Commitment ledger
rows=[("1990","서방 → 소련","'동쪽으로 1인치도' 구두 확약","구두","논란"),
      ("1990","4대국·두 독일","2+4 조약: 구 동독에 외국군·핵 배치 제한","법적 구속","유지"),
      ("1994","러·미·영 → 우크라이나","부다페스트 각서: 핵 포기 대가 영토 보전","정치적 각서","파기"),
      ("1997","나토 ↔ 러시아","기본협정: 신규국 핵 배치 '의도 없음'·대규모 상주군 자제","정치적 선언","논란"),
      ("2008","나토 → 우크라이나·조지아","부쿠레슈티: '장차 회원국이 될 것'","정치적 선언","미이행"),
      ("2010","우크라이나 국내법","비동맹(non-bloc) 지위","국내법","폐지(2014.12)"),
      ("2015","러·우·독·불","민스크 II: 휴전·자치 일정","정치적 합의","이행 실패"),
      ("2021","러시아 → 미국·나토","조약 초안: 가입 금지·1997년 이전 배치로 복귀","요구안","거부")]
FC={"구두":"#cbd5e1","정치적 각서":"#fde68a","정치적 선언":"#fde68a","정치적 합의":"#fde68a","국내법":"#bfdbfe","법적 구속":"#bbf7d0","요구안":"#e9d5ff"}
OC={"이행 실패":RD,"유지":GR,"논란":GD,"파기":RD,"미이행":MU,"폐지(2014.12)":MU,"거부":MU}
fig,ax=plt.subplots(figsize=(9.4,5.6)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(-.6,len(rows)+.9)
hdr=[(0.05,"연도"),(0.7,"누가 누구에게"),(2.75,"약속 내용"),(7.0,"형식"),(8.6,"결과")]
for x,h in hdr: ax.text(x,len(rows)+.25,h,fontsize=9,fontweight="bold",color=TX)
for i,(y,w,c,f,o) in enumerate(rows):
    yy=len(rows)-1-i+.2
    if i%2==0: ax.add_patch(plt.Rectangle((0,yy-.42),10,.84,color="#f8fafc",zorder=0))
    ax.text(.05,yy,y,fontsize=8.6,va="center",color=TX); ax.text(.7,yy,w,fontsize=8,va="center",color=TX)
    ax.text(2.75,yy,c,fontsize=8,va="center",color=TX)
    ax.add_patch(plt.Rectangle((6.95,yy-.28),1.5,.56,color=FC[f])); ax.text(7.7,yy,f,fontsize=7.8,ha="center",va="center",color=TX)
    ax.add_patch(plt.Circle((8.72,yy),.12,color=OC[o])); ax.text(8.92,yy,o,fontsize=8,va="center",color=OC[o],fontweight="bold")
ax.set_title("약속 원장 — 8개 중 지켜진 것은 법적 구속력이 있던 하나뿐",loc="left",fontsize=12.5,fontweight="bold",color=P)
fig.text(.01,.015,"분류는 편집부 판단. '논란'은 범위·해석을 두고 양측 주장이 갈리는 경우. 출처: 미 국가안보기록보관소(NSA Archive), 각 협정 원문, Brookings·RFE/RL.",fontsize=7.3,color=MU)
fig.tight_layout(rect=(0,.03,1,1)); fig.savefig("fig2_commitment_ledger.png"); plt.close(fig)
print("ok")
