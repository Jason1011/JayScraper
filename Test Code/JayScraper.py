import urllib.request, os.path, os, shutil, mimetypes, re, json, argparse, pprint
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

	webContentContainer = open(path + "\\" + 'Web_Source.txt','w')
	webContentContainer.write(soup.prettify())

def getMimeType(url, path, output):

	with urllib.request.urlopen(url) as response:
		info = response.info()
		mime_type = info.get_content_type()
	return mime_type
		#if output == 'file':
		#	outfile.write("Mimetype: " + info.get_content_type())
		#else:
		#	print("Mimetype: " + info.get_content_type())
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

def webData(url, path, output):
	outer_dict = {}

	outer_dict["mime-type"] = getMimeType(url, path, output)
	outer_dict["elements"] = getElements(path, output)

	if output == 'file':
		with open(path + "\\" +'Web_Data.json', 'w') as json_file:
			json.dump(outer_dict, json_file, indent=1)	
	else:
		print(json.dumps(outer_dict, indent=1))	
	
	
def getElements(path, output):
	infilename = "Web_Source.txt"
	infile = open(path + "\\" + infilename,'r')
	lines = infile.readlines()
	
	return getElement(lines, path, output)

def getElement(lines, path, output):

	elements = []
	frequency = {}
	
	for line in lines:
		t = re.match(".*<(\\w+).*", line, re.IGNORECASE)
		if t:
			elements += [t.group(1)]
	elements.sort()
	for element in elements:
		if (element in frequency):
			frequency[element] += 1
		else: 
			frequency[element] = 1
	for key, value in frequency.items():
		("% s count: %d" % (key, value))
	return frequency

def getScripts(path, output):
	
	infilename = "Web_Source.txt"
	infile = open(path + "\\" + infilename,'r')
	str1 = " "
	theLines = (str1.join(infile))
	
	strings = re.findall(r'.*((?:<script>?|<script\s*type=[\w\W]+)[^<]+<\/script>).*', theLines, re.IGNORECASE)
	counter = 0
	string_dict = {}
	for string in strings:
		counter += 1
		cleanstring = re.sub(r'.*(<\/?\w+>?).*', "", string)
		cleanstring = cleanstring.strip()
		string_dict[counter] = cleanstring

	if output == 'file':
		with open(path + "\\" + "Script_Data.json", 'w') as json_file:
			json.dump(string_dict, json_file, indent=4)
	else:
		print(json.dumps(string_dict, indent=4))

def filesCreated(output):
	if output == 'file':
		print("Files created")
	else:
		pass

getWebPage(str(args.url), str(args.path))
print("Receiving data from webpage")
webData(str(args.url), str(args.path), str(args.output))
getScripts(str(args.path), str(args.output))
print("Webscraping Complete")




