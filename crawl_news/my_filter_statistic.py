#encoding=utf-8

import sys
import codecs
import time
import datetime
import json
import locale
import traceback

if len(sys.argv) != 2:
#if len(sys.argv) != 3:
    #sys.stderr.write("python %s crawled_file\n" % sys.argv[0])
    sys.stderr.write("python %s crawled_file\n" % sys.argv[0])
    sys.exit(1)    
    
file_name = sys.argv[1]
#content_file_name = sys.argv[2]
# file = codecs.open('%s' % file_name, 'r', encoding='utf-8')
file = open(file_name, 'r')
#content_file = open(content_file_name, 'w')

locale.setlocale(locale.LC_CTYPE, 'chinese')

count_news = {}
count_year_news = {}
except_data = []
except_data_count = 0

for line in file:
    try:
        line = line.strip()
        line = line.decode('utf-8')
        data = json.loads(line)
        post_time = data['a_post_time']
        content = data['content']
        t = time.strptime(post_time, u"%Y年%m月%d日 %H:%M")
        d = datetime.datetime(*t[:5])
        date_str = d.strftime('%Y%m%d')
        if date_str in count_news: count_news[date_str] += 1
        else: count_news[date_str] = 1
        if date_str[:4] in count_year_news: count_year_news[date_str[:4]] += 1
        else: count_year_news[date_str[:4]] = 1
        #content_file.write(content.encode('utf-8'))
        #content_file.write('\n')
    except:
        #except_data.append(line)
        except_data_count += 1
        #traceback.print_exc()
        continue

file.close()
#content_file.close()
        
sorted_count_news = sorted(count_news.iteritems(), key = lambda d: d[0])
sorted_count_news.reverse()
output = codecs.open('news_date.count', 'w+b', encoding='utf-8')
for item in sorted_count_news:
    output.write("%s\t%d\n" % (item[0], item[1]))

print "\nExcept data num: %d" % except_data_count

for year in count_year_news:
    print "%s\t%d" % (year, count_year_news[year])

