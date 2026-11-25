import streamlit as st
from core.regras import Artigo, avaliar, calcular_janela_anos

# --- Login simples (mock para o MVP) ---
st.set_page_config(page_title="Credenciamento PPGE", page_icon="🎓")

# Simulação de login (depois podemos melhorar com streamlit-authenticator)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Acesso Restrito")
    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if user == "professor" and pwd == "admin123": # Senha simples para teste
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

st.title("🎓 Credenciamento Docente PPGE")
st.caption("Case ME315 — Artigo X + Artigo Y")

with st.form("form_avaliacao"):
    st.subheader("1) Período de Análise (Artigo Y)")
    parentalidade = st.checkbox("Licença parentalidade (+50%)")
    pcd = st.checkbox("Docente/cônjuge PcD (+50%)")
    meses_medica = st.number_input("Licença médica (meses)", min_value=0.0, step=1.0)

    st.subheader("2) Artigos indicados (até 4)")
    artigos = []
    for i in range(4):
        cols = st.columns([3, 2])
        titulo = cols[0].text_input(f"Periódico {i+1}", key=f"t{i}")
        perc = cols[1].number_input(f"Percentil SJR {i+1}", min_value=0.0, max_value=1.0, step=0.01, key=f"p{i}")
        artigos.append(Artigo(titulo or f"Artigo {i+1}", perc))

    enviado = st.form_submit_button("Avaliar Credenciamento")

if enviado:
    janela = calcular_janela_anos(parentalidade, pcd, meses_medica)
    r = avaliar(artigos, janela)
    
    st.divider()
    st.subheader("Resultado da Avaliação")
    if r.credenciado:
        st.success(f"✅ CREDENCIADO — Pontuação: {r.pontuacao:.2f} (Mínimo 1,25)")
    else:
        st.error(f"❌ NÃO CREDENCIADO — Pontuação: {r.pontuacao:.2f} (Mínimo 1,25)")
    
    st.info(r.detalhes)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Artigos que somaram:**")
        for a in r.artigos_validos:
            st.write(f"- {a.titulo} (Percentil: {a.percentil})")
    with col2:
        st.write("**Artigos descartados (< 0,25):**")
        for a in r.artigos_descartados:
            st.write(f"- {a.titulo} (Percentil: {a.percentil})")