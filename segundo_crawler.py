from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from downloader import baixa_pdf


driver = webdriver.Chrome()
url = ''
driver.get(url)

output_file = open("links.txt", "a") 
articles = driver.find_elements(By.TAG_NAME, 'article')
print("PAGINA 01")
print(f"arquivos encontrados: {len(articles)} \n")

# Iterar sobre cada elemento <article>
for article in articles:
    h3_element = article.find_element(By.TAG_NAME, 'h3')
    href = h3_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
    print(href)
    output_file.write(href + "\n")


for pagina in range(1, 60):  # Por exemplo, navegando de 1 a 5
    # Seu código para extrair informações da página atual

    # Procurar o elemento que leva para a próxima página (botão "Próximo" ou link de paginação)
    elemento_proximos = driver.find_elements(By.XPATH, '//*[@id="paginacao"]/li[4]/button')

    # Clicar no elemento para avançar para a próxima página
    if elemento_proximos:
        elemento_proximo = elemento_proximos[0]  # Selecionar o primeiro elemento da lista
        elemento_proximo.click()
        time.sleep(10)
        articles = driver.find_elements(By.TAG_NAME, 'article')
        print(f"PAGINA {pagina}")
        print(f"arquivos encontrados: {len(articles)} \n")

        # Iterar sobre cada elemento <article>
        for article in articles:
            h3_element = article.find_element(By.TAG_NAME, 'h3')
            href = h3_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            print(href)
            output_file.write(href + "\n")
        
    else:
        print("ACABOU TUDO!!") 


baixa_pdf()