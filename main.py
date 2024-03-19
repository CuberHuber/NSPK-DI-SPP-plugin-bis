from datetime import datetime
from logging import config

from selenium import webdriver

from bis import BIS
from src.spp.types import SPP_document

config.fileConfig('dev.logger.conf')

options = webdriver.ChromeOptions()
# Параметр для того, чтобы браузер не открывался.
options.add_argument('headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(options)

doc = SPP_document(id=None, title='Financialdevelopment and the effectiveness of macroprudential and capital flow management measures', abstract='This paper analyses how domestic credit and cross-border capital flows respond to macroprudential and capital flow management measures (CFMs) by using data on 39 economies during the period 2000–13. In doing so, it takes a granular approach by considering price-based and quantity-based macroprudential measures and CFMs. Further, it examines if the level of financial development impacts the effectiveness of such policy measures. This paper differs from the rest of the literature in that the empirical model simultaneously accounts for the effect of macroprudential measures and CFMs on credit dynamics and capital inflows. It also looks at the effectiveness of price-based and quantity-based macroprudential measures and CFMs separately. Finally, it accounts for potential differences in the effectiveness of such policy measures with respect to the level of financial development of countries. This is because high levels of financial development may be associated with the presence of non-bank finance, which makes it easier to circumvent macroprudential measures. We find that tightening quantity-based macroprudential measures slows down growth in total credit, domestic bank credit, corporate credit and housing credit in economies with relatively low financial development, but that tightening price-based macroprudential measures does not. In addition, both price- and quantity-based CFMs are effective in slowing bank inflows, with the former effective at all levels and the latter at relatively high levels of financial development. Finally, we find that tighter macroprudential measures are associated with larger bank or bond inflows, suggesting policy leakages. Using quarterly data on macroprudential policy (MaPP) measures and capital flow management measures (CFMs) taken by 39 economies in 2000–2013, we analyse how domestic credit and cross-border capital flows respond to such measures. In doing so, we take a granular approach by considering price-based and quantity-based MaPP measures and CFMs, and also examine if the level of financial development matters in explaining policy effectiveness. We find that quantity-based MaPP measures significantly affect total credit and its components such as domestic bank credit, corporate credit and housing credit, but that the effects fade away beyond a certain level of financial development, suggesting that highly developed financial markets provide opportunities to circumvent MaPP measures imposed on banks. We also find that both price- and quantity-based CFMs are effective in slowing down bank inflows with the former effective at all levels of financial development and the latter effective at relatively high levels. Finally, we find some evidence on the existence of leakage effects. For example, tighter overall MaPP measures are associated with larger bond inflows, and tighter quantity-based MaPP measures with larger bank inflows. JEL classification_ F34, G15, G28 Keywords_ bank lending, capital flow management measures, cross-border capital flows, financial development, macroprudential policy ', text=None, web_link='https://www.bis.org/publ/work1158.pdf', local_link=None, other_data={'author': 'Yusuf Soner Baskaya Ilhyock Shim Philip Turner '}, pub_date=datetime(2024, 1, 3, 0, 0), load_date=None)

parser = BIS(driver, 10, doc)
docs = parser.content()

print(*docs, sep='\n\r\n')
