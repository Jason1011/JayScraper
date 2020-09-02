import urllib.request, os.path, os, shutil, mimetypes, re, json, argparse, pprint, sys
from bs4 import BeautifulSoup
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Input the desired url and directory where you want the data files saved too')
parser.add_argument('-u','--url', type=str, required=True, help='url of a website')
parser.add_argument('-p','--path', type=str, required=True, help='directory path')
parser.add_argument('-f','--file',  default=False, action='store_true', help='create files')
args = parser.parse_args()

def getWebPage(url, path):
	
	response = urllib.request.urlopen(url)
	webContent = response.read()
	soup = BeautifulSoup(webContent, 'html.parser')

	webContentContainer = open(path + 'Web_Source.txt','w')
	webContentContainer.write(soup.prettify())

def getMimeType(url, path, output):

	with urllib.request.urlopen(url) as response:
		info = response.info()
		mime_type = info.get_content_type()
	return mime_type
		

def webData(url, path, output):
	outer_dict = {}

	outer_dict["mime-type"] = getMimeType(url, path, output)
	outer_dict["elements"] = getElements(path, output)

	if output == True:
		with open(path + 'Web_Data.json', 'w') as json_file:
			json.dump(outer_dict, json_file, indent=1)	
	else:
		print(json.dumps(outer_dict, indent=1))	
	
	
def getElements(path, output):
	infilename = "Web_Source.txt"
	infile = open(path + infilename,'r')
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
	infile = open(path + infilename,'r')
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

	if output == True:
		with open(path + "Script_Data.json", 'w') as json_file:
			json.dump(string_dict, json_file, indent=4)
	else:
		print(json.dumps(string_dict, indent=4))

def filesCreated(output):
	if output == True:
		print("Files created")
	else:
		pass

def jayScraper(url, path, output):
	print("Receiving data from webpage")
	getWebPage(url, path)
	webData(url, path, output)
	getScripts(path, output)
	filesCreated(output)
	print("Webscraping Complete")

jayScraper(str(args.url), str(args.path), (args.file))




