# Alexander Marshall

import re
import sys
import pprint
import requests
from statistics import mean
from bs4 import BeautifulSoup
from selenium import webdriver
import matplotlib.pyplot as plt


def get_scores(band):
    url = 'https://www.metal-archives.com/bands/'+band.replace(' ', '_')
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table = soup.find_all('tbody')[0]
    releases = table.find_all('tr')
    years = []
    scores = []

    for rel in releases:
        items = rel.find_all('td')
        if items[1].text == 'Full-length':
            year = items[2].text
            score = items[3].text
            score = re.findall('[0-9]+%', score)
            if len(score):
                score = score[0].replace('%', '')
                years.append(int(year))
                scores.append(int(score))

    driver.quit()
    return(years, scores)

def best_fit_line(xs, ys):
    xbar = sum(xs)/len(xs)
    ybar = sum(ys)/len(ys)
    n = len(xs)

    numer = sum([xi*yi for xi, yi in zip(xs, ys)]) - n * xbar * ybar
    denum = sum([xi**2 for xi in xs]) - n * xbar**2

    b = numer / denum
    a = ybar - b * xbar
    line = [a + b * xi for xi in xs]

    return line

if __name__ == '__main__':
    c = ['k', 'y', 'm', 'c', 'g', 'b', 'r']
    plt.ylim(0, 100)
    plt.xlabel('Year')
    plt.ylabel('Review Score')
    plt.title('MetalArchives User Scores')
    
    for arg in sys.argv[1:]:
        points = get_scores(arg)
        plt.scatter(points[0], points[1], color=c[-1], label=arg)
        line = best_fit_line(points[0], points[1])
        plt.plot(points[0], line, color=c[-1])
        c.pop()

    plt.legend(loc='lower left')
    plt.show()