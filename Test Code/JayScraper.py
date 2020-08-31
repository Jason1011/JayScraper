import urllib.request, os.path, os, shutil, mimetypes, re, json, argparse
from bs4 import BeautifulSoup
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Input the desired url and directory where you want the data files saved too')
parser.add_argument('-u','--url', type=str, help='url of a website')
parser.add_argument('-p','--path', type=str, help='directory path')
parser.add_argument('-o','--output', type=str, help='If you want the data in a file type file')
args = parser.parse_args()

#make ouput cooler
#def download(url):

	#response = urllib.request.urlopen(url)
	#webContent = response.read()

	#Holder = open('theWebContent.txt','wb')
	#Holder.write(webContent[0:100000])
	#Holder.close()

	#pattern = re.compile("</?\w+((\s+\w+(\s*=\s*(?:.*?|'.*?'|[\^'>\s]+))?)+\s*|\s*)/?>")

	#for i, line in enumerate(open('theWebContent.txt')):
		#for match in re.finditer(pattern, line):
			#print ('Foundon line %s: %s' % (i+1, match.group()))

	#theType = mimetypes.guess_type(url, strict=True)
	#Type = open('MIMETYPE.txt','w')
	#Type.write(str(theType))
	#Type.close()
	


#download('https://www.mountvernon.org/education/primary-sources-2/article/newburgh-address-george-washington-to-officers-of-the-army-march-15-1783/')

def getWebPage(url, path):
	
	response = urllib.request.urlopen(url)
	webContent = response.read()
	soup = BeautifulSoup(webContent, 'html.parser')

	webContentContainer = open(path + "\\" + 'Web_Data.txt','w')
	webContentContainer.write(soup.prettify())

def getMimeType(url, path, output):

	if output == 'file':
		outfilename = "MIMEtype_Data.txt"
		outfile = open(path + "\\" + outfilename,'w')
	with urllib.request.urlopen(url) as response:
		info = response.info()
		if output == 'file':
			outfile.write("Mimetype: " + info.get_content_type())
		else:
			print("Mimetype: " + info.get_content_type())
	#infilename = "Web_Data.txt"
	#infile = open(path + "\\" + infilename,'r')
	#lines = infile.readlines()
	
	#if output == 'file':
	#	outfilename = "MIMEtype_Data.txt"
	#	outfile = open(path + "\\" + outfilename,'w')
	#mimetype = False
	#for line in lines:
	#	m = re.match('.*((text/plain)|(text/csv)|(text/html)|(image/jpeg)|(image/png)|(image/svg+xml)|(video/mp4)).*', line)
	#	if m:
	#		mimetype = m.group(1)
	#if mimetype:
	#	if output == 'file':
	#		outfile.write("MIME type: " + mimetype)
	#	else:
	#		print("MIME type: " + mimetype)
	#else:
	#	if output == 'file':
	#		outfile.write("MIME type: text/html")
	#	else:
	#		print("MIME type: text/html")	

	#Another way to filer the MIMEtype
	#Type = open(outfilename,'w')
	#mimetype = False
	#flag_last = "FLAG21476147392841"
	#lines.append(flag_last)
	#flag_found = False
	#for line in lines:
		#m = re.match('.*((text/plain)|(text/csv)|(text/html)|(image/jpeg)|(image/png)|(image/svg+xml)|(video/mp4)).*', line)
		#if m:
			#Type.write("MIME type: " + m.group(1))
			#flag_found = True
		#elif line == flag_last and flag_found == False:
			#Type.write("MIME type: text/html")	

#def getElement(element, lines):

#	count = 0
#	match_string = ".*((<"+element+"+>)|(<"+element+"+)).*"
#	for line in lines:
#		t = re.match(match_string, line, re.IGNORECASE)
#		if t:
#			if t.group(1) == t.group(1):
#				count = count + 1
#	return count

def getElement(lines, path, output):

	elements = []
	frequency = {}
	for line in lines:
		t = re.match(".*<(\\w+).*", line, re.IGNORECASE)
		if t:
			elements += [t.group(1)]
	elements.sort()
	if output != 'file':
		print("Elemental Count:")
	for element in elements:
		if (element in frequency):
			frequency[element] += 1
		else: 
			frequency[element] = 1
	for key, value in frequency.items():
		("% s count: %d" % (key, value))
	if output == 'file':
		with open(path + "\\" +'Elemental_Data.json', 'w') as json_file:
			json_file.write("Elemental Count: ")
			json.dump(frequency, json_file, indent=4)
	else:
		for item, amount in frequency.items():
			print("{} count: {}".format(item, amount))
	
def getElements(path, output):
	infilename = "Web_Data.txt"
	infile = open(path + "\\" + infilename,'r')
	lines = infile.readlines()
	
	getElement(lines, path, output)

#def getContent(path):
#	infilename = "Web_Data.txt"
#	infile = open(path + "\\" + infilename,'r+')
#	lines = infile.readlines()

#	for line in lines:
#		match = re.search(r'<div.*>(.*)<\/div>', line, re.IGNORECASE)
#		if match:
#			print(match.group(1))
#			return
	

def filesCreated(output):
	if output == 'file':
		print("Files created")
	else:
		pass

#def getElements():

#	infilename = "theWebContent.txt"
#	infile = open(infilename,'r')
#	outfilename = "elementalData.txt"
#	outfile = open(outfilename,'w')
#	lines = infile.readlines()
#
#	d = []
#	match_string = "<(\w+)"
#	for line in lines:
#		m = re.match(match_string, line, re.IGNORECASE)
#		d.append(m)
#	print(d)

getWebPage(str(args.url), str(args.path))
print("Receiving data from webpage")
getMimeType(str(args.url), str(args.path), str(args.output))
filesCreated(str(args.output))
getElements(str(args.path), str(args.output))
#getContent(str(args.path))
print("Webscraping Complete")




