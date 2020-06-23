import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/review', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            flipkart_url = "https://finance.yahoo.com/quote/"+ searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "W(100%)"})
            box = bigboxes[4]
            commentboxes = box.findAll("td", {"class": "Ta(end) Fw(600) Lh(14px)"})
            header = flipkart_html.findAll("div", {"class": "quote-header-section"})
            cmp = header[0]
            CompanyName = cmp.find("h1", {"class": "D(ib) Fz(16px) Lh(18px)"}).text
            Current_price = cmp.findAll("span", {"class": "Trsdu(0.3s)"})
            Price = Current_price[0].text
            Changeinprice = Current_price[1].text
            reviews = []
            m=[]
            for commentbox in commentboxes:
                try:
                    name = commentbox.span.text
                except:
                    name = 'N/A'
                m.append(name)

            # print(m)
            mydict = {"PreviousClose": m[0], "Open": m[1], "Bid": m[2], "Ask": m[3],
                      "DayRange": m[4], "Volume": m[6],
                      "AvgVolume": m[7], "MarketCap": m[8], "Beta5YMonthly": m[9], "PERatioTTM": m[10], "EPSTTM":m[11], "EarningsDate": m[12], "ForwardDividendYield": m[13], "ExDividendDate" : m[14], "Companyname": CompanyName, "price": Price,"changeinprice": Changeinprice}
            #print(mydict)
            reviews.append(mydict)
            print(reviews)
            return render_template('results.html', reviews=reviews)
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=8001, debug=True)
