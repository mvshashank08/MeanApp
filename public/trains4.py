#from trains.json get the urls for the stations' details page of every train and scrape the data
import scrapy
import json
urls = json.loads(open(r'C:\Users\mvshashank08\Desktop\Scrapy Work\trains.json').read())
'''
for url in urls:
	print url['url'],"type:",type(url),"\n"
'''
class ClearTripSpider2(scrapy.Spider):
	name = "ClearTripSpider2"
	allowed_domains = ['www.cleartrip.com']

	def start_requests(self):
		for myDict in urls:
			yield scrapy.Request(myDict['url'], self.parse)
	def parse(self, response):
		stations = [];
		trainName = response.css("h1.truncate strong::text").extract()
		trainName = filterString(trainName)
		trainNo = response.css("h1.truncate small::text").extract()
		trainNo = filterString(trainNo)
		#print trainNo
		source = response.css("li.truncate:nth-child(1)::text").extract()[1]
		destination = response.css("li.truncate:nth-child(2)::text").extract()[1]
		#print source, destination
		source = filterString(source)
		destination = filterString(destination)
		#print response.css("div.resultTable.fixBody table.results tbody tr")
		for tr in response.css("div.resultTable.fixBody table.results tbody tr"):
			#print "in the for loop"
			myDict = {};
			stationName = tr.css("td:nth-child(2) a::text").extract()
			stationCode = tr.css("td:nth-child(2)::text").extract()
			arrival = tr.css("td:nth-child(3)::text").extract()
			departure = tr.css("td:nth-child(4)::text").extract()
			distanceTravelled = tr.css("td:nth-child(6)::text").extract()
			day = tr.css("td:nth-child(7)::text").extract()
			route = tr.css("td:nth-child(8)::text").extract()
			#print "Station Name:", stationName, "\nStation Code:", stationCode, "\nArrival:", arrival, "\nDeparture:", departure, "\nDistance Travelled:", distanceTravelled, "\nDay:", day, "\nRoute", route
			#adding contents to the dictionary
			myDict['stationName'] = filterString(stationName)
			myDict['stationCode'] = filterString(stationCode)
			myDict['arrival'] = filterString(arrival)
			myDict['departure'] = filterString(departure)
			myDict['distanceTravelled'] = filterString(distanceTravelled)
			myDict['day'] = filterString(day)
			myDict['route'] = filterString(route)
			#adding the dictionary to the list
			stations.append(myDict)
		yield{
			'trainName': trainName,
			'trainNumber': trainNo,
			'source': source,
			'destination': destination,
			'station': stations
		}

def filterString(myStr):
	myStr = str(myStr)
	myStr.replace("\\", "")
	myStr = myStr.replace('\t', '')
	myStr = myStr.replace('\n', '')
	myStr = myStr.replace(' ', '')
	myStr = myStr.replace('u\'', '')
	myStr = myStr.replace('\'', '')
	myStr = myStr.replace('[', '')
	myStr = myStr.replace(']', '')
	myStr = myStr.replace('(', '')
	myStr = myStr.replace(')', '')
	myStr = myStr.replace('\\n', '')
	myStr = myStr.replace('\\t', '')
	myStr = myStr.replace(',', '')
	return myStr		