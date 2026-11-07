import json,glob,os,re,collections,random,pickle
HD=re.compile(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n(.*?)\n\s*\1\b",re.S)
def strip(c):
    c=HD.sub(' ',c)
    c=re.sub(r"python3?\s+(-I\s+)?-c\s+(\"[^\"]*\"|'[^']*')",' ',c)
    return c
CMDPOS=r"(?:^|[;&|\n(]\s*|&&\s*|\bthen\s+|\bdo\s+)"
SCHED=re.compile(r"SCHEDULER_CLI['\"]?\s+--cron\s|\"\$\{?\w*\}?\"\s+--cron\s|\$CLI['\"]?\s+--cron\s|--cron-update\s|"+CMDPOS+r"crontab\s+(?!-l|-e|-r)(-|/|~|\$|\S+)|\|\s*crontab\s+-|systemctl\s+(--user\s+)?enable\s|systemd-run\s[^\n]*--on-|"+CMDPOS+r"at\s+(now|\d)")
UNSCHED=re.compile(r"--cron-remove\s|crontab\s+-r|systemctl\s+(--user\s+)?disable\s")
SEND=re.compile(r"--sendfile\s")
LOCALHOST=r"(localhost|127\.0\.0\.1|0\.0\.0\.0)"
PUSH=re.compile(CMDPOS+r"(?:\S+=\S+\s+)*git\s+(-C\s+\S+\s+)?push\b|"+CMDPOS+r"gh\s+(pr|issue|release|repo)\s+(create|merge|comment|edit)\b|"+CMDPOS+r"gh\s+api\s[^\n]*(-X\s*(POST|PATCH|PUT|DELETE)|--method\s+(POST|PATCH|PUT|DELETE))|"+CMDPOS+r"(npm\s+publish|twine\s+upload|vercel\s+(deploy|--prod)|gcloud\s+\S+\s+deploy)")
def ext_remote(c):
    if PUSH.search(c): return True
    for m in re.finditer(CMDPOS+r"curl\b[^\n]*",c):
        s=m.group(0)
        if re.search(r"-X\s*(POST|PUT|PATCH|DELETE)|--data|\s-d\s|\s-F\s|--upload-file",s) and not re.search(LOCALHOST,s): return True
    for m in re.finditer(CMDPOS+r"(scp|rsync)\b[^\n]*",c):
        toks=m.group(0).split()
        toks=[t for t in toks if not t.startswith('-')]
        if toks and re.match(r"(\S+@)?[\w.-]+:\S*",toks[-1]): return True
    if re.search(CMDPOS+r"ssh\s[^\n]*['\"]\s*[^'\"]*\b(rm|mv|cp|systemctl|crontab|tee|mkdir)\b",c): return True
    return False
BG=re.compile(CMDPOS+r"nohup\b|"+CMDPOS+r"setsid\b|\bdisown\b|"+CMDPOS+r"tmux\s+new|docker\s+(run\s+-d|compose\s+up\s+-d)|"+CMDPOS+r"systemctl\s+(--user\s+)?(start|restart)\s|[^&|<>\d]&\s*($|\n)|[^&|<>]&\s*;|&\)\s*($|;|\n)")
LOCAL=re.compile(r"\brm\s|\bmv\s|\bcp\s|\bmkdir\b|\btouch\b|\bsed\s+-i|\bpip\s+install|\buv\s+pip|\bapt(-get)?\s+install|\bnpm\s+(i|install)\b|git\s+(commit|add|checkout|reset|merge|rebase|stash|clone|pull)\b|[^2&\d-]>>?\s*[^&\s(]|\btee\s|\bchmod\b|\bln\s")
