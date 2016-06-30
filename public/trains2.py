# cleartrip.com - get only the urls of the page where the stations' details are present. trains3.py scrapes the data from the staions' details page.
import scrapy

details = []
class ClearTripSpider(scrapy.Spider):
	name = "clearTripSpider"
	start_urls = ["https://www.cleartrip.com/trains/list"]
	
	def parse(self, response):
		print "\nparse function\n"
		yield scrapy.Request(ClearTripSpider.start_urls[0], callback=self.parseLinks)
		print "\nback to parse function\n"
		'''
		print "details list:", details
		for detail in details:
			print "crawling:", detail
			yield scrapy.Request(detail, callback=self.parseDetails)
		pass
		'''
	def parseLinks(self, response):
		print "\nparseLinks function\n"
		for href in response.css("table.results tbody tr td:nth-last-child(2) a::attr(href)").extract():
			fullURL = response.urljoin(href)
			yield{
				'url': fullURL,
			}
			details.append(fullURL)
		#parsing the next page's url
		nextURL = ""
		nextURL = response.css("a.next_page::attr(href)").extract()
		nextURL = filterString(nextURL)
		
		#calling parseLinks function again
		if(nextURL):
			print "Next Page Link:",nextURL, "\n"
			nextFullURL = response.urljoin(nextURL);
			yield scrapy.Request(nextFullURL, callback=self.parseLinks)
		else:
			print "Next Page Link: NULL\n"
	def parseDetails(self, response):
		print "parse details function"
		stations = [];
		trainName = response.css("h1.truncate strong::text").extract()
		trainName = filterString(trainName)
		trainNo = response.css("h1.truncate small::text").extract()
		trainNo = filterString(trainNo)
		print trainNo
		source = response.css("li.truncate:nth-child(1)::text").extract()[1]
		destination = response.css("li.truncate:nth-child(2)::text").extract()[1]
		print source, destination
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