/*** 도서 댓글 삭제 API
01. GET 방식
02. URL 예시 : http://가치읽기.site/v1/book/reply?replyRegNo=9&password=123
03. 파라미터
    > replyRegNo / (필수) / 댓글등록번호
    > password / (필수) / 비밀번호
***/
function studyReplyDelete() {
  $.ajax({
    url: "https://가치읽기.site/v1/book/reply?replyRegNo=7&password=lpoint1!",
    type: "GET",
    dataType: "json",
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

/*** 스터디 댓글 삭제 API
01. GET 방식
02. URL 예시 : http://가치읽기.site/v1/study/reply?replyRegNo=1&password=111!
03. 파라미터
    > replyRegNo / (필수) / 댓글등록번호
    > password / (필수) / 비밀번호
***/

// API가 미완성인 것 같다.
