import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

from tabelaHash import REMOVIDO, TabelaHashSondagemLinear


def montar_tabela(entradas):
    tabela = TabelaHashSondagemLinear(len(entradas))
    tabela.tabela = list(entradas)
    tabela.quantidade = sum(
        1 for entrada in entradas if entrada is not None and entrada is not REMOVIDO
    )
    return tabela


class TestHashMCDC(unittest.TestCase):
        
    def test_mcdc_listagens_100_por_cento(self):
        tabela = TabelaHashSondagemLinear(3)
        
        tabela.inserir("OK", 100) 
        tabela.inserir("DEL", 200) 
        tabela.remover("DEL")     

        resultado = tabela.chaves() #
        self.assertEqual(resultado, ["OK"]) #
    
    def test_mcdc_procurar_posicao_final(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.inserir(0, "v0")
        tabela.remover(0) 

        self.assertEqual(tabela._procurar_posicao(0, para_insercao=True), 0) #

        self.assertIsNone(tabela._procurar_posicao(1, para_insercao=False)) #

        tabela_limpa = TabelaHashSondagemLinear(2)
        tabela_limpa.inserir(0, "v0")
        
        self.assertEqual(tabela_limpa._procurar_posicao(1, para_insercao=True), 1)
        
    def test_mcdc_procurar_posicao_condicoes_de_insercao_e_slot_removido(self):
        tabela = TabelaHashSondagemLinear(3)

        tabela.tabela = [REMOVIDO, None, None]
        tabela._procurar_posicao(0, para_insercao=False) 

        tabela.tabela = [REMOVIDO, REMOVIDO, None]
        tabela._procurar_posicao(0, para_insercao=True)

        tabela_cheia = TabelaHashSondagemLinear(2)
        tabela_cheia.quantidade = 2 

        tabela_cheia.tabela = [(1, "A"), (2, "B")]
        tabela_cheia._procurar_posicao(99, para_insercao=False)
        
        tabela_cheia._procurar_posicao(99, para_insercao=True)

        tabela_cheia.tabela = [REMOVIDO, (2, "B")]
        tabela_cheia._procurar_posicao(99, para_insercao=True)


    def test_mcdc_inserir_avalia_slot_atual_como_vazio_ou_removido(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.tabela = [None, REMOVIDO, (2, "Ocupado")]

        tabela.inserir(0, "Novo A")

        tabela.inserir(1, "Novo B")

        tabela.inserir(2, "Atualiza Ocupado")


    def test_mcdc_listagens_filtram_slots_vazios_e_marcadores_de_remocao(self):
        tabela = TabelaHashSondagemLinear(3)
        
        tabela.tabela = [None, REMOVIDO, ("Chave", "Valor")]

        self.assertEqual(tabela.chaves(), ["Chave"])
        self.assertEqual(tabela.valores(), ["Valor"])
        self.assertEqual(tabela.itens(), [("Chave", "Valor")])

if __name__ == "__main__":
    unittest.main()
