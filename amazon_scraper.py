from bs4 import BeautifulSoup
from requests_html import HTMLSession
import os 
import time
import requests
from discord_webhook import DiscordWebhook

class Scraper:

    #Initializes the scraper C3PO
    def __init__(self,url,budget):

        #Attributes about product
        self.url = url
        self.budget = budget

        #Attributes about scraping
        self.session = HTMLSession()
        self.webpage = self.session.get(self.url).content
        self.parser = 'lxml'
        self.soup = BeautifulSoup(self.webpage,self.parser)

    #Prints the object
    def __str__(self):
        return self.soup.prettify()

    #Stores the title of the product
    def get_title(self):
        temp_title = self.soup.find('span',id='productTitle').text.strip()
        temp_list_title = []
        for x in temp_title:
            if x is '(':
                break
            temp_list_title.append(x)
        self.product_title = ''.join(temp_list_title)
        return self.product_title
    
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
        self.status = False
        if self.alert:
            self.status = self.send_msg()
        return self.status
    
    #Sends a message when the condition is satisfied.
    def send_msg(self):

        webhook_url = str(os.environ.get('WEBHOOK'))

        #Message details
        subject = f'The price of {self.get_title()} is within your budget!'

        body_start = 'Hey there!\n\nThe price is now within your budget. Here is the link, buy it now!\n' 
        body_mid = self.url
        body_end = '\n\nRegards\nYour friendly neighbourhood programmer'
        body = str(body_start) + str(body_mid) + str(body_end)

        message = f"Subject: {subject}\n\n{body}"

        webhook = DiscordWebhook(url=webhook_url, content=message)
        response = webhook.execute()

        print("Message sent successfully!")
        return True


def main():
    url = input("Paste the link of the Amazon product whose price you wish to monitor:")
    budget = int(input("Enter you budget price:"))
    inp_str = ("How frequuently would you like to check the price?"
               "\n1.Every hour\n2.Every 3 hours\n3.Every 6 hours"
               "\nEnter your choice(default is 6 hours):")
    time_choice = int(input(inp_str))
    if time_choice == 1:
        time_delay = 60 * 60
    elif time_choice == 2:
        time_delay = 3 * 60 * 60
    else:
        time_delay = 6 * 60 * 60
    msg = ("Great! Now just sit back and relax. Minimize this program and be sure "
            "that it is running.\nAdditionally, ensure that there is stable internet connection "
            "during the time this program runs.\nIf the price of the product falls within your budget, "
            "you will recieve a message regarding the same and this program will auto-close.\nThank you for using "
            "C3PO scraper modified by JAGUARAVI! Beep-bop bop-beep.")
    print(msg)
    c3po = Scraper(url,budget)
    while True:
        if c3po.run():
            break
        time.sleep(time_delay)

if __name__ == '__main__':
    main()
