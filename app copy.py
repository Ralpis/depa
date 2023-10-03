import flask                                                                                                                                      
import pymysql                                                                                                                                    
import requests                                                                                                                                   
from flask import render_template, request                                                                                                        
from flask_cors import CORS                                                                                                                       
import xmltodict                                                                                                                                  
import json                                                                                                                                       
import restApi                                                                                                                                    
                                                                                                                                                  
app = flask.Flask(__name__)                                                                                                                       
CORS(app)                                                                                                                                         
                                                                                                                                                  
@app.route('/',methods=['GET'])                                                                                                                   
def mainStart():                                                                                                                                  
    return render_template('MainPage.html')    
                                                                                                              
@app.route('/TestPage',methods=['GET'])                                                                                                                   
def testStart():                                                                                                                                 
    return render_template('TestPage'+restApi.testPage()+'.html')    
                                                                                                              
@app.route('/TestPage1',methods=['GET'])                                                                                                                   
def test2Start():                                                                                                                                  
    return render_template('TestPage1.html')

@app.route('/ApiTest',methods=['GET'])                                                                                                                   
def testApiStart():                                                                                                                                  
    return render_template('FrontTest.html')    

@app.route('/studyReg', methods=['GET'])
def studyRegView():
    return render_template('studyReg.html')

@app.route('/bookDetail', methods=['GET'])
def bookDetailView():
    return render_template('bookDetail.html')    

@app.route('/SearchPage', methods=['GET'])
def bookSearchPage():
    return render_template('SearchPage.html')

@app.route('/studydetail')
def studydetail():
    return render_template('StudyDetailPage.html')  

@app.route('/ResultPage',methods=['GET'])
def resultPage():
    return render_template('ResultPage.html',image_file ="result/result"+restApi.resultImg()+'.jpg')  

@app.route('/StudyCreatePage')
def StudyCreate():
    return render_template('StudyCreatePage.html')


#사서 추천 도서 조회 API
@app.route('/v1/saseoRecmd', methods=['GET'])
def saseoRecmd():
    return restApi.saseoRecmd()

#도서 정보 조회 API
@app.route('/v1/book', methods=['GET'])
def booksInfo():
    return restApi.bookInfo()

#도서 댓글 등록 API
@app.route('/v1/book/reply', methods=['POST'])
def bookReplyPost():
    isbn = request.form['isbn']
    crtUsid = request.form['crtUsid']
    content = request.form['content']
    password = request.form['password']
    return restApi.bookReplyPost(isbn, crtUsid, content, password)

#도서 댓글 삭제 API
@app.route('/v1/book/reply', methods=['DELETE'])
def bookReplyDelete():
    return restApi.bookReplyDelete()    

#도서 댓글 조회 API
@app.route('/v1/book/reply', methods=['GET'])
def bookReplySelect():
    return restApi.bookReplySelect()    

#도서 정보 등록 API
@app.route('/v1/book', methods=['POST'])
def bookInfoPost():
    isbn = request.form.get('isbn', '')
    bookTitle = request.form.get('bookTitle', '')
    bookTpDc = request.form.get('bookTpDc', '')
    author = request.form.get('author', '')
    pubInfo = request.form.get('pubInfo', '')
    pubYear = request.form.get('pubYear', '')
    coverUrl = request.form.get('coverUrl', '')
    return restApi.bookInfoPost(isbn, bookTitle, bookTpDc, author, pubInfo, pubYear, coverUrl)

#스터디 정보 등록 API
@app.route('/v1/study', methods=['POST'])
def studyInfoPost():
    studyNm = request.form.get('studyNm', '')
    isbn = request.form.get('isbn', '')
    joinLinkUrl = request.form.get('joinLinkUrl', '')
    return restApi.studyInfoPost(studyNm, isbn, joinLinkUrl)

#스터디 정보 조회 API
@app.route('/v1/study', methods=['GET'])
def studyInfoSelect():
    return restApi.studyInfoSelect()        

#스터디 댓글 조회 API
@app.route('/v1/study/reply', methods=['GET'])
def studyReplySelect():
    return restApi.studyReplySelect()      

#스터디 댓글 등록 API
@app.route('/v1/study/reply', methods=['POST'])
def studyReplyPost():
    studyRegNo = request.form.get('studyRegNo', '')
    isbn = request.form.get('isbn', '')
    crtUsid = request.form.get('crtUsid', '')
    content = request.form.get('content', '')
    password = request.form.get('password', '')
    return restApi.studyReplyPost(studyRegNo, isbn, crtUsid, content, password)

#스터디 댓글 삭제 API
@app.route('/v1/study/reply', methods=['DELETE'])
def studyReplyDelete():
    return restApi.studyReplyDelete()   

#스터디 좋아요 등록 API
@app.route('/v1/study/like', methods=['POST'])
def studyLikePost():
    studyRegNo = request.form.get('studyRegNo', '')
    return restApi.studyLikePost(studyRegNo)       

#app.run(debug=True)
