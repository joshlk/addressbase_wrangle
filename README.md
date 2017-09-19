# addressbase_wrangle
Wrangle AddressBase Premium into a usable format as what [OS](https://www.ordnancesurvey.co.uk/) provide is 💩

## Useful links
* [AddressBase Support page](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/products/addressbase-premium.html)
* [AddressBase user guide](https://www.ordnancesurvey.co.uk/docs/user-guides/addressbase-products-getting-started-guide.pdf)

## Steps
Firstly order Address Base Premium from OS (it's free with restrictions):

1. Sign up to OS's [Data Exploration Licence](https://www.ordnancesurvey.co.uk/business-and-government/licensing/licences/data-exploration.html)
2. Order Address Base Premium CSV version through the [portal](https://orders.ordnancesurvey.co.uk/orders/)

Then download all files:

1. Navigate to [order download page](https://www.ordnancesurvey.co.uk/orderdownload/orders)
2. Click into the order and then save the page as a HTML using your browser and save it into the root folder of this directory
3. Make a folder called `zip_download` in root folder
4. Open a command prompt and navigate to the folder and start a `scrapy shell` ([scrapy](https://scrapy.org/) must be installed)
5. Run the following python code (subsitute the first line with the HTML file):

```python
fetch("Ordnance Survey Download Centre.html")
links = response.xpath('//*[@id="orderLinks"]/li[*]/a/@href').getall()

import urllib

for i, link in enumerate(links):
	while True:
		try:
			urllib.request.urlretrieve(link, "zip_download/{}.zip".format(i))
			break
		except:
			print("Failed: {}".format(link))
```

There are around 10,964 files so will take a couple of hours.

To exstract files:

1. Make a folder `zip_extract` in root direcotry
2. Exstract all zip files. In Windows PowerShell use `Get-ChildItem 'zip_download' -Filter *.zip | Expand-Archive -DestinationPath 'zip_extract' -Force`, on other platforms use ?
3. 
