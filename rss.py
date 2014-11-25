#coding: utf-8
import requests
import re

r = requests.get('https://flashback.org/aktuella-amnen')
if r.status_code != 200:
	exit('Flashback fucked up.')

data = []

nyheter_data = re.search(r'\<a name\=\"nyheter\"\>\<\/a\>(.+?)\<\/table\>', r.text, re.DOTALL)
ovriga_data = re.search(r'\<a name\=\"ovriga\"\>\<\/a\>(.+?)\<\/table\>', r.text, re.DOTALL)

nyheter_data = re.findall(r'\<tr\>(.+?)\<\/tr\>', nyheter_data.group(0), re.DOTALL)
ovrig_data = re.findall(r'\<tr\>(.+?)\<\/tr\>', ovriga_data.group(0), re.DOTALL)

for i in [nyheter_data, ovrig_data]:
	y = False
	for x in i:
		if y:
			b = re.search(r'id\=\"thread\_title\_(.+?)\<\/a\>', x).group(1)
			title = b.split('">')[1]
			link = "https://flashback.org/t"+b.split('">')[0]
			desc = ""
			data.append([title, link, desc])
		else:
			y = True

items = ""
for item in data:
	items += """
	<item>
		<title>{}</title>
		<link>{}</link>
		<description>{}</description>
	</item>
	""".format(item[0], item[1], item[2])

end_result = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
	<title>Flashback - Aktuella ämen</title>
	<link>https://flashback.org/aktuella-amnen</link>
	<description>Yttrandesfrihet på riktigt</description>
""" + items.encode("utf-8") + """
</channel>

</rss>"""

output = open("flashback-rss.xml", "w")
output.write(end_result)
