#!/usr/bin/env python3
"""
hubmath.com MySQL dump → static HTML pages generator
"""
import re, html, sys
from pathlib import Path

DUMP     = "/mnt/d/claude/hubmath.com/hubmath-20260815.dump"
OUT      = Path("/home/claude/hubmath-site")
IMG_BASE = "http://www.hubmath.com"
IMG_NAME_SRC = "/mnt/d/claude/hubmath.com/www/files/member_extra_info/image_name"
IMG_NAME_DST = OUT / "files/member_extra_info/image_name"

# ── 1. 덤프 로드 ──────────────────────────────────────────────────────────────
print("Loading dump…", flush=True)
with open(DUMP, encoding="utf-8", errors="replace") as f:
    raw = f.read()

# ── 2. 핵심 파서: MySQL row 토크나이저 ────────────────────────────────────────
def tokenize_values(text):
    """MySQL INSERT VALUES (...),(...) 를 row 리스트로 반환"""
    rows = []
    i = 0
    n = len(text)
    while i < n:
        # 행 시작 '(' 찾기
        while i < n and text[i] != '(':
            i += 1
        if i >= n:
            break
        i += 1  # '(' skip
        row = []
        field_buf = []
        while i < n:
            c = text[i]
            if c == "'":                        # 문자열 시작
                i += 1
                while i < n:
                    c2 = text[i]
                    if c2 == '\\' and i+1 < n:  # 이스케이프
                        nxt = text[i+1]
                        mapping = {'n':'\n','r':'\r','t':'\t','\\':'\\',
                                   "'":"'",'"':'"','0':'\x00'}
                        field_buf.append(mapping.get(nxt, nxt))
                        i += 2
                    elif c2 == "'":             # 문자열 끝
                        i += 1
                        break
                    else:
                        field_buf.append(c2)
                        i += 1
                row.append(''.join(field_buf))
                field_buf = []
            elif c == 'N' and text[i:i+4] == 'NULL':
                row.append(None)
                field_buf = []
                i += 4
            elif c == ',':                      # 필드 구분자
                if field_buf:
                    row.append(''.join(field_buf).strip())
                    field_buf = []
                i += 1
            elif c == ')':                      # 행 끝
                if field_buf:
                    row.append(''.join(field_buf).strip())
                rows.append(row)
                i += 1
                break
            else:
                field_buf.append(c)
                i += 1
    return rows

def get_table_rows(table_name):
    """테이블 INSERT 블록 → rows"""
    pattern = rf"INSERT INTO `{table_name}` VALUES ([\s\S]+?);\s*\n"
    rows = []
    for m in re.finditer(pattern, raw):
        rows.extend(tokenize_values(m.group(1)))
    return rows

# ── 3. 테이블 파싱 ────────────────────────────────────────────────────────────
print("Parsing modules…", flush=True)
mod_rows = get_table_rows("smart_modules")
mid_map = {}
for r in mod_rows:
    if len(r) < 14: continue
    try:
        srl   = int(r[0]) if r[0] else 0
        mid   = str(r[8]).strip() if r[8] else ''
        title = str(r[13]).strip() if r[13] else mid
        if mid:
            mid_map[mid] = {'srl': srl, 'title': title}
    except: pass
print(f"  modules: {len(mid_map)}", flush=True)

print("Parsing documents…", flush=True)
doc_rows = get_table_rows("smart_documents")
docs_by_srl = {}
docs_by_mod = {}
for r in doc_rows:
    if len(r) < 25: continue
    try:
        # smart_documents 컬럼 순서 (CREATE TABLE 기준):
        # 0:document_srl  1:module_srl  2:category_srl  3:lang_code
        # 4:is_notice      5:title       6:title_bold    7:title_color
        # 8:content        9:readed_count 10:voted_count 11:blamed_count
        # 12:comment_count 13:trackback_count 14:uploaded_count
        # 15:password      16:user_id    17:user_name    18:nick_name
        # 19:member_srl    20:email_address 21:homepage  22:tags
        # 23:extra_vars    24:regdate    25:last_update  26:last_updater
        # 27:ipaddress     28:list_order 29:update_order 30:allow_trackback
        # 31:notify_message 32:status   33:comment_status
        srl       = int(r[0])  if r[0] else 0
        mod_srl   = int(r[1])  if r[1] else 0
        is_notice = str(r[4]).strip() if r[4] else 'N'
        title     = str(r[5])  if r[5] else '(제목없음)'
        content   = str(r[8])  if r[8] else ''
        readed    = int(r[9])  if r[9] and str(r[9]).lstrip('-').isdigit() else 0
        nick      = str(r[18]) if r[18] else '운영자'
        member_srl= int(r[19]) if r[19] and str(r[19]).lstrip('-').isdigit() else 0
        regdate   = str(r[24]) if r[24] else ''
        doc = dict(srl=srl, mod_srl=mod_srl, is_notice=is_notice,
                   title=title, content=content, nick=nick,
                   member_srl=member_srl, regdate=regdate, readed=readed)
        docs_by_srl[srl] = doc
        docs_by_mod.setdefault(mod_srl, []).append(doc)
    except Exception as e:
        pass
print(f"  documents: {len(docs_by_srl)}", flush=True)

print("Parsing comments…", flush=True)
cmt_rows = get_table_rows("smart_comments")
cmts_by_doc = {}
for r in cmt_rows:
    if len(r) < 15: continue
    try:
        # 0:comment_srl 1:module_srl 2:document_srl 3:parent_srl
        # 4:is_secret   5:content    6:voted_count  7:blamed_count
        # 8:notify_message 9:password 10:user_id   11:user_name
        # 12:nick_name  13:member_srl 14:email_address 15:homepage
        # 16:uploaded_count 17:regdate 18:last_update 19:ipaddress
        doc_srl    = int(r[2]) if r[2] else 0
        member_srl = int(r[13]) if r[13] and str(r[13]).lstrip('-').isdigit() else 0
        cmts_by_doc.setdefault(doc_srl, []).append(dict(
            srl        = int(r[0]) if r[0] else 0,
            content    = str(r[5]) if r[5] else '',
            nick       = str(r[12]) if r[12] else '익명',
            member_srl = member_srl,
            regdate    = str(r[17]) if len(r)>17 and r[17] else '',
        ))
    except: pass
print(f"  comments: {sum(len(v) for v in cmts_by_doc.values())}", flush=True)

# ── 4. 유틸 ──────────────────────────────────────────────────────────────────
def fmt_date(s):
    s = str(s).strip()
    if len(s) == 14 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    return s[:10] if len(s) >= 10 else s

def fix_img(content):
    content = re.sub(r'src="(/files/)', rf'src="{IMG_BASE}\1', content)
    content = re.sub(r'src="(/modules/)', rf'src="{IMG_BASE}\1', content)
    content = re.sub(r'src="(/common/)', rf'src="{IMG_BASE}\1', content)
    return content

def img_name_path(member_srl: int) -> str:
    """XE 이미지닉네임 파일 경로 반환 (없으면 빈 문자열)"""
    if member_srl <= 0:
        return ''
    s = str(member_srl)
    last3  = s[-3:].zfill(3)       # 예: 1345 → '345'
    prefix = str(member_srl // 1000).zfill(3)  # 예: 1345 → '001'
    path   = IMG_NAME_DST / last3 / prefix / f"{member_srl}.gif"
    if path.exists():
        return f"../files/member_extra_info/image_name/{last3}/{prefix}/{member_srl}.gif"
    return ''

def nick_html(doc: dict, root="../") -> str:
    """이미지닉네임이 있으면 img 태그, 없으면 텍스트 반환"""
    img = img_name_path(doc['member_srl'])
    if img:
        alt = html.escape(doc['nick'])
        # root 기준으로 경로 조정
        src = img.replace("../", root)
        return f'<img src="{src}" alt="{alt}" class="img-nick" title="{alt}">'
    return html.escape(doc['nick'])

# 이미지닉네임 파일 복사
import shutil, os
print("Copying image_name files…", flush=True)
if os.path.isdir(IMG_NAME_SRC):
    shutil.copytree(IMG_NAME_SRC, str(IMG_NAME_DST), dirs_exist_ok=True)
    print(f"  copied to {IMG_NAME_DST}", flush=True)

# ── 5. 메뉴 구조 (원래 hubmath.com 그대로) ───────────────────────────────────
NAV_MENU = [
    ("HOME", "index.html", [
        ("공지사항",   "pages/notice.html"),
        ("프로필",     "pages/profile.html"),
        ("다이어리",   "pages/diary.html"),
        ("끄적끄적",   "pages/daywrite.html"),
        ("추억록",     "pages/memory.html"),
        ("운영자방",   "pages/control.html"),
    ]),
    ("커뮤니티", "pages/freeboard.html", [
        ("자유게시판",       "pages/freeboard.html"),
        ("감동이 있는 글",   "pages/movingstory.html"),
        ("감동이 있는 영상", "pages/movingmovie.html"),
        ("책 그리고 이야기","pages/bookstory.html"),
        ("사람 그리고 생각","pages/people.html"),
        ("방명록",           "pages/guestbook.html"),
    ]),
    ("수학방", "pages/mathnews.html", [
        ("수학소식",    "pages/mathnews.html"),
        ("수학이야기",  "pages/mathstory.html"),
        ("묻고 답하기","pages/mathquestion.html"),
        ("수학도서",    "pages/mathbook.html"),
        ("소프트웨어",  "pages/software.html"),
        ("수학교구",    "pages/mathtool.html"),
        ("수학퍼즐",    "pages/puzzle.html"),
    ]),
    ("수학교육", "pages/mathtour.html", [
        ("교육과정 및 입시","pages/eduinfo.html"),
        ("학교수업",         "pages/schooledu.html"),
        ("수학행사",         "pages/mathtour.html"),
        ("수학체험전",       "pages/mathmake.html"),
        ("수학연수",         "pages/mathconference.html"),
        ("수학동아리",       "pages/mathclub.html"),
    ]),
    ("전공수학", "pages/majornote.html", [
        ("Math Problem of the Week","pages/pow.html"),
        ("대학수학능력시험",         "pages/mathtest.html"),
        ("전공 Q&amp;A",            "pages/mathqna.html"),
        ("전공노트",                 "pages/majornote.html"),
        ("수학저널",                 "pages/mathjournal.html"),
    ]),
    ("지식창고", "pages/livingtip.html", [
        ("생활속의 지혜","pages/livingtip.html"),
        ("홈페이지",     "pages/homepage.html"),
        ("오피스",       "pages/office.html"),
        ("Apple",        "pages/apple.html"),
        ("외국어",       "pages/language.html"),
    ]),
    ("갤러리", "pages/gallery_list.html", [
        ("자유갤러리",  "pages/gallery_list.html"),
        ("스무살 도전", "pages/pastgallery.html"),
        ("디카속으로",  "pages/webzine.html"),
        ("여행스케치",  "pages/gallery.html"),
        ("Math Art",    "pages/mathart.html"),
    ]),
    ("자료실", "pages/mathfile.html", [
        ("수학자료","pages/mathfile.html"),
        ("기타자료","pages/etcfile.html"),
    ]),
]

def build_nav(root=""):
    items = []
    for menu_name, menu_href, subs in NAV_MENU:
        href = root + menu_href
        sub_items = "".join(
            f'<li><a class="nav2nd" href="{root}{s[1]}">{s[0]}</a></li>'
            for s in subs
        )
        items.append(
            f'<li><a class="nav1st" href="{href}">{menu_name}</a>'
            f'<ul>{sub_items}</ul></li>'
        )
    return (
        '<nav id="main-nav" class="newclearfix">'
        '<ul id="sf-menu" class="sf-arrows">'
        + "".join(items) +
        '</ul></nav>'
    )

def build_footer_html(root=""):
    top = "".join(
        f'<li><a href="{root}{h}">{n}</a></li>' for n, h, _ in NAV_MENU
    )
    return f"""
  <footer id="footer" class="cameron-container newclearfix">
    <span class="footer_arrow"></span>
    <div class="line-bottom newclearfix">
      <div class="footer-l newclearfix">
        <a id="logo-bottom" href="{root}index.html"><span class="smart-logo-bottom"></span></a>
      </div>
      <div class="footer-r newclearfix">
        <nav id="bottom-nav" class="newclearfix"><ul>{top}</ul></nav>
        <ul id="contact-info">
          <li class="email"><a href="mailto:hanshin877@hanmail.net">hanshin877@hanmail.net</a></li>
        </ul>
      </div>
    </div>
  </footer>
  <footer id="copyinfo" class="cameron-container newclearfix">
    <ul><li>Copyright&copy; 2015 정현식&nbsp;&nbsp;All rights reserved.</li></ul>
  </footer>
</div>
<a href="#" id="sTop" title="Back to Top" style="display:none;">TOP</a>
<a id="TouchMe" href="#"><i class="fa fa-bars"></i></a>
<script src="{root}common/js/jquery.min.js"></script>
<script src="{root}layouts/smart/js/superfish.min.js"></script>
<script>
jQuery(document).ready(function($){{
  $('#sf-menu').superfish({{delay:200,animation:{{opacity:'show',height:'show'}},speed:'fast'}});
  $(window).scroll(function(){{ if($(this).scrollTop()>400)$('#sTop').fadeIn(); else $('#sTop').fadeOut(); }});
  $('#sTop').click(function(){{ $('html,body').animate({{scrollTop:0}},400); return false; }});
  $('#TouchMe').click(function(e){{ e.preventDefault(); $('#cameron-mobile-nav').toggleClass('open'); }});
}});
</script>
</body>
</html>"""

def page_head(title, root=""):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} - 허브수학</title>
<link rel="stylesheet" href="{root}common/css/xe.min.css">
<link rel="stylesheet" href="{root}layouts/smart/css/layout.css">
<link rel="stylesheet" href="{root}layouts/smart/fonts/nanumgothic.css">
<link rel="stylesheet" href="{root}layouts/smart/css/colorset3.css">
<link rel="stylesheet" href="{root}addons/cameron_mobile_nav/css/cameron_mobile_navr.css">
<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
<link rel="stylesheet" href="{root}css/custom.css">
<link rel="stylesheet" href="{root}css/board.css">
</head>
<body id="style-box" class="colorset3">
<p class="skipNav"><a href="#content" id="skip" tabindex="1">본문으로 바로가기</a></p>
<div id="cameron-body">
  <header id="header" class="cameron-container newclearfix">
    <a href="{root}index.html" id="logo" tabindex="2">
      <img src="{root}files/attach/images/113/9d12d70e5c7137e849b18f8c14dd3f17.gif" alt="허브수학" title="허브수학" />
    </a>
    {build_nav(root)}
  </header>"""

# ── 6. 목록 페이지 ────────────────────────────────────────────────────────────
def make_list_page(kr_name, docs, root=""):
    docs_sorted = sorted(docs, key=lambda d: d['regdate'], reverse=True)
    num = len(docs_sorted)
    rows = ""
    for doc in docs_sorted:
        notice_html = '<span class="notice-badge">공지</span>' if doc['is_notice'] == 'Y' else str(num)
        num -= 1
        rows += f"""
        <tr>
          <td class="num">{notice_html}</td>
          <td class="title"><a href="article_{doc['srl']}.html">{html.escape(doc['title'])}</a></td>
          <td class="writer">{nick_html(doc, root)}</td>
          <td class="date">{fmt_date(doc['regdate'])}</td>
          <td class="readed">{doc['readed']}</td>
        </tr>"""
    empty = '<tr><td colspan="5" class="empty">등록된 글이 없습니다.</td></tr>'
    return f"""{page_head(kr_name, root)}
  <section id="contents" class="cameron-container newclearfix">
    <header class="sub-page-header newclearfix">
      <h1 class="page-title">{html.escape(kr_name)}</h1>
    </header>
    <section class="newclearfix">
      <div id="content" class="content newclearfix">
        <div class="board-list-wrap">
          <table class="board-list">
            <colgroup>
              <col style="width:60px"><col><col style="width:80px">
              <col style="width:90px"><col style="width:60px">
            </colgroup>
            <thead><tr><th>번호</th><th>제목</th><th>글쓴이</th><th>날짜</th><th>조회</th></tr></thead>
            <tbody>{rows if rows else empty}</tbody>
          </table>
        </div>
      </div>
    </section>
  </section>
{build_footer_html(root)}"""

# ── 7. 게시글 상세 페이지 ─────────────────────────────────────────────────────
def make_article_page(doc, list_file, kr_name, root=""):
    cmts = sorted(cmts_by_doc.get(doc['srl'], []), key=lambda x: x['regdate'])
    content = fix_img(doc['content'])
    content = re.sub(r'<!--before_styler-->.*?<!--after_styler-->', '', content, flags=re.DOTALL)

    cmt_html = "".join(f"""
        <li class="comment-item">
          <div class="cmt-meta">
            <span class="cmt-nick">{html.escape(c['nick'])}</span>
            <span class="cmt-date">{fmt_date(c['regdate'])}</span>
          </div>
          <div class="cmt-body">{fix_img(c['content'])}</div>
        </li>""" for c in cmts)

    cmt_section = f"""
          <div class="comment-wrap">
            <h3 class="comment-title">댓글 {len(cmts)}개</h3>
            <ul class="comment-list">{cmt_html}</ul>
          </div>""" if cmts else ""

    return f"""{page_head(doc['title'], root)}
  <section id="contents" class="cameron-container newclearfix">
    <header class="sub-page-header newclearfix">
      <h1 class="page-title">{html.escape(kr_name)}</h1>
    </header>
    <section class="newclearfix">
      <div id="content" class="content newclearfix">
        <div class="article-wrap">
          <div class="article-head">
            <h2 class="article-title">{html.escape(doc['title'])}</h2>
            <div class="article-meta">
              <span class="writer"><i class="fa fa-user"></i> {nick_html(doc, root)}</span>
              <span class="date"><i class="fa fa-calendar"></i> {fmt_date(doc['regdate'])}</span>
              <span class="readed"><i class="fa fa-eye"></i> {doc['readed']}</span>
            </div>
          </div>
          <div class="article-body">{content}</div>
          <div class="article-foot">
            <a href="{list_file}" class="btn-list"><i class="fa fa-list"></i> 목록</a>
          </div>
          {cmt_section}
        </div>
      </div>
    </section>
  </section>
{build_footer_html(root)}"""

# ── 8. 페이지 생성 ────────────────────────────────────────────────────────────
ALL_PAGES = [
    ("notice",         "notice.html",          "공지사항"),
    ("profile",        "profile.html",         "프로필"),
    ("diary",          "diary.html",           "다이어리"),
    ("daywrite",       "daywrite.html",        "끄적끄적"),
    ("memory",         "memory.html",          "추억록"),
    ("control",        "control.html",         "운영자방"),
    ("freeboard",      "freeboard.html",       "자유게시판"),
    ("movingstory",    "movingstory.html",     "감동이 있는 글"),
    ("movingmovie",    "movingmovie.html",     "감동이 있는 영상"),
    ("bookstory",      "bookstory.html",       "책 그리고 이야기"),
    ("people",         "people.html",          "사람 그리고 생각"),
    ("guestbook",      "guestbook.html",       "방명록"),
    ("mathnews",       "mathnews.html",        "수학소식"),
    ("mathstory",      "mathstory.html",       "수학이야기"),
    ("mathquestion",   "mathquestion.html",    "묻고 답하기"),
    ("mathbook",       "mathbook.html",        "수학도서"),
    ("software",       "software.html",        "소프트웨어"),
    ("mathtool",       "mathtool.html",        "수학교구"),
    ("puzzle",         "puzzle.html",          "수학퍼즐"),
    ("eduinfo",        "eduinfo.html",         "교육과정 및 입시"),
    ("schooledu",      "schooledu.html",       "학교수업"),
    ("mathtour",       "mathtour.html",        "수학행사"),
    ("mathmake",       "mathmake.html",        "수학체험전"),
    ("mathconference", "mathconference.html",  "수학연수"),
    ("mathclub",       "mathclub.html",        "수학동아리"),
    ("pow",            "pow.html",             "Math Problem of the Week"),
    ("mathtest",       "mathtest.html",        "대학수학능력시험"),
    ("mathqna",        "mathqna.html",         "전공 Q&A"),
    ("majornote",      "majornote.html",       "전공노트"),
    ("mathjournal",    "mathjournal.html",     "수학저널"),
    ("livingtip",      "livingtip.html",       "생활속의 지혜"),
    ("homepage",       "homepage.html",        "홈페이지"),
    ("office",         "office.html",          "오피스"),
    ("apple",          "apple.html",           "Apple"),
    ("language",       "language.html",        "외국어"),
    ("list",           "gallery_list.html",    "자유갤러리"),
    ("pastgallery",    "pastgallery.html",     "스무살 도전"),
    ("webzine",        "webzine.html",         "디카속으로"),
    ("gallery",        "gallery.html",         "여행스케치"),
    ("mathart",        "mathart.html",         "Math Art"),
    ("mathfile",       "mathfile.html",        "수학자료"),
    ("etcfile",        "etcfile.html",         "기타자료"),
]

pages_dir = OUT / "pages"
pages_dir.mkdir(exist_ok=True)
root = "../"
total_docs = 0

for mid, html_file, kr_name in ALL_PAGES:
    mod_info = mid_map.get(mid)
    mod_srl  = mod_info['srl'] if mod_info else 0
    docs     = docs_by_mod.get(mod_srl, [])
    print(f"  [{mid}] srl={mod_srl} docs={len(docs)}", flush=True)

    (pages_dir / html_file).write_text(
        make_list_page(kr_name, docs, root), encoding="utf-8"
    )
    for doc in docs:
        (pages_dir / f"article_{doc['srl']}.html").write_text(
            make_article_page(doc, html_file, kr_name, root), encoding="utf-8"
        )
        total_docs += 1

# index.html 의 nav도 업데이트
print("\nUpdating index.html nav…", flush=True)
idx_path = OUT / "index.html"
idx = idx_path.read_text(encoding="utf-8")
new_nav = build_nav("")
# 기존 nav 블록 교체
idx = re.sub(r'<nav id="main-nav"[\s\S]*?</nav>', new_nav, idx, count=1)
idx_path.write_text(idx, encoding="utf-8")

print(f"\n✓ 목록 페이지: {len(ALL_PAGES)}개")
print(f"✓ 게시글 페이지: {total_docs}개")
print("Done!")
