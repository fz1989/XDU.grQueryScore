import re
import urllib2
import urllib
import cookielib
import re
from XDUGraduateLogin import autoLogin
# http://210.27.12.1:90/queryDegreeScoreAction.do?studentid=xdleess20120514sn1585&degreecourseno=0821005

def getScore(stu, cno):
	'''获得单科的数据'''
	url = 'http://210.27.12.1:90/queryDegreeScoreAction.do?'
	#处理cookie
	cookie=cookielib.CookieJar()
	cj=urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(cj)
	#填写表单
	postdata = 'studentid=' + stu + '&degreecourseno='+cno
	req = urllib2.Request(url + postdata)
	operate = opener.open(req)
	#获得数据分析html，太麻烦了this copy from dccrazyboy
	content = operate.read()
	start = content.find('<tbody>')
	end = content.find('</tbody>')
	tbody = content[start:end]
	val = []
	while '</td>' in tbody:
		end = tbody.find('</td>')
		start = tbody.rfind('>',0,end)
		val.append(tbody[start+1:end].strip())
		tbody = tbody[end+len('</td>'):]
	return val

def getAllScore(stu,courses):
	'''获得全部的数据'''
	scores = []
	for course in courses:
		scores.append(getScore(stu,course))
	return scores

if __name__ == '__main__':
	print u'学号：'
	stuno = raw_input()
	print u'密码：'
	stupw = raw_input()
	print u'拼命登录中。。。'
	cno,sno,info = autoLogin(stuno, stupw)
	print u'登录完毕。。。'

	print u'拼命加载中。。。'
	scores = getAllScore(sno,cno)
	print u'加载完毕。。。'
	print "============================================================"
	for (k,v) in info.iteritems():
		print "%s:%s" % (k,v)
	print "============================================================"
	print u'课程名称,学分,成绩'
	for each in scores:
		if each[4]:
			print "%s,%s,%s" % (each[1],each[2],each[4])
	print "============================================================"
	raw_input(u'press anykey to exit!')
