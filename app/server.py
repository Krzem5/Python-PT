from http.server import HTTPServer, BaseHTTPRequestHandler
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
import ntpath
import re
import shutil
import urllib
import xml.etree.ElementTree as ET



SERVER_NAME="http://569dc768.ngrok.io"
WEB_PAGE_PATH="./web/home.html"
WEB_PAGE_CSS_PATH="./web/css/main.css"
PAGES_DIR="./data/pages/"
PAGE_IFRAME_HTML_PATH="./web/page.html"
PAGE_CSS_PATH="./web/css/content.css"
HIGHLIGHT_DATA_DIR="./data/highlight/"
PAGE_JS_PATH="./web/js/content.js"
WEB_PAGE_JS_PATH="./web/js/main.js"
DOWNLOAD_DIR="./data/assets/"
PROGRGAM_EXTENSIONS="py js css html java".split(" ")
EXEC_EXTENSIONS="exe bat".split(" ")
FORMATTER=HtmlFormatter(style="native",noclasses=False,linenos=False)



def decode_tags(txt):
	o=re.sub(r"<lnk l=\"([^\"]+)\">([^<]+)</lnk>","<a class=\"lnk\" l=\"\\1\">\\2</a>",re.sub(r"<sn>([^<]+)</sn>","<span class=\"sn\">\\1</span>",txt.replace("$2","<").replace("$3",">").replace("$4","&").replace("$N","$")))
	return o



def highlight_syntax(seq,lang,file,sl=0):
	f=file.split("/")[-1]
	s=(f"<div class=\"file-header\">"+("<span class=\"r\">"+file.split("/")[0]+"</span><span class=\"o\">/</span>" if len(file.split("/"))>1 else "")+"".join(f"<span class=\"d\">{d}</span></span><span class=\"o\">/</span>" for d in file.split("/")[1:-1])+f"<span class=\"f\">"+(f.split(".")[0]+"<span class=\"f e\"><span class=\"o\">.</span>"+f.split(".")[1]+"</span>" if "." in f and f.split('.')[1] in EXEC_EXTENSIONS else (f.split(".")[0]+f"<span class=\"o\">.</span><span class=\"f{' p' if '.' in f and f.split('.')[1] in PROGRGAM_EXTENSIONS else ''}\">"+f.split(".")[1]+"</span>" if "." in f else f))+"</span></pre></div>") if file!="" else ""
	t=highlight(seq,get_lexer_by_name(lang,encoding="utf-8"),FORMATTER).replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;").replace("<div class=\"highlight\"><pre>","").replace("</pre></div>","").split("\n")
	o=""
	i=1
	for l in t:
		if (i>=len(t)-1):continue
		o+=f"<tr class=\"l\"><td class=\"ln\">{i+int(sl)}</td><td class=\"lc\"><pre class=\"code\">{l}</pre></td></tr>"
		i+=1
	return f"<div class=\"code-box {'has-header'if file!='' else ''}\">{s}<i class=\"material-icons cicon\">content_copy</i><table class=\"table\">"+o+"</table></div>"



def render_file_view(txt):
	def render(d,i=0,p=""):
		o=""
		for k in d["dirs"].keys():
			tp=p+"/"+k
			o+="<span class=\"vl\">&nbsp;&nbsp;&nbsp;&nbsp;</span>"*i+(f"<i class=\"material-icons a s\" data-path=\"{tp[1:]}\">play_arrow</i>" if i>0 else "")+f"<span class=\"{'d' if i>0 else 'r'}\">{k}</span><span class=\"o\" data-path=\"{tp[1:]}\">:</span>\n<div class=\"go\" data-path=\"{tp[1:]}\"><div class=\"g\" data-path=\"{tp[1:]}\">"+render(d["dirs"][k],i=i+1,p=tp)+"</div></div>"
		for f in d["files"]:
			o+="<span class=\"vl\">&nbsp;&nbsp;&nbsp;&nbsp;</span>"*i+f"<span class=\"f\">"+(f.split(".")[0]+"<span class=\"f e\"><span class=\"o\">.</span>"+f.split(".")[1]+"</span>" if "." in f and f.split('.')[1] in EXEC_EXTENSIONS else (f.split(".")[0]+f"<span class=\"o\">.</span><span class=\"f {' p' if '.' in f and f.split('.')[1] in PROGRGAM_EXTENSIONS else ''}\">"+f.split(".")[1]+"</span>" if "." in f else f))+"</span>\n"
		return o
	d={"dirs":{},"files":[]}
	for s in txt.split(";"):
		s=re.sub(r"\n|\t|\s","",s)
		if (s==""):continue
		s=s.split("/")
		p=""
		for dr in s:
			t=d
			for k in p[1:].split("/"):
				if (k==""):continue
				t=t["dirs"][k]
			if (dr==s[-1]):
				t["files"]+=[dr]
				t["files"]=sorted(t["files"])
				continue
			if (dr not in t["dirs"].keys()):
				t["dirs"][dr]={"dirs":{},"files":[]}
				t["dirs"]={k:v for (k,v) in sorted(t["dirs"].items())}
			p+=f"/{dr}"
	return "<div class=\"file-view\"><pre class=\"view\">"+render(d)+"</pre></div>"



def render_content(xml):
	o="<div class=\"content\">"
	for c in xml:
		if (c.tag=="text"):
			t=decode_tags(c.text[1:]).replace("\n","<br>")
			o+=f"<p class=\"text\">{t}</p>"
		elif (c.tag=="code"):
			o+=highlight_syntax(decode_tags(re.sub(r"^([\t\s]+\n)","",re.sub(r"(\n[\t\s]+)$","",c.text))),c.attrib["lang"],c.attrib["file"] if "file" in c.attrib.keys() else "",c.attrib["sl"] if "sl" in c.attrib.keys() else 0)
		elif (c.tag=="file-view"):
			o+=render_file_view(decode_tags(c.text))
		elif (c.tag=="dir"):
			c.text=re.sub(r"\n|\t|\s","",c.text)
			f=c.text.split("/")[-1]
			o+=f"<div class=\"dir-view\"><pre class=\"dir\">"+("<span class=\"r\">"+c.text.split("/")[0]+"</span><span class=\"o\">/</span>" if len(c.text.split("/"))>1 else "")+"".join(f"<span class=\"d\">{d}</span></span><span class=\"o\">/</span>" for d in c.text.split("/")[1:-1])+f"<span class=\"f\">"+(f.split(".")[0]+"<span class=\"f e\"><span class=\"o\">.</span>"+f.split(".")[1]+"</span>" if "." in f and f.split('.')[1] in EXEC_EXTENSIONS else (f.split(".")[0]+f"<span class=\"o\">.</span><span class=\"f {' p' if '.' in f and f.split('.')[1] in PROGRGAM_EXTENSIONS else ''}\">"+f.split(".")[1]+"</span>" if "." in f else f))+"</span></pre></div>"
		else:
			print("Unknown tag: "+c.tag)
	return o+"</div>"



def render_page(ID):
	def format(s,**f):
		for k in f.keys():
			s=s.replace(f"${k}$",f[k])
		return s.replace("\\$","$")
	with open(WEB_PAGE_PATH,"r") as f:
		wpage=f.read()
	with open(PAGE_IFRAME_HTML_PATH,"r") as f:
		page=f.read()
	with open(PAGE_CSS_PATH,"r") as f:
		css=f.read()
	with open(WEB_PAGE_CSS_PATH,"r") as f:
		wcss=f.read()
	with open(PAGE_JS_PATH,"r") as f:
		js=f.read()
	with open(WEB_PAGE_JS_PATH,"r") as f:
		wjs=f.read()
	with open(f"{PAGES_DIR}{ID}.pg","r") as f:
		xml=ET.fromstring(f.read())
	d={}
	if (ntpath.isfile(DOWNLOAD_DIR+ID+".zip")):
		d["download"]=SERVER_NAME+DOWNLOAD_DIR+ID+".zip"
	for c in xml:
		if (c.tag=="id"):
			d["id"]=c.text
		elif (c.tag=="title"):
			d["title"]=c.text
		elif (c.tag=="desc"):
			d["desc"]=c.text
		elif (c.tag=="labels"):
			d["labels"]=c.text
		elif (c.tag=="content"):
			d["content"]=render_content(c)
	c="data:text/html,"+urllib.parse.quote(format(page,js=js,css=css,id=d["id"],title=decode_tags(d["title"]),desc=decode_tags(d["desc"]),labels=d["labels"],download=d["download"],content=d["content"]),safe="~()*!.'")
	html=format(wpage,js=wjs,css=wcss,name=ID,contentsrc=c)
	return bytes(html,"utf-8")



class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		if (re.match(r"/[a-zA-Z]{5}",self.path) and ntpath.isfile(f"{PAGES_DIR}{self.path[1:]}.pg")):
			self.send_response(200)
			self.send_header("Content-type","text/html")
			self.end_headers()
			self.wfile.write(render_page(self.path[1:]))
		elif (self.path.endswith(".zip")):
			self.send_response(200)
			self.send_header("Content-type","text/plain")
			self.end_headers()
			shutil.copyfileobj(open("."+self.path,"rb"),self.wfile)
		else:
			self.send_error(404,message="File not found")



with HTTPServer(("localhost",8000),Handler) as httpd:
	print("Start")
	httpd.serve_forever()