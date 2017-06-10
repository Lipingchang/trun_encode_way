#!/usr/local/bin/python3.6

import os
import chardet
# 学校机房的devc++只识别gb2312的文件，所以在弄过去的时候，要转码。

#检索这个文件夹下 的后缀相符的文件。
def All_Files(dirName,postfix=['.txt','.cpp','.c','.h']):
	File=[]
	Dir=[]
	for x in os.listdir(dirName):
		#判断是不是隐藏文件和后缀对不对
		extend = os.path.splitext(x)[1]
		if x[0]=='.' and not(extend in postfix): 	
			continue
		# 完整路径，判断是不是文件。
		x = os.path.join(dirName,x)		
		if os.path.isfile(x):
			File.append(x)
		else:
			Dir.append(x)

		# 把这个目录下的目录里面的东西给找出来。
		for x in Dir:
			File+=All_Files(x)

	return File


# 把一个文件转换成其他格式，要用比特的方式读入，然后写的时候也要用b，
# 不用b的话，在read的时候就会按照utf-8解码，就会抛出错误。
#TurnGDB(filename,'utf-8')
def TurnGDB(filename,tocode='gb2312'):
	# 如果 传入参数filenamae的文件存在，就执行
	if (os.path.exists(filename)) and (os.path.isfile(filename)):
		try:
			f = open(filename,'rb')
			s = f.read()
			f.close()
			enc=chardet.detect(s)
			codeType=enc['encoding']

			s = s.decode(codeType)
			s = s.encode(tocode)
			f = open(filename,'wb')
			f.write(s)
			f.close()
			print(' turn file form:(', codeType, ') to (',tocode,') successful,')
			return True
		except:
			print(' ## turning file while error happened ## ')
			return False	 
	else:
		print(" ## TurnGDB not exists error ##")
		return False


# 复制文件。
def CopyFile(fromfile,tofile):
	if (os.path.exists(fromfile)) and fromfile!=tofile and not(os.path.exists(tofile)):
		outfile = open(tofile,'wb')
		infile = open(fromfile,'rb')
		s = infile.read()
		outfile.write(s)
		outfile.close
		infile.close
		print(fromfile, " to " , tofile," copy file success")
		return True
	else:
		print(' ## copy file not exists error ##')
		return False


# fromDir 是要拷贝的， ToDir是拷贝到的地方，ToDir是要不存在的。
def CopyDir(fromDir,ToDir):
	if (os.path.exists(fromDir)) and fromDir!=ToDir and (not os.path.exists(ToDir)):
		os.mkdir(ToDir)
		print("\n\t \t making a file: ",ToDir," !!")
		for file in os.listdir(fromDir):
			if file[0]=='.':
				continue
			source = os.path.join(fromDir,file)
			target = os.path.join(ToDir,file)
			if os.path.isfile(source):
				CopyFile(source,target)
			if os.path.isdir(source):
				CopyDir(source,target)
		return True
	else:
		print(fromDir,ToDir)
		return False


currerdir = input("\ncopy dir name: ")
copyto=currerdir + '-copy'
print(currerdir," to ", copyto)
CopyDir(currerdir,copyto)

files = All_Files(copyto)
for x in files:
	TurnGDB(x)
