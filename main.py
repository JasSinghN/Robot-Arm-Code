from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
import time
import requests
import smtplib
import csv


#Email_info(not my personal email)------------
email = 'randomemail2671@gmail.com'
password = 'R45!8282'
#---------------------------------------------

def time_rn():
    time_now = datetime.now()
    current_time = time_now.strftime("%H:%M")
    return current_time

def date_rn():
    date_now = str(date.today())
    return date_now.split('-') #[year,month,day]

def send_mail(name, price, url):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(email, password)
        subject = 'Best Price Found'
        body = f'The best price found for product: \n{name}\n --> Now is... ${str(price)}\nClick Link below:\n{url}'
        message = f'Subject:{subject}\n\n{body}'
        smtp.sendmail(email, email, message)

def record_data(rating, price):
    fout.writerow([date_rn()[0], date_rn()[1], date_rn()[2], time_rn(), price, rating])

def read_data(file_name):
    lowest_price = 1000000
    file = open(file_name, 'r')
    fin = csv.reader(file, delimiter=',')
    next(fin)
    count = 1;
    for line in fin:
        if count % 2 == 0:
            if float(line[4]) < lowest_price:
                lowest_price = float(line[4])
            count += 1
    file.close()
    return lowest_price

def main_parser(url):
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/84.0.4147.135 Safari/537.36'}
    source = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')

    name_span = soup.find('span', class_="a-size-large product-title-word-break")
    rating_span = soup.find('span', class_="reviewCountTextLinkedHistogram noUnderline")
    price_span = soup.find('span', class_="a-size-medium a-color-price priceBlockBuyingPriceString")

    name = name_span.text.strip()
    rating = float(rating_span['title'].split()[0])
    price = float(price_span.text.split()[1])
    return name, rating, price


url_outer = input("Please paste the Amazon page url link below\n-->")
file_name_outer = input("Enter File name in directory ex: 'amazon.csv'\n"
                        "If entering lowest price manually, press enter\n-->")

prog = ''
while prog != '1' and prog != '0':
    prog = input("Enter '0' if you want the script to track product data\n"
                 "Enter '1' would like to receive best price data\n-->")

sleep_time = float(input("How often do you want to the check the page for price info (enter in minutes)\n-->"))
total_time = float(input("What is the total time you want the program to run (enter in hours)\n-->"))

if prog == '0':
    file_outer = open(file_name_outer, 'a')
    fout = csv.writer(file_outer, delimiter=',')
    headings = ['Year', 'Month', 'Day', 'Time', 'price($)', 'rating(out of 5)']
    fout.writerow(headings)

    print("\nTracking...")
    name_outer = ""
    price_outer = 0
    rating_outer = 0

    initial_time = time.perf_counter()
    while (time.perf_counter()-initial_time) < (total_time*60*60):
        name_outer, rating_outer, price_outer = main_parser(url_outer)
        record_data(rating_outer, price_outer)
        time.sleep(sleep_time*60)

    file_outer.close()

else:

    try:
        lowest_price_outer = read_data(file_name_outer)

    except FileNotFoundError:
        lowest_price_outer = float(input("No file found, please enter lowest price manually below\n-->"))

    print("\nSearching...")

    initial_time = time.perf_counter()
    mail = False
    while ((time.perf_counter()-initial_time) < (total_time*60*60)) and mail == False:
        name_outer = ""
        rating_outer = 0
        price_outer = 0
        name_outer, rating_outer, price_outer = main_parser(url_outer)

        if price_outer <= lowest_price_outer:
            send_mail(name_outer, price_outer, url_outer)
            mail = True
            print("\nMail has been sent")
        else:
            time.sleep(sleep_time*60)

final_msg = f'Task completed, run time was {(time.perf_counter()-initial_time)/(60*60)} hours\nPress Enter key to exit'
leave = input(final_msg)