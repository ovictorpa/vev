import unittest
import sys
import os

sys.path.insert(0, os.getcwd())

from VEV.vev.tabelaHash import TabelaHashSondagemLinear

class TestHashMCDC(unittest.TestCase):

    def test_inserir_posicao_vazia(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        self.assertEqual(tabela.buscar("ana"), 1)

    def test_inserir_posicao_removida(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        tabela.remover("ana")
        tabela.inserir("bia", 2)
        self.assertEqual(tabela.buscar("bia"), 2)

    def test_atualizar_posicao_ocupada(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("ana", 1)
        tabela.inserir("ana", 5)
        self.assertEqual(tabela.buscar("ana"), 5)

    def test_chaves_sem_removidos(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("a", 1)
        self.assertEqual(tabela.chaves(), ["a"])

    def test_chaves_com_removidos(self):
        tabela = TabelaHashSondagemLinear(5)
        tabela.inserir("a", 1)
        tabela.remover("a")
        self.assertEqual(tabela.chaves(), [])

    def test_contem_false(self):
        tabela = TabelaHashSondagemLinear(5)
        self.assertFalse(tabela.contem("x"))

if __name__ == "__main__":
    unittest.main()