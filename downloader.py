from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

def baixa_pdf():
    # Inicializar o driver do Chrome (ou outro navegador de sua escolha)
    driver = webdriver.Chrome()

    # Ler os links do arquivo de texto
    with open("links.txt", "r") as file:
        links = file.read().splitlines()

    for link in links:
        # Navegar para o link usando o Selenium
        driver.get(link)
        time.sleep(5)  # Aguardar um tempo para que a página seja totalmente carregada

        try:
            # Encontrar o elemento com class="download"
            download_element = driver.find_element(By.CLASS_NAME, "download")

            # Obter o atributo "href" do elemento
            download_link = download_element.get_attribute("href")

            # Usar o módulo requests para baixar o arquivo
            response = requests.get(download_link)
            
            # Extrair o nome do arquivo do URL e salvá-lo localmente
            filename = download_link.split("/")[-1]
            with open('E:/Geral/Temp/Thay/newpdfs/' + filename, "wb") as file:
                file.write(response.content)
            
            print(f"Arquivo {filename} baixado com sucesso!")

        except Exception as e:
            print(f"Erro ao baixar arquivo de {link}: {str(e)}")

    # Fechar o navegador
    driver.quit()

baixa_pdf()