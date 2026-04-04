import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

from tabelaHash import TabelaHashSondagemLinear

class TestHashPrimePaths(unittest.TestCase):

    def test_busca_em_tabela_vazia(self):
        tabela = TabelaHashSondagemLinear(5)
        self.assertFalse(tabela.contem("x"))

    def test_insercao_sem_colisao(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        self.assertEqual(tabela.buscar("ana"), 1)

    def test_insercao_com_colisao(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(1, "a")
        tabela.inserir(4, "b")  # colisão
        self.assertEqual(tabela.buscar(4), "b")

    def test_reutilizacao_posicao_removida(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(1, "a")
        tabela.remover(1)
        tabela.inserir(4, "b")
        self.assertTrue(tabela.contem(4))

    def test_busca_com_varias_sondagens(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(1, "a")
        tabela.inserir(4, "b")
        tabela.inserir(7, "c")
        self.assertEqual(tabela.buscar(7), "c")
            
    def test_percorrer_tabela_toda_cheia(self):
        self.th = TabelaHashSondagemLinear(capacidade=3)
        self.th.inserir(0, "V0")
        self.th.inserir(1, "V1")
        self.th.inserir(2, "V2")
        
        pos = self.th._procurar_posicao(10, para_insercao=False)
        self.assertIsNone(pos)

    def test_atualizacao_valor_existente(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        tabela.inserir("ana", 2)
        self.assertEqual(tabela.buscar("ana"), 2)
        
    def test_percorrer_tabela_toda_com_removido(self):
        
        self.th = TabelaHashSondagemLinear(capacidade=3)

        self.th.inserir(0, "V0")
        self.th.inserir(1, "V1")
        self.th.inserir(2, "V2")
        self.th.remover(0)
        pos = self.th._procurar_posicao(10, para_insercao=True)
        self.assertEqual(pos, 0)
        
if __name__ == "__main__":
    unittest.main()