"""SP44: 삼국사기 신라본기(권1–12) 원문 XML에서 월이 적힌 전쟁·재해·기후 기사를 뽑는다.

Usage: python3 tools/sp44_extract_samguk.py <삼국사기_unzipped 디렉터리>
Output: output/data/sp44_silla_months.json
원문: 국사편찬위원회 한국사데이터베이스 삼국사기 원문 XML (기사별 날짜·주제 분류 포함).
"""
import json, os, re, sys
import xml.etree.ElementTree as ET

SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), "..", "output", "data", "sp44_silla_months.json")
MONTH = re.compile(r"(\d{1,2})월")

def kind_of(subject):
    if subject.startswith("정치＞군사＞전쟁"):
        return "war"
    if "재해" in subject or "자연현상＞기후" in subject:
        return "weather"
    return None

records = []
for i in range(1, 13):  # 新羅本紀 第一–第十二
    path = os.path.join(SRC, f"sg_{i:03d}.xml")
    root = ET.parse(path).getroot()
    for el in root.iter():
        if el.tag.split("}")[-1] != "level3":
            continue
        d = el.find(".//{*}dateOccured")
        s = el.find(".//{*}subjectClass")
        date = d.text if d is not None else ""
        subject = s.text if s is not None else ""
        m = MONTH.search(date)
        kind = kind_of(subject)
        if m is None or kind is None:
            continue
        records.append({"file": os.path.basename(path), "id": el.get("id"),
                        "date": date, "subject": subject, "kind": kind,
                        "month": int(m.group(1))})

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"source": "삼국사기 신라본기 권1–12 원문 XML (국사편찬위원회)",
               "n_war": sum(r["kind"] == "war" for r in records),
               "n_weather": sum(r["kind"] == "weather" for r in records),
               "records": records}, f, ensure_ascii=False, indent=1)
print("wrote", OUT, len(records))
