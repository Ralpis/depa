/*** 도서 댓글 등록 API
01. POST 방식
02. URL 예시 : https://가치읽기.site/v1/book/reply
03. 파라미터
    > isbn / (필수) / 국제표준도서번호
    > crtUsid / (필수) / 작성자
    > content / (필수) / 내용
    > password / (필수) / 비밀번호
***/
function bookReplyPost() {
  var param = {};
  param.isbn = "234123412";
  param.crtUsid = "박장식";
  param.content = "재밌다~";
  param.password = "lpoint1!";

  $.ajax({
    url: "https://가치읽기.site/v1/book/reply",
    type: "POST",
    dataType: "json",
    data: param,
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);

      $("#data-container").html(jsonData); //.html로 div에 값 넣을 수 있다.
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}

/*** 스터디 댓글 등록 API
01. POST 방식
02. URL 예시 : https://가치읽기.site/v1/study/reply
03. 파라미터
    > studyRegNo / (필수) / 스터디등록번호
    > isbn / (필수) / 도서등록번호
    > crtUsid / (필수) / 작성자
    > content / (필수) / 내용
    > password / (필수) / 비밀번호
***/
function studyReplyPost() {
  var param = {};
  param.studyRegNo = "12";
  param.isbn = "2323124";
  param.crtUsid = "박장식";
  param.content = "재밌다~";
  param.password = "lpoint1!";

  $.ajax({
    url: "https://가치읽기.site/v1/study/reply",
    type: "POST",
    dataType: "json",
    data: param,
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);

      $("#data-container").html(jsonData); //.html로 div에 값 넣을 수 있다.
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}

/*** 스터디 정보 등록 API
01. POST 방식
02. URL 예시 : https://가치읽기.site/v1/study
03. 파라미터
    > studyNm / (필수) / 스터디명
    > isbn / (필수) / 국제표준도서번호
    > joinLinkUrl / (필수) / 가입링크URL
***/
function studyInfoPost() {
  var param = {};
  param.studyNm = "안녕하십니까";
  param.isbn = "9788954639002";
  param.joinLinkUrl = "https://google.com";

  $.ajax({
    url: "https://가치읽기.site//v1/study",
    type: "POST",
    dataType: "json",
    data: param,
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);

      $("#data-container").html(jsonData); //.html로 div에 값 넣을 수 있다.
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}

/*** 스터디 좋아요 등록 API
01. POST 방식
02. URL 예시 : https://가치읽기.site/v1/study/like
03. 파라미터
   > studyRegNo : 스터디 등록 번호
  
***/
function studyLikePost() {
  var param = {};
  param.studyRegNo = "3";

  $.ajax({
    url: "https://가치읽기.site/v1/study/like",
    type: "POST",
    dataType: "json",
    data: param,
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);

      $("#data-container").html(jsonData); //.html로 div에 값 넣을 수 있다.
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}

/*** 도서정보 등록 API (관리자용)
01. POST 방식
02. URL 예시 : https://가치읽기.site/v1/book
03. 파라미터
    > isbn / (선택) / 국제표준도서번호 / ex) 55
    > bookTitle / (선택) / 도서명 / ex) 222
    > bookTpDc / (선택) / 도서타입구분 / ex) 
    > author / (선택) / 저작자
    > pubInfo / (선택) / 발행정보
    > pubYear / (선택) / 발행년도
    > coverUrl / (선택) / 표지URL
***/
