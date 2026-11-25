from core.regras import Artigo, avaliar, calcular_janela_anos

def test_exemplo_nao_credencia():
    arts = [Artigo("A1", 0.80), Artigo("A2", 0.30), Artigo("A3", 0.20), Artigo("A4", 0.15)]
    r = avaliar(arts, 4)
    assert abs(r.pontuacao - 1.10) < 1e-9
    assert r.credenciado is False

def test_exemplo_credencia():
    arts = [Artigo("A1", 0.80), Artigo("A2", 0.30), Artigo("A3", 0.25)]
    r = avaliar(arts, 4)
    assert abs(r.pontuacao - 1.35) < 1e-9
    assert r.credenciado is True

def test_janelas_artigo_y():
    assert calcular_janela_anos() == 4
    assert calcular_janela_anos(parentalidade=True) == 6
    assert calcular_janela_anos(pcd=True) == 5