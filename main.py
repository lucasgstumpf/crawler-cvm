import PyPDF2
import re
import csv
import os

# Diretório onde os arquivos PDF estão localizados
diretorio = 'E:/Geral/Temp/Thay/newpdfs/'

# Lista para armazenar os dados extraídos de todos os arquivos PDF
dados_totais = []
output_file = open("errados.txt", "a") 

# Loop pelos arquivos PDF no diretório
for arquivo_pdf in os.listdir(diretorio):
    if arquivo_pdf.endswith(".pdf"): # == 'SP2012228_AROUCH_Invest.pdf': #.endswith(".pdf"):
        pdf_path = os.path.join(diretorio, arquivo_pdf)

        name_archive = arquivo_pdf
        
        # Abre o arquivo PDF em modo de leitura binária
        try:
            pdf_file = open(pdf_path, 'rb')
            print(f"Lendo: {arquivo_pdf}")
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Inicializa uma string vazia para armazenar o conteúdo do PDF
            pdf_text = ''

            # Loop através das páginas do PDF
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text() 
                if page_num == 2:
                    break

            # Fecha o arquivo PDF
            pdf_file.close()
        except:
            print(f"Arquivo corrompido ->  {arquivo_pdf} ")

        #print(pdf_text)

        # Extrair os dados desejados
        numero_processo_match = re.search(r"(\d+\.\d+/\d+-\d+|nº\s*\d+/\d+|[a-z][a-z]\s*\d+/\d+)", pdf_text , flags=re.MULTILINE|re.DOTALL|re.IGNORECASE )

        numero_processo = numero_processo_match.group(1) if numero_processo_match else "null"
        
        data_julgamento_match = re.search(r"Data do julgamento:\s*(\d{2}/\d{2}/\d{4})", pdf_text)
        data_julgamento = data_julgamento_match.group(1) if data_julgamento_match else "null"
        
        relatora_match = re.search(r"Relatora:\s*(.+)", pdf_text)
        relatora = relatora_match.group(1) if relatora_match else "null"
        
        acusado_match = re.search(r"ACUSADO*A*S*\s*:*\s*(.*)EMENTA", pdf_text,  flags=re.MULTILINE|re.DOTALL|re.IGNORECASE )
        acusado = acusado_match.group(1) if acusado_match else "null"
        
        ementa_match = re.search(r"EMENTAS*\s*:\s*(.*)DECIS.O", pdf_text,  flags=re.MULTILINE|re.DOTALL|re.IGNORECASE )
        ementa = ementa_match.group(1).strip() if ementa_match else "null"
        
        decisao_match = re.search(r"Decisão:(.*?)(Documento assinado eletronicamente|\Z)", pdf_text, re.DOTALL)
        decisao_completa = decisao_match.group(1).strip() if decisao_match else "null"
        

        

        # print(f"Numero_processo : {str(numero_processo)} ")
        # print(f"data_julgamento : {str(data_julgamento)} ")
        # print(f"relatora : {str(relatora)} ")
        #print(f"acusado : {str(acusado)}  ")
        nomes = re.split(r'\n', str(acusado))
        nomes = [nome.strip() for nome in nomes if nome.strip()]  # Remove linhas em branco
        # print(f"ementa : {str(ementa)}")
        # print(f"decisao_completa : {str(decisao_completa)}")

        if acusado != "null":
            if(len(nomes) <= 5 and nomes[0] != 'null'):
                # Adiciona os dados extraídos à lista de dados totais
                dados_totais.append([name_archive,numero_processo, data_julgamento, relatora, acusado, ementa, decisao_completa])

                if "null" in dados_totais[-1]:
                    with open('output.txt', 'a', encoding='utf-8', errors='ignore') as output_file:
                        output_file.write(str(arquivo_pdf) + '\n')
                        if str(numero_processo) == 'null':
                            output_file.write(f"Numero_processo : {str(numero_processo)} \n")
                        if str(data_julgamento) == 'null':
                            output_file.write(f"data_julgamento : {str(data_julgamento)} \n")
                        if str(relatora) == 'null':
                            output_file.write(f"relatora : {str(relatora)} \n")
                        if str(acusado) == 'null':
                            output_file.write(f"acusado : {str(acusado)} \n ")
                        if str(ementa) == 'null':
                            output_file.write(f"ementa : {str(ementa)} \n")
                        output_file.write('\n\n\n-------\n\n\n')


# Nomes das colunas
colunas = ["nome_arquivo","numero_processo", "Data do Julgamento", "Relatora", "Acusado", "Ementa", "Decisão"]

#Escreve os dados no arquivo CSV
with open('resultado.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(colunas)  # Escreve os nomes das colunas
    csv_writer.writerows(dados_totais)  # Escreve os dados

print("Dados salvos com sucesso no arquivo resultado.csv")
