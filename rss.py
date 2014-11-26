#coding: utf-8
import requests
import re

r = requests.get('https://flashback.org/aktuella-amnen')
if r.status_code != 200:
	exit('Flashback fucked up.')

data = []

nyheter_data = re.search(r'\<a name\=\"nyheter\"\>\<\/a\>(.+?)\<\/table\>', r.text, re.DOTALL).group(0).encode("utf-8")
ovriga_data = re.search(r'\<a name\=\"ovriga\"\>\<\/a\>(.+?)\<\/table\>', r.text, re.DOTALL).group(0).encode("utf-8")

nyheter_data = re.findall(r'\<tr\>(.+?)\<\/tr\>', nyheter_data, re.DOTALL)
ovrig_data = re.findall(r'\<tr\>(.+?)\<\/tr\>', ovriga_data, re.DOTALL)

for i in [nyheter_data, ovrig_data]:
	y = False
	for x in i:
		if y:
			a = re.search(r'id\=\"thread\_title\_(.+?)\<\/a\>', x).group(1)
			b = re.search(r'<a class="gentle2 forum_title" href="/f(.+?)</a>', x).group(1)
			title = a.split('">')[1]
			link = "https://flashback.org/t"+a.split('">')[0]

			category_url = b.split('">')[0]
			category = b.split('">')[1].split('</')[0]
			data.append([title, link, category_url, category])
		else:
			y = True

items = ""
for item in data:
	items += """
	<item>
		<title>{}</title>
		<link>{}</link>
		<category domain="https://www.flashback.org/f{}">{}</category>
	</item>
	""".format(item[0], item[1], item[2], item[3])

end_result = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
	<title>Flashback - Aktuella ämen</title>
	<link>https://flashback.org/aktuella-amnen</link>
	<description>Yttrandesfrihet på riktigt</description>
""" + items + """
</channel>

</rss>"""

output = open("flashback-rss.xml", "w")
output.write(end_result)
