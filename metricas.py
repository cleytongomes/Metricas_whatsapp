from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


# Importa o arquivo das variaveis
import variaveis


'''
    Vai para a conversa selecionada
'''
def buscaConversa(grupo):

    inp_xpath_search = variaveis.link_busca
    input_box_search = driver.find_element(By.XPATH, inp_xpath_search)
    input_box_search.click()
    time.sleep(0.5)

    input_box_search.clear()
    time.sleep(0.5)

    input_box_search.send_keys(grupo)
    time.sleep(2)

    elemento = wait.until(ec.element_to_be_clickable((By.XPATH, "//span[@title='" + grupo + "']" )))
    elemento.click()
    time.sleep(2)


'''
    Vai para as Informações do grupo
'''
def vai_para_infos_grupo():

    # Seleciona o Contato / Grupo
    header_conversa = driver.find_element(By.XPATH, variaveis.link_infos_grupo)
    header_conversa.click()
    time.sleep(2)


'''
    Retorna a quantidade de membros do grupo selecionado
'''
def retorna_qtd_membros():
    qtd_participantes = driver.find_element(By.XPATH, variaveis.num_elementos_grupo)
    qtd, texto = (qtd_participantes.get_attribute('innerHTML')).split(" ")

    return qtd


'''
    Salva as informações em um arquivo
'''
def gera_csv(integrantes_grupo):
    file = open("integrantes_grupo.csv", "w+", encoding="utf-8")

    # Topo da tabela
    file.write("grupo;qtd\n")

    # Escreve as linhas dos grupos encontrados
    for linha in integrantes_grupo:
        file.write(linha + "\n")

    # Fecha o arquivo
    file.close()


'''
    Desconecta do whatsapp
'''
def sair_whatsapp():

    bt_menu = driver.find_element(By.XPATH, variaveis.link_bt_menu)
    bt_menu.click()
    time.sleep(2)

    bt_sair = driver.find_element(By.XPATH, variaveis.link_bt_sair)
    bt_sair.click()
    time.sleep(2)



# Abre o navegador
ser = Service("drivers/geckodriver.exe")
driver = webdriver.Firefox(service=ser)

# Define o tempo de espera
wait = WebDriverWait(driver, 10)

# Abre o whatsapp
driver.get("https://web.whatsapp.com")

# Espera o Whatsapp carregar
input("Quando o whatsapp estiver logado, pressione a tecla enter.")
print("Iniciando o processo . . . \n")

# Pega os nomes dos grupos a serem analisados
# Abre o arquivo com os grupos
file = open("grupos_monitorados.txt", encoding="utf-8")

# Pega os grupos
grupos = file.readlines()

# Fecha o arquivo
file.close()

# Integrantes por grupo
integrantes_grupo = []

# Verifica cada um dos grupos
for grupo in grupos:

    # Retira espaços das laterais
    grupo = grupo.strip()

    # Verifica se o nome do grupo não está em branco
    if len(grupo) == 0:
        continue

    try:
        buscaConversa(grupo)
        vai_para_infos_grupo()
        membros = retorna_qtd_membros()
        integrantes_grupo.append((grupo) + ";" + membros)
        print(f"{grupo} -> {membros} Integrante(s)")

    except:
        print(f"Erro: Não conseguimos achar o grupo {grupo}, verifique se o nome está correto")

# Grava os nomes no documento CSV
gera_csv(integrantes_grupo)

# Fecha o whatsapp
sair_whatsapp()

# Fecha o navegador
driver.quit()

# Fim do programa
input("\nFim de Execução")