import sqlite3 as sqlite
import time
import urllib
import zlib
import string
import os


APP_PATH = os.getcwd()

conn = sqlite.connect(APP_PATH + '/data/yelpdb.sqlite')
conn.text_factory = str #text will be returned as string not unicode (default for sqlite3)
cur = conn.cursor()

cur.execute('''SELECT content FROM Reviews WHERE business_id = ?''', ("wendys-belmont-2",))
# contents = cur.fetchall()
# print contents

counts = dict()
for review in cur :
    text = review[0]
    text = text.translate(None, string.punctuation)
    text = text.translate(None, '1234567890')
    text = text.strip()
    text = text.lower()
    words = text.split()
    for word in words:
        if len(word) < 3 : continue
        counts[word] = counts.get(word,0) + 1

# Find the top 100 words
words = sorted(counts, key=counts.get, reverse=True)
print words
highest = None
lowest = None
for w in words[:100]:
    if highest is None or highest < counts[w] :
        highest = counts[w]
    if lowest is None or lowest > counts[w] :
        lowest = counts[w]
print 'Range of counts:',highest,lowest

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('yelpWord.js','w')
fhand.write("yelpWord = [")
first = True
for k in words[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")

print "Output written to yelpWord.js"
print "Open yelpWord.htm in a browser to view"
