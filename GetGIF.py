#!/usr/bin/python3
					   #	 #<-- Download Module
import urllib.request , re , time , sys , bs4 , praw , requests

#Reddit Credentials:
bot_id			= ''
secret			= ''

def Reddit(Topic , NumberOfTopics):
	TheList = list()
	reddit = praw.Reddit(client_id=bot_id,client_secret=secret,user_agent='Science News Bot')
	for submission in reddit.subreddit(Topic).hot(limit=NumberOfTopics):
		title = submission.title
		url = submission.url
		try:
			if re.search('gif$' , url):
				request = requests.get(url)
				if request.status_code == 200:
					TheInfo = (title , url)
					TheList.append(TheInfo)
				else:
					continue

			elif re.search('gifv$' , url):				
				URL = re.findall('(.*?)gifv$' , url)
				newURL = URL[0] + 'gif'
				if request.status_code == 200:
					TheInfo = (title , newURL)
					TheList.append(TheInfo)
				else:
					continue

			else:
				newURL = url + '.gif'
				request = requests.get(newURL)
				if request.status_code == 200:
					TheInfo = (title , newURL)
					TheList.append(TheInfo)
				else:
					continue
		except Exception as TheError:
			#print(TheError)
			continue
	return(TheList)
#----------------------------------------------------------------------------------------------------------------------------------
List = Reddit(sys.argv[1] , int(sys.argv[2]))

for link in List:
	try:
		response = urllib.request.urlopen(link[1])
		size = int(response.getheader('Content-Length'))/1000000
		if size < 3:
			print(size , 'MB' , '\t' , link[1] , '\t' , link[0])
			TheFile = open('GIFs' , 'a')
			TheFile.write(link[0] + '\n') #<-- Optional: Adds a text string before each URL (can be used with a twitter bot to tweet the string as title and the link as the media)
			TheFile.write(link[1] + '\n')
			TheFile.close()
		time.sleep(3)
	except Exception as TheError:
		print(TheError)
		continue
