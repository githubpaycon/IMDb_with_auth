from funcsforspo_l.fpython.functions_for_py import *
from funcsforspo_l.fselenium.functions_selenium import *
from src.base.base import *
from src.database.database import *

class LeFilmes(Bot):
    def __init__(self, headless, download_files) -> None:
        super().__init__(headless, download_files)
        rank_col = []
        nome_filme_col = []
        ano_col = []
        imdb_rating_col = []

    def recupera_os_filmes(self):
        def vai_para_o_site():
            faz_log_st(f'Indo para o site https://www.imdb.com/chart/top/?ref_=nv_mv_250')
            self.DRIVER.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')

        def recupera_todos_os_filmes():
            faz_log_st('Recuperando texto...')
            rank_ = espera_e_retorna_lista_de_elementos_text(self.WDW, (By.CSS_SELECTOR, 'td[class="titleColumn"]'))
            imdb = espera_e_retorna_lista_de_elementos_text(self.WDW, (By.CSS_SELECTOR, 'td[class="ratingColumn imdbRating"]'))
            ziper = zip(rank_, imdb)
            
            # limpa em caso de 2a execução

            for i, imdb in ziper:
                rank_value = i.split('. ')[0]
                nome_filme = i.split(' (')[0]
                ano_filme = i.split(' (')[1].replace('(', '').replace(')', '')
                faz_log_st(f'RANK: {rank_value}')
                faz_log_st(f'NOME FILME: {nome_filme}')
                faz_log_st(f'ANO FILME: {ano_filme}')
                faz_log_st(f'IMDB RANKING: {imdb}')
                faz_log_st(' ')
                
                rank_col.append(rank_value)
                nome_filme_col.append(nome_filme)
                ano_col.append(ano_filme)
                imdb_rating_col.append(imdb)
                
                
                
                # faz_log_st(i)
                
        
        vai_para_o_site()
        recupera_todos_os_filmes()
        self.DRIVER.quit()

def executar_bot():
    bot = LeFilmes(True, False)
    bot.recupera_os_filmes()


