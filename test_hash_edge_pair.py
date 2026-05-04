import unittest
from tabelaHash import TabelaHashSondagemLinear, REMOVIDO

class TestTabelaHashSondagemLinear(unittest.TestCase):

    def test_init_valid_invalid(self):

        tabela = TabelaHashSondagemLinear(5)
        self.assertEqual(tabela.capacidade, 5)
        with self.assertRaises(ValueError):
            TabelaHashSondagemLinear(0)

    def test_funcao_hash_fluxos(self):

        tabela = TabelaHashSondagemLinear(10)

        self.assertEqual(tabela.funcao_hash(10), 0)

        self.assertEqual(tabela.funcao_hash("ABC"), (ord("A") + ord("B") + ord("C")) % 10)

        self.assertEqual(tabela.funcao_hash(""), 0)

        class ObjetoVazio:
            def __str__(self): return ""
        self.assertEqual(tabela.funcao_hash(ObjetoVazio()), 0)

    def test_procurar_posicao_edge_pairs(self):

        tabela = TabelaHashSondagemLinear(3)
        
        tabela.inserir(0, "val0") 
        tabela.inserir(3, "val3") 
        tabela.remover(0)        
        
        self.assertEqual(tabela._procurar_posicao(3), 1)

        self.assertIsNone(tabela._procurar_posicao(6, para_insercao=False))

        self.assertEqual(tabela._procurar_posicao(6, para_insercao=True), 0)

    def test_procurar_posicao_saida_loop_com_removida(self):

        tabela = TabelaHashSondagemLinear(2)
        
        tabela.inserir(0, "valor0") 
        tabela.inserir(1, "valor1") 
        
        tabela.remover(0) 

        tabela.quantidade = 2 
        
        posicao = tabela._procurar_posicao(2, para_insercao=True)
        
        self.assertEqual(posicao, 0)

    def test_metodos_listagem_cobertura_total(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.inserir("A", 10)
        tabela.inserir("B", 20)
        tabela.remover("B") 

        self.assertEqual(tabela.chaves(), ["A"])
        self.assertEqual(tabela.valores(), [10])
        self.assertEqual(tabela.itens(), [("A", 10)])

        tabela.tabela = []
        self.assertEqual(tabela.chaves(), [])
        self.assertEqual(tabela.valores(), [])
        self.assertEqual(tabela.itens(), [])


    def test_str_representacao_completa(self):

        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir("A", 1)
        tabela.remover("A")

        res = str(tabela)
        self.assertIn("REMOVIDO", res)
        self.assertIn("VAZIO", res)

        tabela_um = TabelaHashSondagemLinear(1)
        tabela_um.inserir("fim", "valor")
        self.assertEqual(str(tabela_um), "0: fim -> valor")


    def test_inserir_buscar_excecoes(self):
        tabela = TabelaHashSondagemLinear(1)
        tabela.inserir("key", "val")
        
        with self.assertRaises(OverflowError):
            tabela.inserir("outra", 2)
            
        with self.assertRaises(KeyError):
            tabela.buscar("nado")
            
        with self.assertRaises(KeyError):
            tabela.remover("nado")
            

    def test_hash_edge_pair_objeto_com_caracteres(self):
        tabela = TabelaHashSondagemLinear(10)

        chave = 1.5
        soma_esperada = sum(ord(c) for c in str(chave)) % 10
        self.assertEqual(tabela.funcao_hash(chave), soma_esperada)
        
        
    def test_inserir_edge_pair_em_removido(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir("A", 1)
        tabela.remover("A") 

        tabela.inserir("B", 2)
        self.assertEqual(tabela.buscar("B"), 2)
        
        
    def test_inserir_edge_pair_12_11_8(self):
        tabela = TabelaHashSondagemLinear(1)

        tabela.inserir("chave_teste", "valor1")

        tabela.remover("chave_teste")

        tabela.inserir("nova_chave", "valor2")
        
        self.assertEqual(tabela.buscar("nova_chave"), "valor2")
        self.assertEqual(len(tabela), 1)
        
        
    def test_inserir_edge_pair_atualizacao(self):
        tabela = TabelaHashSondagemLinear(3)
        tabela.inserir("chave", "original")

        tabela.inserir("chave", "atualizado")
        self.assertEqual(tabela.buscar("chave"), "atualizado")
        self.assertEqual(len(tabela), 1) 
        
        
    def test_edge_pair_chaves_falha_primeira_condicao(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.tabela = [None, (1, 'val')] 

        self.assertEqual(tabela.chaves(), [1])

        tabela_fim = TabelaHashSondagemLinear(1)
        tabela_fim.tabela = [None] 

        self.assertEqual(tabela_fim.chaves(), [])

    def test_edge_pair_chaves_sucesso_e_continuidade(self):
        tabela = TabelaHashSondagemLinear(2)
        tabela.tabela = [(0, 'a'), (1, 'b')]

        self.assertEqual(tabela.chaves(), [0, 1])

        tabela_fim = TabelaHashSondagemLinear(1)
        tabela_fim.tabela = [(0, 'a')]
        self.assertEqual(tabela_fim.chaves(), [0])

    def test_edge_pair_chaves_com_removidos(self):
        tabela = TabelaHashSondagemLinear(1)
        tabela.tabela = [REMOVIDO] 

        self.assertEqual(tabela.chaves(), [])

        tabela_seq = TabelaHashSondagemLinear(2)
        tabela_seq.tabela = [(0, 'a'), REMOVIDO] 
        self.assertEqual(tabela_seq.chaves(), [0])
        
    def test_valores_edge_pairs_finalizacao(self):
        tabela_n = TabelaHashSondagemLinear(1)
        self.assertEqual(tabela_n.valores(), [])

        tabela_r = TabelaHashSondagemLinear(1)
        tabela_r.inserir("A", 1)
        tabela_r.remover("A")
        self.assertEqual(tabela_r.valores(), [])

        tabela_v = TabelaHashSondagemLinear(1)
        tabela_v.inserir("B", 2)
        self.assertEqual(tabela_v.valores(), [2])

    def test_valores_edge_pairs_continuidade(self):
        tabela_cheia = TabelaHashSondagemLinear(2)
        tabela_cheia.inserir("D", 4)
        tabela_cheia.inserir("E", 5)
        self.assertEqual(tabela_cheia.valores(), [4, 5])
        
    
    def test_itens_edge_pairs_finalizacao(self):
        tabela_v = TabelaHashSondagemLinear(1)
        tabela_v.inserir("chave", "valor")

        self.assertEqual(tabela_v.itens(), [("chave", "valor")])

    def test_itens_edge_pairs_continuidade(self):
        tabela_f = TabelaHashSondagemLinear(2)
        tabela_f.tabela = [None, REMOVIDO] 

        self.assertEqual(tabela_f.itens(), [])
        
        
    def test_str_edge_pairs_finalizacao(self):
        tabela_r = TabelaHashSondagemLinear(1)
        tabela_r.tabela = [REMOVIDO]

        self.assertEqual(str(tabela_r), "0: REMOVIDO")

        tabela_v = TabelaHashSondagemLinear(1)
        tabela_v.tabela = [("B", 2)]
        self.assertEqual(str(tabela_v), "0: B -> 2")

    def test_str_edge_pairs_continuidade(self):
        tabela_mista = TabelaHashSondagemLinear(2)
        tabela_mista.tabela = [REMOVIDO, ("V", 1)] 
        esperado = "0: REMOVIDO\n1: V -> 1"
        self.assertEqual(str(tabela_mista), esperado)
    
if __name__ == '__main__':
    unittest.main()