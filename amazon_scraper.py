from bs4 import BeautifulSoup
from requests_html import HTMLSession
import os 
import smtplib , ssl
import requests

class Scraper:

    #Initializes the scraper C3PO
    def __init__(self,url,budget,u_email):
        self.url = url
        self.budget = budget

        context = ssl.create_default_context()
        port = 587
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', port, context=context)
        self.email = str(os.environ.get('DEVELOPER_MAIL'))
        self.app_pw = str(os.environ.get('DEVELOPER_PASS'))
        self.u_email = u_email
        
        self.session = HTMLSession()
        self.webpage = self.session.get(self.url).content
        self.parser = 'lxml'
        self.soup = BeautifulSoup(self.webpage,self.parser)

    #Prints the object
    def __str__(self):
        return self.soup.prettify()

    #Stores the title of the product
    def get_title(self):
        self.product_title = self.soup.find('span',id='productTitle').text.strip()
        return
    
    #Stores the price of the product after filtering the string and converting it to an integer
    def get_price(self):
        price_raw = self.soup.find('span',id='priceblock_ourprice').text.strip()
        price_filtered = price_raw[2:len(price_raw)-3]
        self.product_price = int(''.join([x for x in price_filtered if x is not ',']))
        return
    
    #Prints product title
    def print_title(self):
        print(self.product_title)
        return        

    #Prints product price
    def print_price(self):
        print(self.product_price)
        return

    #Checks if the price of the product is below the budget
    def is_below_budget(self):
        if self.product_price <= self.budget:
            return True
        else:
            return False
    
    #Runs the scraper
    def run(self):
        self.get_title()
        self.get_price()
        self.alert = self.is_below_budget()
        if self.alert:
            self.send_email()
        return
    
    def send_email(self):
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.email,self.app_pw)

        subject = 'The price of the product is within your budget!'

        body = self.url

        message = f"Subject: {subject}\n\n{body}"

        self.server.sendmail(self.email,self.u_email,message)

        print("Email sent successfully!")
        self.server.quit()
        return


def main():
    url = input("Paste the link of the Amazon product whose price you wish to monitor:")
    budget = int(input("Enter you budget price:"))
    u_email = input("Enter your email:")
    c3po = Scraper(url,budget,u_email)
    c3po.run()

if __name__ == '__main__':
    main()