import ntpath
import random



ID=""
while (ID=="" or ntpath.isfile(f"../app/data/pages/{ID}.pg")):
	ID="".join([random.choice(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")) for _ in range(5)])
s=f"""
<?xml version="1.0" encoding="utf-8"?>
<page>
	<id>{ID}</id>
	<title>TITLE</title>
	<desc>DESCRIPTION</desc>
	<labels></labels>
	<content>
	<text>
TEXT_STRING
	</text>
	</content>
</page>
"""
with open(f"../app/data/pages/{ID}.pg","w") as f:
	f.write(s[1:-1])
with open(f"../app/data/assets/{ID}.zip","w"):
	pass