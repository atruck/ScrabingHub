import os
from lxml.html import fromstring
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import staleness_of

path = os.environ['SHUB_FIFO_PATH']
pipe = open(path, 'w')

# writer = csv.writer(open('tourneau.csv', 'wb'))
browser = webdriver.PhantomJS()

base_urls = ['http://www.tourneau.com/rolex/rolex-watches/submariner/',
'http://www.tourneau.com/rolex/rolex-watches/datejust/',
'http://www.tourneau.com/rolex/rolex-watches/datejust/?sz=18&start=18',
'http://www.tourneau.com/rolex/rolex-watches/datejust/?sz=18&start=36',
'http://www.tourneau.com/rolex/rolex-watches/datejust/?sz=18&start=54',
'http://www.tourneau.com/rolex/rolex-watches/oyster-perpetual/',
'http://www.tourneau.com/rolex/rolex-watches/pearlmaster/',
'http://www.tourneau.com/rolex/rolex-watches/pearlmaster/?sz=18&start=18',
'http://www.tourneau.com/rolex/rolex-watches/cosmograph-daytona/',
'http://www.tourneau.com/rolex/rolex-watches/sea-dweller/',
'http://www.tourneau.com/rolex/rolex-watches/gmt-master-ii/',
'http://www.tourneau.com/rolex/rolex-watches/yacht-master/',
'http://www.tourneau.com/rolex/rolex-watches/day-date/',
'http://www.tourneau.com/rolex/rolex-watches/day-date/?sz=18&start=18',
'http://www.tourneau.com/rolex/rolex-watches/sky-dweller/',
'http://www.tourneau.com/rolex/rolex-watches/explorer/',
'http://www.tourneau.com/rolex/rolex-watches/milgauss/',
'http://www.tourneau.com/rolex/rolex-watches/air-king/',
'http://www.tourneau.com/rolex/rolex-watches/cellini/',
'http://www.tourneau.com/watches/brands/tag-heuer/?sz=90',
'http://www.tourneau.com/watches/brands/tag-heuer/?sz=90&start=90',
'http://www.tourneau.com/watches/brands/tag-heuer/?sz=90&start=180',
'http://www.tourneau.com/watches/brands/omega/?sz=90',
'http://www.tourneau.com/watches/brands/citizen/?sz=90',
'http://www.tourneau.com/watches/brands/citizen/?sz=90&start=90',
'http://www.tourneau.com/watches/brands/montblanc/?sz=90',
'http://www.tourneau.com/watches/brands/hamilton/?sz=90',
'http://www.tourneau.com/watches/brands/hamilton/?sz=90&start=90',
'http://www.tourneau.com/watches/brands/iwc/?sz=90',
'http://www.tourneau.com/watches/brands/iwc/?sz=90&start=90']

product_sel = 'div.product-image > a'

brand_sel = 'span.brand'
name_sel = 'h1.product-name'
img_sel = 'img.primary-image'
price_sel = 'div.product-price'

attributes_sel = 'div.product-main-attributes > ul > li.attribute'
attribute_key_sel = 'span.label,div.label'
attribute_value_sel = 'span.value,div.value'

product_pages = []

for u in base_urls:
	try:
		browser.get(u)
		WebDriverWait(browser, 10).until(lambda browser:browser.find_element_by_css_selector(product_sel))
		product_links = browser.find_elements_by_css_selector(product_sel)
		product_pages.extend([p.get_attribute("href") for p in product_links])
	except Exception as e:
		print str(type(e).__name__) + ' scraping ' + u

print 'Retrieved ' + str(len(product_pages)) + ' product pages...'

for p in product_pages:
	try:
		browser.get(p)
		WebDriverWait(browser, 15).until(lambda browser:browser.find_element_by_css_selector(img_sel))

		brand = browser.find_element_by_css_selector(brand_sel)
		name = browser.find_element_by_css_selector(name_sel)
		imgs = browser.find_elements_by_css_selector(img_sel)
		price = browser.find_element_by_css_selector(price_sel)
		attributes = browser.find_elements_by_css_selector(attributes_sel)

		attribute_map = {}
		for a in attributes:
			try:
				key = a.find_element_by_css_selector(attribute_key_sel)
				value = a.find_element_by_css_selector(attribute_value_sel)
				attribute_map[str(key.text).encode('utf8')] = (str(value.text).encode('utf8').strip()).replace(':','')
			except NoSuchElementException:
				continue

		product_name = name.text
		if u'\u2033' in name.text:
			product_name = name.text.replace(u'\u2033', u'\"')
		if u'\u2026' in name.text:
			product_name = name.text.replace(u'\u2026', u'...')
		if u'\u2013' in name.text:
			product_name = name.text.replace(u'\u2013', u'-')
		if u'\n' in name.text:
			product_name = name.text.replace(u'\n', u' ')

		# writer.writerow([str(p).encode('utf8'),
		# 	str(brand.text).encode('utf8'),
		# 	str(product_name).encode('utf8'),
		# 	str([str(i.get_attribute("src")).encode('utf8') for i in imgs if i.get_attribute("src") is not None]),
		# 	fromstring(price.get_attribute('outerHTML')).text_content().strip().encode('utf8'),
		# 	str(attribute_map)
		# 	])

		# write item
		pipe.write('ITM {"url": "' + p + '", "brand": "' + str(brand.text).encode('utf8') + '", "name": "' + str(product_name).encode('utf8') + '", "images": "' + str([str(i.get_attribute("src")).encode('utf8') for i in imgs if i.get_attribute("src") is not None]) + '", "price": "' + fromstring(price.get_attribute('outerHTML')).text_content().strip().encode('utf8') + '", "attributes": "' + str(attribute_map) + '"}\n')
		pipe.flush()

		print 'Crawled ' + str(product_name).encode('utf8')
	except Exception as e:
		print str(type(e).__name__) + ' scraping ' + p

	# break

browser.quit()