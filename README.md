# bvseoSpider-GUI
GUI Application for scraping certain webpages using the bvseo schema for customer review analysis
(C)2017 Stephen M. Wanser

Currently:
Enter the URL of the target web page to be scraped and click Launch. The application will launch a spider to crawl the target page and scrape the pertinent data and present it in a browsable format with a list and a detail frame. The application senses whether or not the page is formatted in the bvseo schema for customer reviews. It automatically detects the product name and all reviews contained on the page. From each review it parses the publication date, rating, rating name and the full written customer review.

Future Feature Plans:
sqlite3 database storage/retrieval, recursive domain-level crawling for products, product/brand monitoring and alerting for new reviews, sentiment analysis


