# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import codecs

tree = ET.parse(u'D:\\剧本数据\\1.txt.xml')
root = tree.getroot()
print root.tag
print root.attrib
session_node = root[1]
previous_node = 0
query = codecs.open(u'D:\\剧本数据\\query.txt','w','utf-8')
answer = codecs.open(u'D:\\剧本数据\\answer.txt','w','utf-8')
for node in session_node:
    print node.attrib['speaker'], node.text
    if previous_node == 0:
        previous_node = node
        continue
    query.write(previous_node.text + '\n')
    answer.write(node.text + '\n')
    previous_node = node
query.close()
answer.close()
