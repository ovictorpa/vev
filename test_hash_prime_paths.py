import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

from VEV.vev.tabelaHash import TabelaHashSondagemLinear

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

    def test_tabela_cheia(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir(1, "a")
        tabela.inserir(2, "b")
        tabela.inserir(3, "c")
        with self.assertRaises(OverflowError):
            tabela.inserir(4, "d")

    def test_atualizacao_valor_existente(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        tabela.inserir("ana", 2)
        self.assertEqual(tabela.buscar("ana"), 2)

if __name__ == "__main__":
    unittest.main()