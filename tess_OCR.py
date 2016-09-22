#!/usr/bin/env python
#coding:utf-8
#version: python3 32bit

'''
利用开源DLL，进行OCR识别
V0.1，实现了英文及数字的初步的识别
'''

import os,ctypes,sys

def getres(lang,filename):
	dllpath = os.path.dirname(os.path.abspath(__file__)) + "/tess.dll"
	envpath = os.path.dirname(os.path.abspath(__file__))
	print("envpath:", envpath)
	os.environ['TESSDATA_PREFIX'] = envpath
	TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')

	libpath = "/usr/local/lib32/"
	libpath_w = os.path.dirname(os.path.abspath(__file__))
	if not TESSDATA_PREFIX:
		print("path error")
		TESSDATA_PREFIX = "../"

	if sys.platform == "win32":
		libname = libpath_w + "/tess.dll"
		libname_alt = "tess.dll"
	else:
		libname = libpath + "tess.so.3.0.5"
		libname_alt = "tess.so.3"
	try:
		tess = ctypes.cdll.LoadLibrary(dllpath)
	except:
		try:
			tess = ctypes.cdll.LoadLibrary(libname_alt)
		except:
			print("Trying to load '%s'..." % libname)
			print("Trying to load '%s'..." % libname_alt)
			exit(1)
	tess.TessVersion.restype = ctypes.c_char_p
	tess_version = tess.TessVersion()[:4]
	print("tess_version：", tess_version)

	api = tess.TessBaseAPICreate()
	rc = tess.TessBaseAPIInit3(api, TESSDATA_PREFIX.encode(), lang.encode())

	if (rc):
		tess.TessBaseAPIDelete(api)
		print("ERROR")
		exit(3)

	tess.TessBaseAPIGetInitLanguagesAsString.restype = ctypes.c_char_p
	langs = tess.TessBaseAPIGetInitLanguagesAsString(api)

	tess.TessBaseAPIProcessPages(api, filename.encode(), None, 0, None)
	tess.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
	text_out = tess.TessBaseAPIGetUTF8Text(api)
	res2 = ctypes.c_char_p(text_out).value
	print("res:", res2)
	return (ctypes.string_at(text_out))
if __name__ == '__main__':
	filename="test2.jpg"
	lang ="eng"
	print(getres(lang,filename))


