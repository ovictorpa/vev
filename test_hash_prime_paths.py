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

class TestHashPrimePaths(unittest.TestCase):
    
    def setUp(self):
        self.tabela = TabelaHashSondagemLinear(capacidade=3)

    def test_busca_em_tabela_vazia(self):
        self.tabela.tabela = [None, None, None]
        self.assertIsNone(self.tabela._procurar_posicao(0, para_insercao=False))

    def test_busca_com_colisao_sucesso(self):
        self.tabela.tabela = [(0, "zero"), (3, "tres"), None]
        self.assertEqual(self.tabela._procurar_posicao(3, para_insercao=False), 1)

    def test_busca_passando_por_removido_ate_none(self):
        self.tabela.tabela = [REMOVIDO, None, (2, "dois")]
        self.assertIsNone(self.tabela._procurar_posicao(0, para_insercao=False))

    def test_busca_passando_por_removido_ate_sucesso(self):
        self.tabela.tabela = [REMOVIDO, (3, "tres"), None]
        self.assertEqual(self.tabela._procurar_posicao(3, para_insercao=False), 1)

    def test_busca_percorrer_tabela_toda_cheia_falha(self):
        self.tabela.tabela = [(0, "zero"), (1, "um"), (2, "dois")]

        self.tabela.quantidade = 3 
        self.assertIsNone(self.tabela._procurar_posicao(3, para_insercao=False))

    def test_insercao_sem_colisao(self):
        self.tabela.tabela = [None, None, None]
        self.assertEqual(self.tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_insercao_reutilizacao_posicao_removida(self):
        self.tabela.tabela = [REMOVIDO, None, None]
        self.assertEqual(self.tabela._procurar_posicao(0, para_insercao=True), 0)

    def test_insercao_encontra_chave_apos_removido(self):
        self.tabela.tabela = [REMOVIDO, (3, "tres"), None]
        self.assertEqual(self.tabela._procurar_posicao(3, para_insercao=True), 1)

    def test_insercao_percorrer_tabela_toda_com_multiplos_removidos(self):
        self.tabela.tabela = [REMOVIDO, REMOVIDO, (6, "seis")]
        self.tabela.quantidade = 3
        self.assertEqual(self.tabela._procurar_posicao(3, para_insercao=True), 0)

    def test_insercao_percorrer_tabela_toda_cheia_falha(self):
        self.tabela.tabela = [(0, "zero"), (1, "um"), (2, "dois")]
        self.tabela.quantidade = 3
        self.assertIsNone(self.tabela._procurar_posicao(3, para_insercao=True))
        
    def test_inserir_prime_path_tabela_cheia(self):
        self.tabela.tabela = [(1, "A"), (2, "B"), (3, "C")]
        self.tabela.quantidade = 3
        
        with self.assertRaises(OverflowError) as context:
            self.tabela.inserir(4, "D")
        
        self.assertEqual(str(context.exception), "Tabela hash cheia.")
        
        self.assertNotIn((4, "D"), self.tabela.tabela)

    def test_inserir_prime_path_atualiza_chave_existente(self):
        self.tabela.tabela = [None, (10, "ValorAntigo"), None]
        self.tabela.quantidade = 1

        self.tabela.inserir(10, "ValorNovo")
        
        self.assertEqual(self.tabela.quantidade, 1)
        self.assertEqual(self.tabela.tabela[1], (10, "ValorNovo"))

    def test_inserir_prime_path_slot_vazio_virgem(self):
        self.tabela.inserir(5, "Cinco")
        
        posicao = self.tabela.funcao_hash(5)
        self.assertEqual(self.tabela.tabela[posicao], (5, "Cinco"))
        self.assertEqual(self.tabela.quantidade, 1)

    def test_inserir_prime_path_slot_removido(self):
        posicao = self.tabela.funcao_hash(7)

        self.tabela.tabela = [None, None, None]
        self.tabela.tabela[posicao] = REMOVIDO
        self.tabela.quantidade = 0 
        
        self.tabela.inserir(7, "Sete")
        
        self.assertEqual(self.tabela.tabela[posicao], (7, "Sete"))
        self.assertEqual(self.tabela.quantidade, 1)

    def test_remover_prime_path_chave_nao_encontrada(self):
        self.tabela.tabela = [None, (2, "Dois"), None]
        self.tabela.quantidade = 1
        
        with self.assertRaises(KeyError) as context:
            self.tabela.remover(99)
            
        self.assertEqual(str(context.exception), "'Chave não encontrada: 99'")
        self.assertEqual(self.tabela.quantidade, 1)
        self.assertEqual(self.tabela.tabela[1], (2, "Dois"))

    def test_remover_prime_path_sucesso(self):
        self.tabela.tabela = [(0, "Zero"), (1, "Um"), None]
        self.tabela.quantidade = 2

        self.tabela.remover(0)
        
        self.assertEqual(self.tabela.tabela[0], REMOVIDO)
        self.assertEqual(self.tabela.quantidade, 1)
        self.assertEqual(self.tabela.tabela[1], (1, "Um"))
        
    def test_funcao_hash_todos_caminhos(self):
        th = TabelaHashSondagemLinear(10)

        self.assertEqual(th.funcao_hash(15), 5)

        self.assertEqual(th.funcao_hash(""), 0)
        
        self.assertEqual(th.funcao_hash("A"), 65 % 10)
        
        self.assertEqual(th.funcao_hash("AB"), (65 + 66) % 10)
        class Vazio:
            def __str__(self): return ""
        self.assertEqual(th.funcao_hash(Vazio()), 0)
        
        class ObjetoUmChar:
            def __str__(self): return "X"
        
        self.assertEqual(th.funcao_hash(ObjetoUmChar()), ord("X") % 10)
        
        chave_float = 1.5 
        soma_float = sum(ord(c) for c in str(chave_float)) % 10
        self.assertEqual(th.funcao_hash(chave_float), soma_float)


    def test_iteradores_transicoes_completas(self):
        t1 = TabelaHashSondagemLinear(1)
        
        t1.tabela = [None]
        t1.chaves(); t1.valores(); t1.itens(); str(t1)
        
        t1.tabela = [REMOVIDO]
        t1.chaves(); t1.valores(); t1.itens(); str(t1)
        
        t1.tabela = [("K", "V")]
        t1.chaves(); t1.valores(); t1.itens(); str(t1)

        t3 = TabelaHashSondagemLinear(3)

        t3.tabela = [("A", 1), REMOVIDO, None]
        t3.chaves(); t3.valores(); t3.itens(); str(t3)

        t3.tabela = [None, ("B", 2), REMOVIDO]
        t3.chaves(); t3.valores(); t3.itens(); str(t3)

        t3.tabela = [REMOVIDO, None, ("C", 3)]
        t3.chaves(); t3.valores(); t3.itens(); str(t3)

        t3.tabela = [None, None, None]
        t3.chaves()
        t3.tabela = [REMOVIDO, REMOVIDO, REMOVIDO]
        t3.chaves()
        t3.tabela = [("X", 1), ("Y", 2), ("Z", 3)]
        str(t3)

    def test_procurar_posicao_estado_critico_insercao(self):
        th = TabelaHashSondagemLinear(3)
        th.quantidade = 0

        th.tabela = [None, None, REMOVIDO]
        self.assertEqual(th._procurar_posicao(2, para_insercao=True), 2) 
        self.assertIsNone(th._procurar_posicao(2, para_insercao=False)) 

        th.tabela = [(2, "Val"), None, REMOVIDO]
        self.assertEqual(th._procurar_posicao(2, para_insercao=True), 0) 
        self.assertEqual(th._procurar_posicao(2, para_insercao=False), 0)

        th.tabela = [(0, "A"), REMOVIDO, (2, "C")]
        th.quantidade = 2
        self.assertEqual(th._procurar_posicao(10, para_insercao=True), 1)
        self.assertIsNone(th._procurar_posicao(10, para_insercao=False))

        th.tabela = [(0, "A"), (1, "B"), (2, "C")]
        th.quantidade = 3
        self.assertIsNone(th._procurar_posicao(10, para_insercao=True))
        self.assertIsNone(th._procurar_posicao(10, para_insercao=False))

    
    def test_inserir_caminhos_decisao(self):
        th = TabelaHashSondagemLinear(2)
        
        th.tabela = [None, None]; th.quantidade = 0
        th.inserir(0, "A")
        self.assertEqual(th.quantidade, 1)
        
        th.tabela = [(0, "A"), None]; th.quantidade = 1
        th.inserir(0, "Z") 
        self.assertEqual(th.quantidade, 1)
        
        th.tabela = [REMOVIDO, None]; th.quantidade = 0
        th.inserir(0, "B")
        self.assertEqual(th.quantidade, 1)
        
        th.tabela = [(0, "X"), (1, "Y")]; th.quantidade = 2
        with self.assertRaises(OverflowError):
            th.inserir(3, "C")

    def test_remover_caminhos_decisao(self):
        th = TabelaHashSondagemLinear(2)
        
        th.tabela = [(0, "A"), None]; th.quantidade = 1
        th.remover(0)
        self.assertEqual(th.quantidade, 0)
        self.assertEqual(th.tabela[0], REMOVIDO)

        th.tabela = [None, None]
        with self.assertRaises(KeyError):
            th.remover(99)

if __name__ == "__main__":
    unittest.main()
