/*** 사서 추천 도서 조회 API
01. GET 방식
02. URL 예시 : https://가치읽기.site/v1/saseoRecmd?startDate=20020401&endDate=20220601&drCode=11
03. 파라미터
    > startDate / (선택) / 검색시작일자 (예: 20020401)
    > endDate / (선택)  / 검색종료일자 (예 : 20220601)
    > drCode / (선택) / 분류번호  (11:문학, 6:인문과학, 5:사회과학 4:자연과학, 1:철학)
***/
function saseoRecmd() {
  $.ajax({
    url: "https://가치읽기.site/v1/saseoRecmd?startDate=20020401&endDate=20220601&drCode=11",
    type: "GET",
    dataType: "json",
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);

      var recomIsbn = JSON.stringify(response.result[0]["recomIsbn"]);
      console.log("recomIsbn : " + recomIsbn);

      $("#data-container").html(jsonData); //.html로 div에 값 넣을 수 있다.
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}

/*** 도서 정보 조회 API
01. GET 방식
02. URL 예시 : https://가치읽기.site/v1/book?kwd=똑게육아&pageNum=1&pageSize=20&sort=ipub_year
03. 파라미터
    > kwd / (필수) / 검색키워드
    > srchTarget / (선택) / 구체적인 검색 타겟 
      *** total (전체), title (제목), isbn (국제표준도서번호) author (저자), publisher (발행자) 생략시 전체
    > pageNum / (선택) / 현재페이지
    > pageSize / (선택) / 페이지당 출력 건수 (기본 10건)
    > sort / (선택) / 정렬기준 (생략시 : 정확도순)
      *** ititle (제목), iauthor (저자), ipublisher (발행처), ipub_year (발행년도)
***/
function bookInfo() {

  $.ajax({
    url: "https://가치읽기.site/v1/book?kwd=똑게육아&pageNum=1&pageSize=20&sort=ipub_year",
    type: "GET",
    dataType: "json",
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);
      alert("11");
      $("#data-container").html(jsonData);

      var studyList = JSON.stringify(response.result[0]["studyList"]);
      console.log("studyList : " + studyList);
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}

function bookInfo2(){
  document.getElementById("myButton").addEventListener("click", function() {
    var searchValue = document.getElementById("searchText").value;
    // 검색어 값을 가져와 변수에 저장

    var data = {
        kwd: searchValue,
        sort: "ipub_year",
        order: "desc"
    };

  $.ajax({
    url: "https://가치읽기.site/v1/book",
    type: "GET",
    dataType: "json",
    data: {"kwd": searchValue, "sort": "ipub_year", "order": "desc"},
    success: function (response) {
        var isbn = JSON.stringify(response.result[0]["isbm"]); 
        var titleInfo = JSON.stringify(response.result[0]["titleInfo"]); 
        var authorInfo = JSON.stringify(response.result[0]["authorInfo"]); 
        var pubInfo = JSON.stringify(response.result[0]["pubInfo"]); 
        var pubYearInfo = JSON.stringify(response.result[0]["pubYearInfo"]); 
        var kdcName = JSON.stringify(response.result[0]["kdcName"]); 
        var imageUrl = JSON.stringify(response.result[0]["imageUrl"]); 
        var studyList = JSON.stringify(response.result[0]["studyList"]); 

        $("#img_url").attr("src",imageUrl)
        $("#a").html(authorInfo); 

        alert("BJS");
        
    },
    error: function (error) {
        alert("통신 실패");
    },
});
  })};





/*** 도서 댓글 조회 API
01. GET 방식이므로 url에 파라미터 달고 요청 보내야한다.
02. 예시 : https://가치읽기.site/v1/book/reply?replyRegNo=1
03. 파라미터
    > isbn(선택) 국제표준도서번호
    > replyRegNo (선택) 댓글등록번호
***/
function bookReplySelect() {
  $.ajax({
    url: "https://가치읽기.site/v1/book/reply?isbn=234123412",
    type: "GET",
    dataType: "json",
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);
      $("#data-container").html(jsonData);

      var replyRegNo = JSON.stringify(response.result[0]["replyRegNo"]);
      console.log("replyRegNo : " + replyRegNo);
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}

/*** 스터디 정보 조회 API
01. GET 방식이므로 url에 파라미터 달고 요청 보내야한다.
02. 예시 : https://가치읽기.site/v1/study?studyRegNo=2&adminYn=Y
03. 파라미터
  > studyNm / (선택) / 스터디명 : LIKE 검색
  > studyRegNo / (선택) / 스터디등록번호 : 스터디번호로 조회시 조회수(views)+1 증가
  > adminYn / (선택) / 관리자여부 (Y : 무조건 테스트 스터디 조회)
***/
function studyInfoSelect() {
  $.ajax({
    url: "https://가치읽기.site/v1/study?studyNm=안녕하십니까",
    type: "GET",
    dataType: "json",
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);
      $("#data-container").html(jsonData);
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}

/*** 스터디 댓글 조회 API
01. GET 방식
02. 예시 : https://가치읽기.site/v1/study/reply?isbn=1234
03. 파라미터
  > replyRegNo / (선택) / 댓글등록번호
  > isbn / (선택) 국제표준도서번호
  > studyRegNo / (선택) 스터디등록번호
***/
function studyReplySelect() {
  $.ajax({
    url: "https://가치읽기.site/v1/study/reply",
    type: "GET",
    dataType: "json",
    success: function (response) {
      console.log(response);
      var jsonData = JSON.stringify(response);
      alert(jsonData);
      $("#data-container").html(jsonData);
    },
    error: function (error) {
      alert("통신 실패");
    },
  });
}
