import requests
from flask import request
import xmltodict
import json
from urllib import parse
import pymysql
import validators

KEY = 'da80e69c5efed7c11f3079ccb079cab368f8a19fb78803ada0175fdf6632135c'
#HOST = '211.217.159.196'
HOST = '127.0.0.1'
DB_NAME = 'VReading'
USER_NAME = 'PMUSR'
PASSWORD = '1234'
#DB_NAME = 'depa_dev'
#USER_NAME = 'root'
#PASSWORD = 'lpoint1!'
CHAR_SET = 'utf8'

#사서 추천 도서 조회 API
def saseoRecmd():
    drCode = request.args.get('drCode')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    startRowNum = request.args.get('startRowNum')
    endRowNum = request.args.get('endRowNum')

    res = requests.get(url='https://www.nl.go.kr/NL/search/openApi/saseoApi.do',params={'key':KEY, 'drCode':drCode, 'startDate':startDate, 'endDate':endDate, 'startRowNumApi':startRowNum, 'endRowNumApi':endRowNum})

    dictionary = xmltodict.parse(res.text)
    json_object = json.loads(json.dumps(dictionary, ensure_ascii=False)) #json 변환
    
    totalCount = json_object["channel"]["totalCount"] #조회 건수

    if totalCount == '0' : #조회되는 데이터가 없는 경우 null 리턴
        return '{"result": []}' 

    res_dict = dict(result=[])

    for val in json_object["channel"]["list"] :
        recomIsbn = val["item"]["recomisbn"]
        drCodeName = val["item"]["drCodeName"]
        publishYear = val["item"]["publishYear"]
        recomTitle = val["item"]["recomtitle"]
        recomAuthor = val["item"]["recomauthor"]
        recomPublisher = val["item"]["recompublisher"]
        recomFilePath = val["item"]["recomfilepath"]
        recomIsbn = nvl(recomIsbn,'0000000000000')
        val_dict = dict(recomIsbn=recomIsbn[0:13], kdcName=drCodeName, publishYear=publishYear, recomTitle=recomTitle, recomAuthor=recomAuthor, recomPublisher=recomPublisher, recomFilePath=recomFilePath)
        res_dict['result'].append(val_dict)

    res_dict = dict(totalCount=len(json_object["channel"]["list"]))|res_dict    

    return json.dumps(res_dict, indent="\t", ensure_ascii=False)

#도서 정보 조회 API
def bookInfo():
    if request.args.get('kwd') is None or request.args.get('kwd') == '':
        return {'result':'FAIL', 'resultMsg': 'kwd(키워드) null fail!' }

    kwd = request.args.get('kwd')

    res = requests.get(url='https://www.nl.go.kr/NL/search/openApi/search.do',params={'key':KEY, 'kwd':kwd, 'apiType':'json', 'category':'도서', 'srchTarget':request.args.get('srchTarget'), 'pageNum':request.args.get('pageNum'), 'pageSize':request.args.get('pageSize'), 'sort':request.args.get('sort'), 'order':request.args.get('order')})

    if res.json()['total'] == 0 :
        return res.json()

    res_dict = dict(total=res.json()['total'], result=[])

    for val in res.json()["result"] :
        titleInfo = val["titleInfo"]
        authorInfo = val["authorInfo"]
        pubInfo = val["pubInfo"]
        pubYearInfo = val["pubYearInfo"] 
        kdcCode = val["kdcCode1s"]
        kdcName = val["kdcName1s"]
        isbn = nvl(val["isbn"],'0000000000000')[0:13]
        if val["imageUrl"] is None or val["imageUrl"] == "" :
            imageUrl = ""
        else :
            imageUrl = "https://cover.nl.go.kr/"+val["imageUrl"]
        
        try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
        except:
                return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

        try:
            cur = conn.cursor(pymysql.cursors.DictCursor)
        except:
                return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }     

        sql = "SELECT A.STUDY_REG_NO AS studyRegNo, A.STUDY_NM AS studyNm, A.JOIN_LINK_URL AS joinLinkUrl, A.U_YN AS uYn FROM PD_TB_STUDY_MST A, PD_TB_STUDY_DTL B WHERE A.STUDY_REG_NO = B.STUDY_REG_NO AND B.ISBN = %s AND A.STUDY_REG_NO <> '1'"
        cur.execute(sql, isbn)
        studyList = cur.fetchall()
        val_dict = dict(isbn=isbn, titleInfo=titleInfo, authorInfo=authorInfo, pubInfo=pubInfo, pubYearInfo=pubYearInfo, kdcName=kdcName, imageUrl=imageUrl, studyList=studyList)
        res_dict['result'].append(val_dict)
 
    return json.dumps(res_dict, indent="\t", ensure_ascii=False)

#도서 댓글 등록 API
def bookReplyPost(isbn, crtUsid, content, password):
    if isbn is None :
        return {'result':'FAIL', 'resultMsg': 'kwd(키워드) null fail!' }
    elif crtUsid is None :
        return {'result':'FAIL', 'resultMsg': 'crtUsid(작성자) null fail!' }
    elif content is None :
        return {'result':'FAIL', 'resultMsg': 'content(내용) null fail!' }
    elif password is None :
        return {'result':'FAIL', 'resultMsg': 'password(비밀번호) null fail!' }

    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor()
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       
       
    sql = "INSERT INTO PD_TB_BOOK_REPLY_INFO (isbn, crt_Usid, content, password) VALUES(%s, %s, %s, %s)"
    vals = (isbn, crtUsid, content, password)
    cur.execute(sql, vals)
    conn.commit()
    cur.close()
    conn.close()
    return { 'result':'OK', 'resultMsg': 'database write success!' }

#도서 댓글 삭제 API
def bookReplyDelete():
    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor()
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       
    
    #댓글 삭제 비밀번호 검증
    password = request.args.get('password')
    sql = "SELECT 1 FROM PD_TB_BOOK_REPLY_INFO WHERE PASSWORD = %s"
    cur.execute(sql, password)
    res = cur.fetchone()

    if res is None or res[0] == 0 :
        cur.close()
        conn.close()
        return { 'result':'FAIL', 'resultMsg': 'password incorrect or reply doesn\'t exist' } 

    #댓글 삭제 처리
    replyRegNo = request.args.get('replyRegNo')
    sql = "DELETE FROM PD_TB_BOOK_REPLY_INFO WHERE REPLY_REG_NO = %s"
    vals = (replyRegNo)
    print(replyRegNo)
    cur.execute(sql, vals)  
    conn.commit()
    cur.close()
    conn.close()
    return { 'result':'OK', 'resultMsg': 'database delete success!' }

#도서 댓글 조회 API
def bookReplySelect():
    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor(pymysql.cursors.DictCursor)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       
    
    replyRegNo = request.args.get('replyRegNo')
    isbn = request.args.get('isbn')

    #도서댓글 등록번호와 ISBN 값이 없으면 전체 도서에 대한 댓글 조회 
    if request.args.get('replyRegNo') is None and request.args.get('isbn') is None: 
        sql = "SELECT REPLY_REG_NO replyRegNo, ISBN isbn, CRT_USID crtUsid, CONTENT content, FST_CRT_DTTI fstCrtDtti, LT_CH_DTTI ltChDtti FROM PD_TB_BOOK_REPLY_INFO"
        cur.execute(sql)

    #ISBN이 없으면 해당 도서댓글만 조회
    elif request.args.get('isbn') is None : 
        sql = "SELECT REPLY_REG_NO replyRegNo, ISBN isbn, CRT_USID crtUsid, CONTENT content, FST_CRT_DTTI fstCrtDtti, LT_CH_DTTI ltChDtti FROM PD_TB_BOOK_REPLY_INFO WHERE REPLY_REG_NO = %s"
        vals = (replyRegNo)
        cur.execute(sql, vals)

    #도서댓글등록번호가 없으면 해당 ISBN에 대한 모든 댓글 조회
    elif request.args.get('replyRegNo') is None : 
        sql = "SELECT REPLY_REG_NO replyRegNo, ISBN isbn, CRT_USID crtUsid, CONTENT content, FST_CRT_DTTI fstCrtDtti, LT_CH_DTTI ltChDtti FROM PD_TB_BOOK_REPLY_INFO WHERE ISBN = %s"
        vals = (isbn)
        cur.execute(sql, vals)

    #도서댓글등록번호와 ISBN 모두 존재하는 경우
    else : 
        sql = "SELECT REPLY_REG_NO replyRegNo, ISBN isbn, CRT_USID crtUsid, CONTENT content, FST_CRT_DTTI fstCrtDtti, LT_CH_DTTI ltChDtti FROM PD_TB_BOOK_REPLY_INFO WHERE ISBN = %s AND REPLY_REG_NO = %s"
        vals = (isbn, replyRegNo)
        cur.execute(sql, vals)    
    
           
    res = cur.fetchall()
    res_dict_list = dict(result=res)
    res_dict_total = dict(totalCount=len(res))

    res_dict = res_dict_total|res_dict_list

    #conn.commit()
    cur.close()
    conn.close()

    return json.dumps(res_dict, ensure_ascii=False, default=str)   

#도서 정보 등록 API
def bookInfoPost(isbn, bookTitle, bookTpDc, author, pubInfo, pubYear, coverUrl):
    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor()
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       
       
    sql = "INSERT INTO PD_TB_BOOK_MST (ISBN, BOOK_TITLE, BOOK_TP_DC, AUTHOR, PUB_INFO, PUB_YEAR, COVER_URL) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    vals = (isbn, bookTitle, bookTpDc, author, pubInfo, pubYear, coverUrl)
    cur.execute(sql, vals) 
    conn.commit()
    cur.close()
    conn.close()
    return { 'result':'OK', 'resultMsg': 'database write success!' }

#스터디 정보 등록 API
def studyInfoPost(studyNm, isbn, joinLinkUrl, content):
    #스터디명 또는 ISBN 또는 가입링크URL 값 없는 경우 필수값 누락 오류 리턴
    if studyNm is None or studyNm == '' :
        return {'result':'FAIL', 'resultMsg': 'studyNm(스터디명) null fail!' }
    elif isbn is None or isbn == '' :
        return {'result':'FAIL', 'resultMsg': 'isbn(국제표준도서번호) null fail!' }
    elif joinLinkUrl is None or joinLinkUrl == '' :
        return {'result':'FAIL', 'resultMsg': 'joinLinkUrl(가입링크URL) null fail!' } 
    elif content is None or content == '' :
        return {'result':'FAIL', 'resultMsg': 'content(내용) null fail!' }       

    valid = validators.url(joinLinkUrl)
    if valid != True:
        return {'result':'FAIL', 'resultMsg': '오픈채팅방 URL 형식에 맞지 않습니다.' }

    #스터디 등록 시 신청한 ISBN의 유효성 체크
    res = requests.get(url='https://www.nl.go.kr/NL/search/openApi/search.do',params={'key':KEY, 'isbn':isbn, 'apiType':'json', 'kwd':isbn, 'srchTarget':isbn, 'category':'도서'})
    
    total = res.json()['total']
    if total == 0 :
        return {'result':'FAIL', 'resultMsg': '존재하지 않는 ISBN(국제표준도서번호)'}

    #DB 연결
    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor()
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       

    #소장자료조회 API 결과값으로 도서 정보 세팅
    bookTitle = res.json()["result"][0]['titleInfo']
    bookTpDc = res.json()["result"][0]['kdcName1s']
    author = res.json()["result"][0]['authorInfo']
    pubInfo = res.json()["result"][0]['pubInfo']
    pubYear = res.json()["result"][0]['pubYearInfo']
    pubYear = pubYear[0:4]
    coverUrl = res.json()["result"][0]['imageUrl']

    #스터디 등록 시 신청한 도서를 도서_MST 테이블에 등록 (기등록된 ISBN일 경우 Ignore Insert 처리)   
    sql = "INSERT IGNORE INTO PD_TB_BOOK_MST (ISBN, BOOK_TITLE, BOOK_TP_DC, AUTHOR, PUB_INFO, PUB_YEAR, COVER_URL) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    vals = (isbn, bookTitle, bookTpDc, author, pubInfo, pubYear, coverUrl)
    cur.execute(sql, vals)
    conn.commit()
    
    #스터디 INSERT
    sql = "INSERT INTO PD_TB_STUDY_MST (STUDY_NM, JOIN_LINK_URL, CONTENT) VALUES(%s, %s, %s)"
    vals = (studyNm, joinLinkUrl, content)
    cur.execute(sql, vals)
    conn.commit()

    #등록한 스터디의 스터디등록번호(STUDY_REG_NO) SELECT
    sql = "SELECT LAST_INSERT_ID() FROM PD_TB_STUDY_MST"
    cur.execute(sql)
    lastStudyRegNo = cur.fetchone()

    #조회한 스터디등록번호와 ISBN 매핑하여 스터디 DTL 테이블에 INSERT
    sql = "INSERT INTO PD_TB_STUDY_DTL (STUDY_REG_NO, ISBN) VALUES(%s, %s)"
    vals = (lastStudyRegNo, isbn)
    cur.execute(sql, vals)
    
    conn.commit()
    cur.close()
    conn.close()
    return { 'result':'OK', 'resultMsg': 'database write success!', 'studyReg': lastStudyRegNo, 'studyNm':studyNm}

#스터디 정보 조회 API
def studyInfoSelect():
    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor(pymysql.cursors.DictCursor)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       
    
    studyRegNo = nvl(request.args.get('studyRegNo'),'')
    studyNm = nvl(request.args.get('studyNm'),'')
    adminYn = nvl(request.args.get('adminYn'),'')
    isbn = nvl(request.args.get('isbn'),'')
    sort = nvl(request.args.get('sort'),'')
    kdcName = nvl(request.args.get('kdcName'),'')
    limit = nvl(request.args.get('limit'),'')
    offset = nvl(request.args.get('offset'),'')
    titleInfo = nvl(request.args.get('titleInfo'),'')
    kwd = nvl(request.args.get('kwd'),'')

    total = ''
    where = ''
    limitCond = ''
    offsetCond = ''
    vals = ()
    if sort == 'likes' :
        orderBy = " ORDER BY LIKES DESC"
    elif sort == 'views' :
        orderBy = " ORDER BY VIEWS DESC"
    else :
        orderBy = ""

    #adminYn = Y 인 경우, studyRegNo=1 테스트덤프 데이터만 조회
    if adminYn == 'Y' :
        sql = "SELECT A.STUDY_REG_NO AS studyRegNo, A.STUDY_NM AS studyNm, A.JOIN_LINK_URL AS joinLinkUrl, A.LIKES AS likes, A.VIEWS AS views, A.U_YN AS uYn, A.CONTENT, A.FST_CRT_DTTI AS fstCrtDtti, A.LT_CH_DTTI AS ltChDtti FROM PD_TB_STUDY_MST A, PD_TB_STUDY_DTL B, PD_TB_BOOK_MST C WHERE A.STUDY_REG_NO = B.STUDY_REG_NO AND B.ISBN = C.ISBN AND A.STUDY_REG_NO = 1"
    else :
        sql = "SELECT A.STUDY_REG_NO AS studyRegNo, A.STUDY_NM AS studyNm, A.JOIN_LINK_URL AS joinLinkUrl, A.LIKES AS likes, A.VIEWS AS views, A.U_YN AS uYn, A.CONTENT, A.FST_CRT_DTTI AS fstCrtDtti, A.LT_CH_DTTI AS ltChDtti FROM PD_TB_STUDY_MST A, PD_TB_STUDY_DTL B, PD_TB_BOOK_MST C WHERE A.STUDY_REG_NO = B.STUDY_REG_NO AND B.ISBN = C.ISBN AND A.STUDY_REG_NO > 1"
        if studyRegNo :
            studyRegNo = (studyRegNo,)
            where += " AND A.STUDY_REG_NO = %s"
            vals += studyRegNo
        if studyNm :
            where += " AND A.STUDY_NM LIKE %s"
            vals += ("%" + studyNm + "%",)
        if titleInfo :
            where += " AND C.BOOK_TITLE LIKE %s"
            vals += ("%" + titleInfo + "%",)
        if kwd :
            where += " AND (C.BOOK_TITLE LIKE %s OR A.STUDY_NM LIKE %s)"
            vals += ("%" + kwd + "%", "%" + kwd + "%",)
        if isbn :
            isbn = (isbn,)
            where += " AND B.ISBN = %s"    
            vals += isbn
        if kdcName :
            kdcName = (kdcName,)
            where += " AND C.BOOK_TP_DC = %s"    
            vals += kdcName
        if limit :
            limit = int(limit)
            limit = (limit,)
            limitCond += " LIMIT %s "    
            vals += limit
        if offset :
            offset = int(offset)
            offset = (offset,)
            offsetCond += " OFFSET %s "    
            vals += offset
    total = sql + where
    sql = sql + where + orderBy + limitCond + offsetCond
    cur.execute(sql, vals)
    rows = cur.fetchall()
    res_dict = dict(result=[])
    for row in rows :
        sql = "SELECT A.ISBN AS isbn, B.BOOK_TITLE AS bookTitle, B.BOOK_TP_DC AS kdcName, B.AUTHOR AS author, B.COVER_URL AS coverUrl FROM PD_TB_STUDY_DTL A, PD_TB_BOOK_MST B WHERE A.ISBN = B.ISBN AND STUDY_REG_NO = %s"
        cur.execute(sql, row['studyRegNo'])
        isbnList = cur.fetchall()
        isbnList_dict = dict(isbnList=isbnList) 
        row = row | isbnList_dict 
        res_dict['result'].append(row)

    vals_total = list(vals)
    if offset != '':
        vals_total.pop(len(vals_total)-1)
    if limit != '':    
        vals_total.pop(len(vals_total)-1)
    cur.execute(total, vals_total)
    rows = cur.fetchall()

    res_dict = dict(totalCount=len(rows))|res_dict

    #스터디 번호로 조회했을 시에만 조회수+1 증가
    sql = "UPDATE PD_TB_STUDY_MST SET VIEWS = VIEWS+1 WHERE STUDY_REG_NO = %s AND STUDY_REG_NO <> 1"
    cur.execute(sql, studyRegNo)
    conn.commit()

    cur.close()
    conn.close()

    return json.dumps(res_dict, ensure_ascii=False, default=str)   

#테스터 카운트 업데이트 API
def testCountUpdate(): 
    try:
        conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
        return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
        cur = conn.cursor(pymysql.cursors.DictCursor)
    except:
        return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }

    sql = "UPDATE PD_TB_STUDY_MST SET VIEWS = VIEWS+1 WHERE STUDY_REG_NO = 1"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

    return {'result:':'OK', 'resultMsg': 'SUCCESS' }

#스터디 댓글 조회 API
def studyReplySelect():
    replyRegNo = nvl(request.args.get('replyRegNo'),'')
    isbn = nvl(request.args.get('isbn'),'')
    studyRegNo = nvl(request.args.get('studyRegNo'),'')
    
    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor(pymysql.cursors.DictCursor)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       

    sql = "SELECT REPLY_REG_NO replyRegNo, STUDY_REG_NO studyRegNo, ISBN isbn, CRT_USID crtUsid, CONTENT content, FST_CRT_DTTI fstCrtDtti, LT_CH_DTTI ltChDtti FROM PD_TB_STUDY_REPLY_INFO WHERE 1=1"
    where = ''
    vals = ()
    orderBy = " ORDER BY FST_CRT_DTTI DESC"

    if replyRegNo :
        replyRegNo = (replyRegNo,)
        where += " AND REPLY_REG_NO = %s"
        vals += replyRegNo
    if isbn :
        isbn = (isbn,)
        where += " AND ISBN = %s"
        vals += isbn
    if studyRegNo :
        studyRegNo = (studyRegNo,)
        where += " AND STUDY_REG_NO = %s"
        vals += studyRegNo
    
    sql = sql + where + orderBy
    cur.execute(sql, vals)
    res = cur.fetchall()
    res_dict_list = dict(result=res)

    sql = "SELECT COUNT(*) as totalCount FROM PD_TB_STUDY_REPLY_INFO WHERE 1=1"
    sql = sql + where
    cur.execute(sql, vals)
    res = cur.fetchone()
    res_dict_total = dict(res)
    res_dict = res_dict_total|res_dict_list

    cur.close()
    conn.close()

    return json.dumps(res_dict, ensure_ascii=False, default=str)     

#스터디 댓글 등록 API
def studyReplyPost(studyRegNo, isbn, crtUsid, content, password):
    if studyRegNo is None or studyRegNo == '' :
        return {'result':'FAIL', 'resultMsg': 'studyRegNo(스터디등록번호) null fail!' }
    elif crtUsid is None or crtUsid == '' :
        return {'result':'FAIL', 'resultMsg': 'crtUsid(작성자) null fail!' }
    elif content is None or content == '' :
        return {'result':'FAIL', 'resultMsg': 'content(내용) null fail!' }
    elif password is None or password == '' :
        return {'result':'FAIL', 'resultMsg': 'password(비밀번호) null fail!' }

    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor()
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       
       
    sql = "INSERT INTO PD_TB_STUDY_REPLY_INFO (study_reg_no, isbn, crt_usid, content, password) VALUES(%s, %s, %s, %s, %s)"
    vals = (studyRegNo, isbn, crtUsid, content, password)
    cur.execute(sql, vals)
    conn.commit()
    cur.close()
    conn.close()
    return { 'result':'OK', 'resultMsg': 'database write success!' }

#스터디 댓글 삭제 API
def studyReplyDelete():
    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor()
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       
    
    #댓글 삭제 비밀번호 검증
    password = request.args.get('password')
    sql = "SELECT 1 FROM PD_TB_STUDY_REPLY_INFO WHERE PASSWORD = %s"
    cur.execute(sql, password)
    res = cur.fetchone()

    if res is None or res[0] == 0 :
        cur.close()
        conn.close()
        return { 'result':'FAIL', 'resultMsg': 'password incorrect or reply doesn\'t exist' } 

    #댓글 삭제 처리
    replyRegNo = request.args.get('replyRegNo')
    sql = "DELETE FROM PD_TB_STUDY_REPLY_INFO WHERE REPLY_REG_NO = %s"
    vals = (replyRegNo)
    print(replyRegNo)
    cur.execute(sql, vals)  
    conn.commit()
    cur.close()
    conn.close()
    return { 'result':'OK', 'resultMsg': 'database delete success!' }

#스터디 좋아요 등록 API
def studyLikePost(studyRegNo):
    try:
            conn = pymysql.connect(host=HOST, user=USER_NAME, password=PASSWORD, db=DB_NAME, charset=CHAR_SET)
    except:
            return { 'result':'FAIL', 'resultMsg': 'database connection fail!' }

    try:
            cur = conn.cursor()
    except:
            return { 'result':'FAIL', 'resultMsg': 'database cursor fail!' }       
    

    #스터디 좋아요 UPDATE
    sql = "UPDATE PD_TB_STUDY_MST SET LIKES = LIKES+1 WHERE STUDY_REG_NO = %s"
    vals = (studyRegNo)
    cur.execute(sql, vals)
    conn.commit()
    cur.close()
    conn.close()
    return { 'result':'OK', 'resultMsg': 'database delete success!' }

def resultImg():
    return request.args.get('sel')

def testPage():
    page = request.args.get('page')
    if page is None or page == '':
        return ""
    else:
        return request.args.get('page')

def nvl(v, t):
    return t if v is None else v