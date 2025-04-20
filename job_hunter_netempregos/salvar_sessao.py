# salvar_sessao.py
from scraper import iniciar_driver, fazer_login

driver = iniciar_driver(manter_aberto=True)  # Abre e NÃO fecha!
fazer_login(driver)
