# addressbase_wrangle
Wrangle [AddressBase Premium](https://www.ordnancesurvey.co.uk/business-and-government/products/addressbase-premium.html) into a usable format as what [Ordnance Survey](https://www.ordnancesurvey.co.uk/) provide is 💩

## Steps
These steps require Python and two packages, [scrapy](https://scrapy.org/) and [pandas](https://pandas.pydata.org/). Installing a Python distribution like [Python Anaconda](https://www.anaconda.com/download/) is recomended.

Firstly order Address Base Premium from OS (it's free with restrictions):

1. Sign up to OS's [Data Exploration Licence](https://www.ordnancesurvey.co.uk/business-and-government/licensing/licences/data-exploration.html)
2. Order Address Base Premium as a CSV through the [portal](https://orders.ordnancesurvey.co.uk/orders/)

Then download all files:

1. Navigate to [order download page](https://www.ordnancesurvey.co.uk/orderdownload/orders)
2. Click on the order and then save the page as a HTML using your browser and save it into the root folder of this directory
3. Open a command prompt and navigate to the folder and start a `scrapy shell` ([scrapy](https://scrapy.org/) must be installed)
4. Run the following python code (substitute the first line with the HTML file):

```python
fetch("Ordnance Survey Download Centre.html")
links = response.xpath('//*[@id="orderLinks"]/li[*]/a/@href').getall()

import urllib
from urllib.parse import urlparse
import os

for i, link in enumerate(links):
    while True:
        try:
            file_name = os.path.basename(urlparse(link).path)
            urllib.request.urlretrieve(link, os.path.join("zip_download", file_name))
            break
        except:
            print("Failed: {}".format(file_name))
```

There are around 10,964 files so will take a couple of hours.

To extract and append files:

1. Extract all zip files. In Windows PowerShell use `Get-ChildItem 'zip_download' -Filter *.zip | Expand-Archive -DestinationPath 'zip_extract' -Force`, on other platforms use (? please suggest)
2. Run `python addressbase_wrangle.py` (requires [pandas](https://pandas.pydata.org/))
3. Specify the full path to the directory `zip_extract`

CSV files will be in the `output` folder.

## Useful links
* [AddressBase Support page](https://www.ordnancesurvey.co.uk/business-and-government/help-and-support/products/addressbase-premium.html)
* [AddressBase user guide](https://www.ordnancesurvey.co.uk/docs/user-guides/addressbase-products-getting-started-guide.pdf)

## Licence
This text, guide and tool is licensed under MIT (see license.txt for details), except anything that has been sourced from OS (and therefore under their own terms) which includes:

* [Header files stored in `zip_extract` directory](https://www.ordnancesurvey.co.uk/docs/product-schemas/addressbase-premium-header-files.zip)
