#! /usr/bin/python
#-*-coding:gbk-*-
import os
import sys
import re

reload(sys)
sys.setdefaultencoding("gbk")


class CInjection:
	
	def __init__(self):
		self.log_file = 'E:/python/pytest/1.log'

	def CheckIn(self, files):
		if not re.search("\.php$", files):
			return False
		unsafe_var = []
		in_zhushi = False #标示内容是否在注释当中
		f = file(files, 'r')
		ff = file(self.log_file, 'a+')
		line_list = f.readlines()
		for row in range(0, len(line_list)):
			if re.search("^\s*\/\/", line_list[row]):
				continue
			elif re.search("^\s*\/\*.*?\*\/", line_list[row]):
				line_list[row] = re.sub("^\s*\/\*.*?\*\/", "", line_list[row])
			elif re.search("^\s*\/\*", line_list[row]):
				in_zhushi = True
				continue
			elif in_zhushi == True and not re.search("\*\/", line_list[row]):
				continue
			elif re.search("\*\/", line_list[row]):
				in_zhushi = False
			
			if in_zhushi == True:
				continue
			if re.search("\.php$", files) and re.search("\$[a-zA-Z0-9_]{1,}\s*=(?:\s|\w+\()*\s*\$_(POST|GET|REQUEST|COOKIE)", line_list[row], re.I):
				tmp = re.search("(\$[a-zA-Z0-9_]{1,})\s*=(?:\s|\w+\()*\s*\$_(POST|GET|REQUEST)", line_list[row], re.I)
				try:
					if tmp:
						hi = tmp.group(1)
						if not re.search("int|intval", line_list[row]):
							if hi not in unsafe_var:
								unsafe_var.append(str(hi))
						else:
							if hi in unsafe_var:
								unsafe_var.remove(hi)
				except:
					pass
			elif re.search("\.php$", files) and re.search("select.*?(?<!')\"\s*\.\s*(\$\w+)\.\s*\"", line_list[row], re.I):
				sql_tmp = re.search("select.*?(?<!')\"\s*\.\s*(\$\w+)\.\s*\"", line_list[row], re.I)
				try:
					sql_var = sql_tmp.group(1)
					if sql_var in unsafe_var:
						ff.write(files + "---line " + str(row + 1) + "：" +line_list[row] + "\r\n")
				except:
					pass
			elif re.search("\.php$", files) and re.search("select.*?(?<!')\s*\{\s*(\$\w+)\s*\}", line_list[row], re.I):
				sql_tmp = re.search("select.*?(?<!')\s*\{\s*(\$\w+)\s*\}", line_list[row], re.I)
				try:
					sql_var = sql_tmp.group(1)
					if sql_var in unsafe_var:
						ff.write(files + "---line " + str(row + 1) + "：" +line_list[row] + "\r\n")
				except:
					pass
			elif re.search("(\$\w+)\s*=\s*(.*?)\s*(\$\w+)", line_list[row], re.I):  #判断危险变量是否被赋值给别的变量
				sql_tmp = re.search("(\$\w+)\s*=\s*(.*?)\s*(\$\w+)", line_list[row], re.I)				
				try:
					other_var = sql_tmp.group(1)  #赋值之后的变量
					my_func = sql_tmp.group(2)    #处理方法 
					my_var = sql_tmp.group(3)     #原变量
					if my_var in unsafe_var:
						if my_func and not re.search("int|intval", my_func, re.I):
							unsafe_var.append(other_varr)
						elif my_func and re.search("int|intval", my_func, re.I) and my_var == other_var:  #如果危险变量在下面受过处理，则从unsafe列表中去掉
							unsafe_var.remove(my_var)
				except:
					pass
			else:
				#print line_list[row]
				pass
		f.close()
		ff.close()
		return True
	
	def getFile(self, path):
		for root, dirs, files in os.walk(path):
			for filepath in files:
				self.CheckIn(os.path.join(root, filepath))
				print 'I am doing ' + os.path.join(root, filepath) + '\r\n'



check = CInjection()
check.getFile("E:/python/pytest")

print "done.\r\n"
