#!/bin/bash
PAGES_DIR="/home/claude/hubmath-site/pages"
mkdir -p "$PAGES_DIR"

make_page() {
  local FILE="$PAGES_DIR/$1"
  local TITLE="$2"
  local DESC="$3"

  cat > "$FILE" << HTMLEOF
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${TITLE} - 허브수학</title>
<link rel="stylesheet" href="../common/css/xe.min.css">
<link rel="stylesheet" href="../layouts/smart/css/layout.css">
<link rel="stylesheet" href="../layouts/smart/fonts/nanumgothic.css">
<link rel="stylesheet" href="../layouts/smart/css/colorset3.css">
<link rel="stylesheet" href="../addons/cameron_mobile_nav/css/cameron_mobile_navr.css">
<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
<link rel="stylesheet" href="../css/custom.css">
</head>
<body id="style-box" class="colorset3">
<p class="skipNav"><a href="#content" id="skip" tabindex="1">본문으로 바로가기</a></p>
<div id="cameron-body">
  <header id="header" class="cameron-container newclearfix">
    <a href="../index.html" id="logo" tabindex="2">
      <img src="../files/attach/images/113/9d12d70e5c7137e849b18f8c14dd3f17.gif" alt="허브수학" title="허브수학" />
    </a>
    <nav id="main-nav" class="newclearfix">
      <ul id="sf-menu" class="sf-arrows">
        <li><a class="nav1st" href="../index.html">HOME</a><ul><li><a class="nav2nd" href="notice.html">공지사항</a></li><li><a class="nav2nd" href="profile.html">프로필</a></li><li><a class="nav2nd" href="diary.html">다이어리</a></li><li><a class="nav2nd" href="memory.html">추억록</a></li><li><a class="nav2nd" href="control.html">운영자방</a></li></ul></li>
        <li><a class="nav1st" href="freeboard.html">커뮤니티</a><ul><li><a class="nav2nd" href="freeboard.html">자유게시판</a></li><li><a class="nav2nd" href="movingstory.html">감동이 있는 글</a></li><li><a class="nav2nd" href="movingmovie.html">감동이 있는 영상</a></li><li><a class="nav2nd" href="bookstory.html">책 그리고 이야기</a></li><li><a class="nav2nd" href="people.html">사람 그리고 생각</a></li></ul></li>
        <li><a class="nav1st" href="mathnews.html">수학방</a><ul><li><a class="nav2nd" href="mathnews.html">수학소식</a></li><li><a class="nav2nd" href="mathstory.html">수학이야기</a></li><li><a class="nav2nd" href="mathquestion.html">묻고 답하기</a></li><li><a class="nav2nd" href="mathtool.html">수학교구</a></li><li><a class="nav2nd" href="puzzle.html">수학퍼즐</a></li></ul></li>
        <li><a class="nav1st" href="schooledu.html">수학교육</a><ul><li><a class="nav2nd" href="schooledu.html">학교수업</a></li><li><a class="nav2nd" href="mathmake.html">체험수학</a></li><li><a class="nav2nd" href="gifted.html">영재수학</a></li><li><a class="nav2nd" href="mathbook.html">수학도서</a></li><li><a class="nav2nd" href="software.html">수학소프트웨어</a></li></ul></li>
        <li><a class="nav1st" href="majornote.html">전공수학</a><ul><li><a class="nav2nd" href="mathqna.html">전공 Q&amp;A</a></li><li><a class="nav2nd" href="majornote.html">전공노트</a></li><li><a class="nav2nd" href="mathjournal.html">수학저널</a></li></ul></li>
        <li><a class="nav1st" href="livingtip.html">지식창고</a><ul><li><a class="nav2nd" href="livingtip.html">생활속의 지혜</a></li><li><a class="nav2nd" href="language.html">외국어</a></li><li><a class="nav2nd" href="ai.html">AI</a></li></ul></li>
        <li><a class="nav1st" href="gallery.html">갤러리</a><ul><li><a class="nav2nd" href="gallery.html">자유갤러리</a></li></ul></li>
        <li><a class="nav1st" href="mathfile.html">자료실</a><ul><li><a class="nav2nd" href="mathfile.html">수학자료</a></li><li><a class="nav2nd" href="etcfile.html">기타자료</a></li></ul></li>
      </ul>
    </nav>
  </header>

  <section id="contents" class="cameron-container newclearfix">
    <header class="sub-page-header newclearfix">
      <h1 class="page-title">${TITLE}</h1>
    </header>
    <section class="newclearfix">
      <div id="content" class="content newclearfix sub-page-wrapper">
        <div class="sub-page-notice">
          <p>${DESC}</p>
          <p style="color:#aaa;font-size:12px;margin-top:20px;">※ 이 페이지는 준비 중입니다.</p>
        </div>
      </div>
    </section>
  </section>

  <footer id="footer" class="cameron-container newclearfix">
    <span class="footer_arrow"></span>
    <div class="line-bottom newclearfix">
      <div class="footer-l newclearfix"><a id="logo-bottom" href="../index.html"><span class="smart-logo-bottom"></span></a></div>
      <div class="footer-r newclearfix">
        <nav id="bottom-nav" class="newclearfix"><ul><li><a href="../index.html">HOME</a></li><li><a href="freeboard.html">커뮤니티</a></li><li><a href="mathnews.html">수학방</a></li><li><a href="schooledu.html">수학교육</a></li><li><a href="majornote.html">전공수학</a></li><li><a href="livingtip.html">지식창고</a></li><li><a href="gallery.html">갤러리</a></li><li><a href="mathfile.html">자료실</a></li></ul></nav>
        <ul id="contact-info"><li class="email"><a href="mailto:hanshin877@hanmail.net">hanshin877@hanmail.net</a></li></ul>
      </div>
    </div>
  </footer>
  <footer id="copyinfo" class="cameron-container newclearfix">
    <ul><li>Copyright&copy; 2015 정현식&nbsp;&nbsp;All rights reserved.</li></ul>
  </footer>
</div>
<a href="#" id="sTop" title="Back to Top" style="display:none;">TOP</a>
<a id="TouchMe" href="#"><i class="fa fa-bars"></i></a>
<script src="../common/js/jquery.min.js"></script>
<script src="../layouts/smart/js/superfish.min.js"></script>
<script>
jQuery(document).ready(function($){
  $('#sf-menu').superfish({delay:200,animation:{opacity:'show',height:'show'},speed:'fast'});
  $(window).scroll(function(){ if($(this).scrollTop()>400)$('#sTop').fadeIn(); else $('#sTop').fadeOut(); });
  $('#sTop').click(function(){ $('html,body').animate({scrollTop:0},400); return false; });
  $('#TouchMe').click(function(e){ e.preventDefault(); $('#cameron-mobile-nav').toggleClass('open'); });
});
</script>
</body>
</html>
HTMLEOF
  echo "Created: $1"
}

# HOME
make_page "notice.html"      "공지사항"        "이곳은 공지사항 게시판입니다. 운영과 관련된 중요한 소식을 전달합니다."
make_page "profile.html"     "프로필"          "운영자 정현식 선생님의 소개 및 약력을 확인하실 수 있습니다."
make_page "diary.html"       "다이어리"        "일상의 생각과 기록을 담는 다이어리 공간입니다."
make_page "memory.html"      "추억록"          "소중한 추억과 기억을 담아두는 공간입니다."
make_page "control.html"     "운영자방"        "운영자 전용 공간입니다."

# 커뮤니티
make_page "freeboard.html"   "자유게시판"      "자유롭게 이야기를 나누는 공간입니다."
make_page "movingstory.html" "감동이 있는 글"  "마음을 따뜻하게 하는 감동적인 글을 모아둔 공간입니다."
make_page "movingmovie.html" "감동이 있는 영상" "감동을 주는 영상들을 모아둔 공간입니다."
make_page "bookstory.html"   "책 그리고 이야기" "책에 관한 이야기, 독서 후기를 나누는 공간입니다."
make_page "people.html"      "사람 그리고 생각" "사람과 삶에 대한 이야기, 생각을 나누는 공간입니다."

# 수학방
make_page "mathnews.html"    "수학소식"        "수학 관련 최신 뉴스와 소식을 전합니다."
make_page "mathstory.html"   "수학이야기"      "흥미로운 수학 이야기와 수학의 역사를 나누는 공간입니다."
make_page "mathquestion.html" "묻고 답하기"    "수학 관련 궁금한 점을 묻고 답하는 공간입니다."
make_page "mathtool.html"    "수학교구"        "수학 학습에 도움이 되는 교구를 소개하는 공간입니다."
make_page "puzzle.html"      "수학퍼즐"        "재미있는 수학 퍼즐을 풀어보는 공간입니다."

# 수학교육
make_page "schooledu.html"   "학교수업"        "학교 수학 수업과 관련된 자료를 공유하는 공간입니다."
make_page "mathmake.html"    "체험수학"        "수학 체험 활동 자료를 나누는 공간입니다."
make_page "gifted.html"      "영재수학"        "수학 영재 교육과 관련된 내용을 다루는 공간입니다."
make_page "mathbook.html"    "수학도서"        "수학 관련 추천 도서를 소개하는 공간입니다."
make_page "software.html"    "수학소프트웨어"  "수학 학습에 유용한 소프트웨어를 소개하는 공간입니다."

# 전공수학
make_page "mathqna.html"     "전공 Q&A"        "대학 전공수학 관련 질문과 답변을 나누는 공간입니다."
make_page "majornote.html"   "전공노트"        "전공수학 학습 노트를 공유하는 공간입니다."
make_page "mathjournal.html" "수학저널"        "수학 관련 논문과 저널을 소개하는 공간입니다."

# 지식창고
make_page "livingtip.html"   "생활속의 지혜"  "일상생활에 도움이 되는 지식과 지혜를 모아두는 공간입니다."
make_page "language.html"    "외국어"          "외국어 학습에 관련된 자료를 공유하는 공간입니다."
make_page "ai.html"          "AI"              "인공지능(AI) 관련 최신 정보와 활용 방법을 소개하는 공간입니다."

# 갤러리
make_page "gallery.html"     "자유갤러리"      "자유롭게 사진과 이미지를 공유하는 갤러리 공간입니다."

# 자료실
make_page "mathfile.html"    "수학자료"        "수학 학습에 필요한 다양한 자료를 다운로드할 수 있는 공간입니다."
make_page "etcfile.html"     "기타자료"        "수학 외 다양한 자료를 다운로드할 수 있는 공간입니다."

echo "모든 페이지 생성 완료!"
