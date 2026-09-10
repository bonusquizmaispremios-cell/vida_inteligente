import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="VIDA INTELIGENTE", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_vida():
    return {"perfis": {}}

_cache = get_cache_vida()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'notas_areas_vida', 'historico_planos', 'planos_salvos',
    'missoes_hoje', 'missoes_concluidas_hoje', 'diario_entradas',
    'habitos_ativos', 'conquistas_desbloqueadas', 'projetos_ativos',
    'grandes_metas', 'data_ultima_missao',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_plano(tipo: str, titulo: str, conteudo: str):
    st.session_state.historico_planos.append({
        'data':     datetime.now().strftime('%d/%m %H:%M'),
        'tipo':     tipo,
        'titulo':   titulo,
        'conteudo': conteudo,
    })
    verificar_conquistas()

# --- INICIALIZAÇÃO DE ESTADO ---
AREAS_VIDA = ["Saúde", "Finanças", "Família", "Trabalho", "Estudos", "Saúde Mental", "Hábitos", "Bem-estar"]
EMOJI_AREA = {"Saúde":"❤️","Finanças":"💰","Família":"👨‍👩‍👧","Trabalho":"💼","Estudos":"📚","Saúde Mental":"🧠","Hábitos":"🏃","Bem-estar":"😊"}

defaults = {
    'etapa':                "Login",
    'usuario':               "",
    'api_key':               "",
    'pagina':                "Home",
    'notas_areas_vida':      {a: 5 for a in AREAS_VIDA},
    'historico_planos':      [],
    'planos_salvos':         [],
    'missoes_hoje':          [],
    'missoes_concluidas_hoje': [],
    'diario_entradas':       [],
    'habitos_ativos':        [],
    'conquistas_desbloqueadas': [],
    'projetos_ativos':       [],
    'grandes_metas':         [],
    'data_ultima_missao':    "",

    'missoes_concluidas_hoje_temp': [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- CONQUISTAS ---
CONQUISTAS_DEFINIDAS = [
    {"id": "primeiro_plano",   "nome": "Primeiro Plano Criado",    "emoji": "🎯", "condicao": lambda s: len(s.historico_planos) >= 1},
    {"id": "primeira_semana",  "nome": "Primeira Semana Completa", "emoji": "📅", "condicao": lambda s: len(s.missoes_concluidas_hoje) >= 7},
    {"id": "primeiro_habito",  "nome": "Primeiro Hábito Criado",   "emoji": "🔥", "condicao": lambda s: len(s.habitos_ativos) >= 1},
    {"id": "primeiro_diario",  "nome": "Primeira Reflexão",        "emoji": "📖", "condicao": lambda s: len(s.diario_entradas) >= 1},
    {"id": "primeiro_projeto", "nome": "Primeiro Projeto Iniciado","emoji": "📋", "condicao": lambda s: len(s.projetos_ativos) >= 1},
    {"id": "primeira_meta",    "nome": "Primeira Grande Meta",     "emoji": "🏆", "condicao": lambda s: len(s.grandes_metas) >= 1},
    {"id": "dez_planos",       "nome": "10 Planos Realizados",     "emoji": "🎖️", "condicao": lambda s: len(s.historico_planos) >= 10},
    {"id": "vida_equilibrada", "nome": "Vida Equilibrada",         "emoji": "⚖️", "condicao": lambda s: all(v >= 6 for v in s.notas_areas_vida.values())},
]

def verificar_conquistas():
    novas = []
    for c in CONQUISTAS_DEFINIDAS:
        if c['id'] not in st.session_state.conquistas_desbloqueadas:
            if c['condicao'](st.session_state):
                st.session_state.conquistas_desbloqueadas.append(c['id'])
                novas.append(c)
    return novas

# --- ECOSSISTEMA — para onde encaminhar ---
ECOSSISTEMA_APPS = {
    "financeiro": {"nome": "Oráculo Financeiro", "emoji": "💰", "quando": "questões de orçamento, dívidas, investimentos"},
    "procrastinacao": {"nome": "Destrava", "emoji": "⚡", "quando": "quando uma tarefa está travada e você não consegue agir"},
    "mental": {"nome": "Mente Poderosa", "emoji": "🧠", "quando": "bloqueios emocionais, ansiedade, meditação, PNL"},
    "treino": {"nome": "Personal Trainer IA", "emoji": "💪", "quando": "rotina de exercícios e treino físico"},
    "vendas": {"nome": "Mestre de Vendas Físicas", "emoji": "📦", "quando": "objetivos envolvendo vender produtos ou abrir negócio"},
    "juridico": {"nome": "Consultor Jurídico", "emoji": "⚖️", "quando": "dúvidas sobre direitos e questões legais"},
    "seguranca": {"nome": "Guardião Pessoal", "emoji": "🛡️", "quando": "segurança pessoal, residencial ou em viagens"},
    "alimentacao": {"nome": "Chef Calórico", "emoji": "🍽️", "quando": "alimentação, dieta e cardápio"},
    "estudos": {"nome": "Tutor de Concursos", "emoji": "📚", "quando": "estudar para concursos ou provas específicas"},
    "carreira": {"nome": "Perfil Profissional", "emoji": "💼", "quando": "currículo, LinkedIn e posicionamento profissional"},
}

# --- MOTOR DE IA ---
def vida_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        notas_txt = ", ".join([f"{a}: {n}/10" for a, n in st.session_state.notas_areas_vida.items()])
        system = f"""Você é um Gerente Pessoal de Vida com IA — um misto de coach, planejador e consultor estratégico.
Usuário: {st.session_state.usuario}.
Notas atuais das áreas da vida: {notas_txt}.
{system_extra}

PRINCÍPIOS:
- Seja prático, direto e organizado — sempre estruture em etapas claras
- Considere o contexto real da pessoa, nunca dê conselhos genéricos
- Quando relevante, mencione no final que existe uma ferramenta complementar no ecossistema para aprofundar
  (mas só se for genuinamente útil, não force isso)
- Português do Brasil, tom de gerente pessoal experiente — confiável e organizado, não robótico"""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def detectar_app_recomendado(texto: str) -> dict | None:
    """Analisa o texto e sugere qual app do ecossistema pode ajudar."""
    texto_lower = texto.lower()
    palavras_chave = {
        "financeiro": ["dívida", "orçamento", "investir", "investimento", "gastos", "dinheiro", "economizar"],
        "procrastinacao": ["procrastin", "travad", "não consigo começar", "adiando", "trava"],
        "mental": ["ansiedade", "medo", "bloqueio emocional", "estresse", "meditar"],
        "treino": ["treino", "exercício", "academia", "musculação", "correr"],
        "vendas": ["vender", "negócio", "empreender", "produto físico"],
        "juridico": ["direito", "lei", "processo", "advogado", "contrato"],
        "seguranca": ["segurança", "risco", "perigo", "trajeto seguro"],
        "alimentacao": ["dieta", "cardápio", "alimentação", "comida", "caloria"],
        "estudos": ["concurso", "prova", "estudar para"],
        "carreira": ["currículo", "linkedin", "entrevista de emprego"],
    }
    for app_key, palavras in palavras_chave.items():
        if any(p in texto_lower for p in palavras):
            return ECOSSISTEMA_APPS[app_key]
    return None

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_planos)
    habitos = len(st.session_state.habitos_ativos)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F0F4FF;border:1px solid #6366F1;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} planos gerados · {habitos} hábitos ativos</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"vida_inteligente_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
            key="vidainte11"
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

def renderizar_encaminhamento(app_info: dict):
    st.markdown(f"""
    <div class="encaminhamento-box">
        💡 <strong>Dica do ecossistema:</strong> para se aprofundar nesse assunto, o app
        <strong>{app_info['emoji']} {app_info['nome']}</strong> é especializado em {app_info['quando']}.
        Se você tiver esse app disponível, vale a pena consultá-lo.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'conquistas_desbloqueadas' not in st.session_state: st.session_state['conquistas_desbloqueadas'] = []
if 'diario_entradas' not in st.session_state: st.session_state['diario_entradas'] = []
if 'grandes_metas' not in st.session_state: st.session_state['grandes_metas'] = []
if 'habitos_ativos' not in st.session_state: st.session_state['habitos_ativos'] = []
if 'historico_planos' not in st.session_state: st.session_state['historico_planos'] = []
if 'missoes_concluidas_hoje' not in st.session_state: st.session_state['missoes_concluidas_hoje'] = []
if 'missoes_concluidas_hoje_temp' not in st.session_state: st.session_state['missoes_concluidas_hoje_temp'] = []
if 'missoes_hoje' not in st.session_state: st.session_state['missoes_hoje'] = []
if 'planos_salvos' not in st.session_state: st.session_state['planos_salvos'] = []
if 'projetos_ativos' not in st.session_state: st.session_state['projetos_ativos'] = []
if 'data_ultima_missao' not in st.session_state: st.session_state['data_ultima_missao'] = None

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 VIDA INTELIGENTE")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 quizcompremios.com.br</div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS — navegação nativa
    _tab_Home, _tab_Objetivos, _tab_Planejamento, _tab_MissaoDia, _tab_Projetos, _tab_Tempo, _tab_Habitos, _tab_Diario, _tab_Metas, _tab_Crise, _tab_Revisao, _tab_Relatorio, _tab_Conquistas, _tab_Decisoes = st.tabs(['🏠 Painel da Vida', '🎯 Objetivos Inteligent', '📅 Planejamento Intelig', '🚀 Missão do Dia', '📋 Organizador de Proje', '⏰ Organizador do Tempo', '🔥 Hábitos', '📖 Diário Inteligente', '🏆 Grandes Metas', '🚨 Modo Crise', '🌙 Revisão Noturna', '📈 Relatório Semanal', '🎖️ Sistema de Conquista', '❤️ Central de Decisões'])

    with _tab_Home:
            col_u, col_r = st.columns([3, 1])
            with col_u:
                st.title(f"Olá, {st.session_state.usuario}! 🧠")
                st.markdown("<span class='badge'>Gerente Pessoal Ativo</span>", unsafe_allow_html=True)
            with col_r:
                if st.button("🚪 Sair", key="vidainte3"):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()

            if len(st.session_state.historico_planos) == 0:
                st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
                padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
                ⚠️ Seus dados não estão mais no servidor.
                </div>""", unsafe_allow_html=True)
                arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
                if arq_home is not None:
                    try:
                        dados_home = json.load(arq_home)
                        carregar_json_sessao(dados_home)
                        salvar_perfil_cache(st.session_state.usuario)
                        st.success("✅ Dados recuperados!")
                        st.rerun()
                    except Exception:
                        st.error("Arquivo inválido.")

            st.markdown("### 🏠 Painel da Vida")
            st.markdown("Avalie de 0 a 10 cada área. Isso alimenta todos os planos que a IA cria para você.")

            col_a, col_b = st.columns(2)
            for i, area in enumerate(AREAS_VIDA):
                col = col_a if i % 2 == 0 else col_b
                with col:
                    nota_atual = st.session_state.notas_areas_vida.get(area, 5)
                    cor = "#22C55E" if nota_atual >= 7 else ("#B45309" if nota_atual >= 4 else "#B91C1C")
                    st.markdown(f"""
                    <div class="area-vida-box">
                        <div class="area-vida-header">
                            <span>{EMOJI_AREA[area]} {area}</span>
                            <span class="area-vida-nota" style="color:{cor};">{nota_atual}/10</span>
                        </div>
                        <div class="barra-bg"><div class="barra-fill" style="width:{nota_atual*10}%;background:{cor};"></div></div>
                    </div>
                    """, unsafe_allow_html=True)
                    nova_nota = st.slider(f"Ajustar {area}", 0, 10, nota_atual, key=f"slider_{area}", label_visibility="collapsed")
                    st.session_state.notas_areas_vida[area] = nova_nota

            media_geral = round(sum(st.session_state.notas_areas_vida.values()) / len(AREAS_VIDA), 1)
            area_mais_fraca = min(st.session_state.notas_areas_vida, key=st.session_state.notas_areas_vida.get)

            cor_media = "#22C55E" if media_geral >= 7 else ("#B45309" if media_geral >= 4 else "#B91C1C")
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="font-size:0.85em;color:#555;">SUA MÉDIA GERAL DE VIDA</div>
                <div style="font-size:2.2em;font-weight:700;color:{cor_media};font-family:'Playfair Display',serif;">{media_geral}/10</div>
                <div style="font-size:0.9em;color:#555;margin-top:4px;">🎯 Comece por: <strong>{EMOJI_AREA[area_mais_fraca]} {area_mais_fraca}</strong> — é sua área mais frágil agora</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🎯 CRIAR PLANO PARA MELHORAR ESSA ÁREA", key="btn_plano_area_fraca", use_container_width=True):
                st.session_state.pagina = "Objetivos"
                st.session_state['area_foco_objetivo'] = area_mais_fraca
                st.rerun()


            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_planos)}</div><div>Planos criados</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.habitos_ativos)}</div><div>Hábitos ativos</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.projetos_ativos)}</div><div>Projetos ativos</div></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.conquistas_desbloqueadas)}</div><div>Conquistas</div></div>", unsafe_allow_html=True)

            st.markdown("<div class='card'>💡 <em>'Você não precisa ser perfeito em todas as áreas. Precisa saber qual delas merece sua atenção agora.'</em></div>", unsafe_allow_html=True)

            st.markdown("### 🗺️ O que cada painel faz")
            guia = {
                "🎯 Objetivos":      "Transforme um objetivo grande em metas anuais, mensais, semanais e missão diária",
                "📅 Planejamento":   "Organiza seu dia automaticamente, prioriza tarefas e evita sobrecarga",
                "🚀 Missão do Dia":  "Gera sua missão personalizada para hoje, todos os dias",
                "📋 Projetos":       "Divide qualquer projeto grande (abrir empresa, casar, faculdade) em etapas pequenas",
                "⏰ Tempo":          "Analisa onde você perde tempo e o que pode eliminar ou delegar",
                "🔥 Hábitos":        "Cria e acompanha hábitos novos com lembretes e progresso",
                "📖 Diário":         "Reflexão guiada no fim do dia — o que deu certo, o que melhorar",
                "🏆 Grandes Metas":  "Acompanha metas de longo prazo — casa, carro, faculdade, aposentadoria",
                "🚨 Modo Crise":     "Quando a vida sai do controle, reorganiza toda a rotina com você",
                "🌙 Revisão Noturna":"Antes de dormir, revisa o que foi cumprido e ajusta amanhã",
                "📈 Relatório":      "Todo domingo, mostra sua evolução da semana",
                "🎖️ Conquistas":     "Acompanhe as marcas que você já desbloqueou",
                "❤️ Decisões":       "Tire dúvidas importantes — mudar de emprego, comprar algo, fazer um curso",
            }
            for aba, desc in guia.items():
                st.markdown(f"**{aba}** — {desc}")

            if st.session_state.historico_planos:
                st.markdown("### 🕐 Últimos Planos")
                for item in reversed(st.session_state.historico_planos[-4:]):
                    st.markdown(
                        f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> "
                        f"<small style='color:#888'>{item['data']}</small><br>"
                        f"<small>{item.get('titulo', '')[:80]}</small></div>", unsafe_allow_html=True)

        # ========================
        # OBJETIVOS INTELIGENTES
        # ========================

    with _tab_Objetivos:
            st.header("🎯 Objetivos Inteligentes")
            st.markdown("Diga o que você quer alcançar. A IA transforma em um plano com etapas anuais, mensais, semanais e diárias.")

            col1, col2 = st.columns(2)
            with col1:
                objetivo = st.text_area("💭 O que você quer alcançar?", height=100,
                    value=f"Quero melhorar minha área de {st.session_state.get('area_foco_objetivo','')}" if st.session_state.get('area_foco_objetivo') else "",
                    placeholder="ex: Quero comprar uma casa, Quero emagrecer 15kg, Quero abrir meu negócio...", key="vidainte10")
                prazo = st.selectbox("📅 Prazo desejado:", ["3 meses", "6 meses", "1 ano", "2 anos", "5 anos"], key="vidainte4")
            with col2:
                contexto_obj = st.text_area("📋 Contexto atual:", height=100,
                    placeholder="ex: Tenho R$2.000/mês de renda livre, trabalho CLT, moro de aluguel...", key="vidainte9")
                tempo_disp = st.selectbox("⏰ Tempo disponível por dia para isso:", ["15-30 min", "30min-1h", "1-2h", "2h+"], key="vidainte5")

            if st.button("🎯 CRIAR MEU PLANO COMPLETO", key="vidainte6"):
                if objetivo.strip():
                    with st.spinner("Transformando seu objetivo em um plano..."):
                        prompt = (
                            f"Transforme este objetivo em um plano estruturado completo.\n"
                            f"Objetivo: {objetivo}. Prazo: {prazo}. Contexto: {contexto_obj or 'não informado'}.\n"
                            f"Tempo disponível por dia: {tempo_disp}.\n\n"
                            f"FORMATO:\n\n"
                            f"🎯 PLANO: {objetivo.upper()}\n"
                            f"Prazo: {prazo}\n\n"
                            f"📅 OBJETIVO ANUAL:\n[o que precisa estar pronto em 12 meses, ou no prazo total se menor]\n\n"
                            f"📆 OBJETIVOS MENSAIS:\n[divida em marcos mensais — quantos meses fizerem sentido no prazo]\n\n"
                            f"📋 OBJETIVOS SEMANAIS (primeiras 4 semanas):\n[ações semanais concretas]\n\n"
                            f"☀️ MISSÃO DIÁRIA (o que fazer hoje):\n[3-5 ações pequenas e imediatas, considerando {tempo_disp} disponível]\n\n"
                            f"⚠️ MAIOR RISCO DE FALHAR NESSE PLANO:\n[seja honesto sobre o que pode travar essa pessoa]\n\n"
                            f"✅ COMO MEDIR PROGRESSO:\n[indicador simples para acompanhar]"
                        )
                        res = vida_ia(prompt)
                        salvar_plano("Objetivo", objetivo, res)
                        st.session_state['objetivo_temp'] = res
                        app_sugerido = detectar_app_recomendado(objetivo)
                        if app_sugerido:
                            st.session_state['app_sugerido_objetivo'] = app_sugerido
                else:
                    st.warning("Descreva seu objetivo.")

            if st.session_state.get('objetivo_temp'):
                st.markdown(f"<div class='card'>{st.session_state['objetivo_temp']}</div>", unsafe_allow_html=True)
                if st.session_state.get('app_sugerido_objetivo'):
                    renderizar_encaminhamento(st.session_state['app_sugerido_objetivo'])

                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar plano (.txt)", data=st.session_state['objetivo_temp'],
                        file_name="objetivo.txt", mime="text/plain", use_container_width=True, key="vidainte8")
                with col_sv:
                    if st.button("❤️ Salvar plano", use_container_width=True, key="vidainte7"):
                        st.session_state.planos_salvos.append({
                            'tipo': 'Objetivo', 'titulo': objetivo if 'objetivo' in dir() else '',
                            'conteudo': st.session_state['objetivo_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        # ========================
        # PLANEJAMENTO INTELIGENTE
        # ========================

    with _tab_Planejamento:
            st.header("📅 Planejamento Inteligente")
            st.markdown("Organize seu dia — a IA prioriza e evita sobrecarga.")

            tarefas_dia = st.text_area("📝 Liste suas tarefas de hoje (uma por linha):", height=150,
                placeholder="Responder e-mails do trabalho\nLevar filho ao médico\nEstudar inglês 30min\nPagar contas\nTreinar...", key="vidainte7_d2")
            col1, col2 = st.columns(2)
            with col1:
                horas_disp_plan = st.selectbox("⏰ Horas disponíveis hoje:", ["2 horas","4 horas","6 horas","8 horas","10+ horas"], key="vidainte8_d2")
            with col2:
                energia_hoje = st.select_slider("🔋 Sua energia hoje:", options=["Muito baixa","Baixa","Normal","Alta","Muito alta"], value="Normal", key="vidainte1")

            if st.button("📅 ORGANIZAR MEU DIA", key="vidainte9_d2"):
                if tarefas_dia.strip():
                    with st.spinner("Organizando seu dia..."):
                        prompt = (
                            f"Organize este dia de forma inteligente.\n"
                            f"Tarefas: {tarefas_dia}\n"
                            f"Horas disponíveis: {horas_disp_plan}. Energia hoje: {energia_hoje}.\n\n"
                            f"FORMATO:\n\n"
                            f"📅 SEU DIA ORGANIZADO\n\n"
                            f"🔴 PRIORIDADE MÁXIMA (faça primeiro):\n[tarefas com justificativa]\n\n"
                            f"🟡 IMPORTANTE (faça hoje, mas não primeiro):\n[tarefas]\n\n"
                            f"🟢 PODE ESPERAR (se sobrar tempo):\n[tarefas]\n\n"
                            f"⏰ CRONOGRAMA SUGERIDO:\n[horário aproximado para cada bloco, considerando {horas_disp_plan} e energia {energia_hoje}]\n\n"
                            f"⚠️ SINAL DE SOBRECARGA:\n[se a lista for grande demais para o tempo disponível, avise isso claramente e sugira o que cortar]"
                        )
                        res = vida_ia(prompt)
                        salvar_plano("Planejamento", "Organização do dia", res)
                        st.session_state['plan_temp'] = res
                else:
                    st.warning("Liste suas tarefas.")

            if st.session_state.get('plan_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['plan_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['plan_temp'], file_name="planejamento_dia.txt", mime="text/plain", key="vidainte10_d2")

        # ========================
        # MISSÃO DO DIA
        # ========================

    with _tab_MissaoDia:
            st.header("🚀 Missão do Dia")
            hoje = datetime.now().strftime('%d/%m/%Y')

            if st.session_state.data_ultima_missao != hoje or not st.session_state.missoes_hoje:
                st.markdown("Gere sua missão personalizada para hoje.")
                foco_missao = st.text_input("🎯 Algo específico em foco hoje? (opcional):", placeholder="ex: tenho uma reunião importante, preciso estudar para a prova...", key="vidainte11_d2")

                if st.button("🚀 GERAR MINHA MISSÃO DE HOJE", key="vidainte12"):
                    with st.spinner("Montando sua missão..."):
                        notas_txt = ", ".join([f"{a} ({n}/10)" for a, n in st.session_state.notas_areas_vida.items() if n < 6])
                        prompt = (
                            f"Gere a missão do dia para {st.session_state.usuario}.\n"
                            f"Áreas que precisam de atenção (nota baixa): {notas_txt or 'nenhuma área crítica'}.\n"
                            f"Foco específico de hoje: {foco_missao or 'nenhum específico'}.\n"
                            f"Hábitos ativos: {', '.join(st.session_state.habitos_ativos) if st.session_state.habitos_ativos else 'nenhum cadastrado'}.\n\n"
                            f"Gere de 4 a 6 itens de missão para HOJE — pequenos, concretos e realizáveis.\n"
                            f"Misture: 1 item da área mais fraca, 1 hábito ativo (se houver), 1 item do foco específico (se houver), e itens gerais de produtividade/bem-estar.\n\n"
                            f"FORMATO — responda APENAS com a lista, uma ação por linha, sem numeração, começando com verbo no infinitivo:\n"
                            f"Exemplo de formato esperado:\nFinalizar o orçamento mensal\nCaminhar 30 minutos\nEstudar inglês por 20 minutos\nLigar para o cliente pendente"
                        )
                        res = vida_ia(prompt)
                        itens = [linha.strip() for linha in res.split('\n') if linha.strip() and len(linha.strip()) > 5][:6]
                        st.session_state.missoes_hoje = itens
                        st.session_state.missoes_concluidas_hoje_temp = []
                        st.session_state.data_ultima_missao = hoje
                        salvar_plano("Missão Diária", hoje, res)
                        st.rerun()
            else:
                st.markdown(f"#### 📅 Missão de hoje — {hoje}")
                concluidas_hoje = st.session_state.get('missoes_concluidas_hoje_temp', [])

                for i, item in enumerate(st.session_state.missoes_hoje):
                    feito = i in concluidas_hoje
                    col_check, col_texto = st.columns([1, 9])
                    with col_check:
                        marcado = st.checkbox("", value=feito, key=f"missao_check_{i}_{hoje}")
                    with col_texto:
                        estilo = "text-decoration:line-through;opacity:0.5;" if marcado else ""
                        st.markdown(f"<div class='missao-item' style='{estilo}'>{'✅' if marcado else '⬜'} {item}</div>", unsafe_allow_html=True)

                    if marcado and i not in concluidas_hoje:
                        concluidas_hoje.append(i)
                    elif not marcado and i in concluidas_hoje:
                        concluidas_hoje.remove(i)

                st.session_state.missoes_concluidas_hoje_temp = concluidas_hoje
                pct = round(len(concluidas_hoje) / len(st.session_state.missoes_hoje) * 100) if st.session_state.missoes_hoje else 0

                st.markdown(f"""
                <div class="missao-dia-box">
                    <div style="text-align:center;font-size:1.3em;font-weight:700;">{pct}% concluído hoje</div>
                    <div class="barra-bg"><div class="barra-fill" style="width:{pct}%;background:#6366F1;"></div></div>
                </div>
                """, unsafe_allow_html=True)

                if pct == 100 and hoje not in st.session_state.missoes_concluidas_hoje:
                    st.session_state.missoes_concluidas_hoje.append(hoje)
                    st.success("🎉 Missão do dia 100% concluída! Isso conta para suas conquistas semanais.")
                    for nova in verificar_conquistas():
                        st.markdown(f"<div class='toast-conquista'>🎉 <strong>Nova conquista!</strong><br>{nova['emoji']} {nova['nome']}</div>", unsafe_allow_html=True)

                if st.button("🔄 Gerar nova missão (substitui a de hoje)", key="vidainte13"):
                    st.session_state.missoes_hoje = []
                    st.rerun()

        # ========================
        # ORGANIZADOR DE PROJETOS
        # ========================

    with _tab_Projetos:
            st.header("📋 Organizador de Projetos")
            st.markdown("Qualquer projeto grande — divida em etapas pequenas e gerenciáveis.")

            col1, col2 = st.columns(2)
            with col1:
                nome_projeto = st.text_input("📋 Nome do projeto:", placeholder="ex: Abrir minha empresa, Reformar a casa, Casar...", key="vidainte14")
                tipo_projeto = st.selectbox("📂 Tipo:", ["Abrir empresa","Reformar casa","Casamento","Viagem","Construção","Faculdade","Concurso","Empreender","Mudança de cidade","Outro"], key="vidainte15")
            with col2:
                prazo_projeto = st.text_input("📅 Prazo desejado:", placeholder="ex: 6 meses, até dezembro...", key="prazo_projeto_input")
                orcamento_projeto = st.text_input("💰 Orçamento disponível (opcional):", placeholder="ex: R$10.000, ainda não defini...", key="vidainte16")

            detalhes_projeto = st.text_area("📝 Detalhes do projeto:", height=100,
                placeholder="ex: Quero abrir uma loja de roupas femininas no bairro onde moro...", key="vidainte6_d2")

            if st.button("📋 DIVIDIR PROJETO EM ETAPAS", key="vidainte17"):
                if nome_projeto.strip():
                    with st.spinner("Organizando seu projeto..."):
                        prompt = (
                            f"Divida este projeto em etapas pequenas e gerenciáveis.\n"
                            f"Projeto: {nome_projeto}. Tipo: {tipo_projeto}. Prazo: {prazo_projeto or 'não definido'}.\n"
                            f"Orçamento: {orcamento_projeto or 'não definido'}. Detalhes: {detalhes_projeto or 'não informado'}.\n\n"
                            f"FORMATO:\n\n"
                            f"📋 PROJETO: {nome_projeto.upper()}\n\n"
                            f"🗺️ FASES DO PROJETO:\n\n"
                            f"FASE 1 — [nome da fase]:\n[etapas dessa fase, cada uma com prazo estimado]\n\n"
                            f"FASE 2 — [nome da fase]:\n[etapas]\n\n"
                            f"FASE 3 — [nome da fase]:\n[etapas]\n\n"
                            f"[continue com quantas fases fizerem sentido]\n\n"
                            f"💰 ESTIMATIVA DE CUSTOS POR FASE:\n[se houver orçamento envolvido]\n\n"
                            f"⚠️ MAIORES RISCOS DESSE TIPO DE PROJETO:\n[riscos comuns e como mitigar]\n\n"
                            f"✅ PRIMEIRA AÇÃO CONCRETA (comece hoje):\n[1 ação imediata]"
                        )
                        res = vida_ia(prompt)
                        salvar_plano("Projeto", nome_projeto, res)
                        if nome_projeto not in st.session_state.projetos_ativos:
                            st.session_state.projetos_ativos.append(nome_projeto)
                        st.session_state['projeto_temp'] = res
                        for nova in verificar_conquistas():
                            st.session_state.setdefault('toasts_pendentes', []).append(nova)
                else:
                    st.warning("Informe o nome do projeto.")

            if st.session_state.get('projeto_temp'):
                st.markdown(f"<div class='card-orange'>{st.session_state['projeto_temp']}</div>", unsafe_allow_html=True)
                for toast in st.session_state.pop('toasts_pendentes', []):
                    st.markdown(f"<div class='toast-conquista'>🎉 <strong>Nova conquista!</strong><br>{toast['emoji']} {toast['nome']}</div>", unsafe_allow_html=True)

                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['projeto_temp'],
                        file_name=f"projeto_{nome_projeto.replace(' ','_') if 'nome_projeto' in dir() else ''}.txt",
                        mime="text/plain", use_container_width=True, key="vidainte5_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_proj", use_container_width=True):
                        st.session_state.planos_salvos.append({
                            'tipo': 'Projeto', 'titulo': nome_projeto if 'nome_projeto' in dir() else '',
                            'conteudo': st.session_state['projeto_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

            if st.session_state.projetos_ativos:
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 📂 Seus projetos ativos")
                for p in st.session_state.projetos_ativos:
                    st.markdown(f"<span class='badge'>📋 {p}</span>", unsafe_allow_html=True)

        # ========================
        # ORGANIZADOR DO TEMPO
        # ========================

    with _tab_Tempo:
            st.header("⏰ Organizador do Tempo")
            st.markdown("Analise onde seu tempo está indo e o que pode mudar.")

            rotina_atual = st.text_area("📝 Descreva sua rotina típica de um dia:", height=150,
                placeholder="ex: Acordo 7h, trabalho das 8h às 18h, chego em casa e fico no celular até dormir às 23h...", key="vidainte4_d2")

            if st.button("⏰ ANALISAR MEU TEMPO", key="vidainte18"):
                if rotina_atual.strip():
                    with st.spinner("Analisando sua rotina..."):
                        prompt = (
                            f"Analise esta rotina e identifique onde o tempo está sendo desperdiçado.\n"
                            f"Rotina: {rotina_atual}\n\n"
                            f"FORMATO:\n\n"
                            f"⏰ ANÁLISE DO SEU TEMPO\n\n"
                            f"📊 MAPA DO SEU DIA:\n[resumo das horas em cada tipo de atividade]\n\n"
                            f"🕳️ ONDE VOCÊ ESTÁ PERDENDO TEMPO:\n[identifique especificamente, com base no que foi descrito]\n\n"
                            f"⏱️ TEMPO LIVRE REAL DISPONÍVEL:\n[estimativa de quanto tempo de qualidade sobra por dia]\n\n"
                            f"🗑️ O QUE PODE SER ELIMINADO:\n[atividades de baixo valor identificadas]\n\n"
                            f"🤝 O QUE PODE SER DELEGADO:\n[se aplicável]\n\n"
                            f"✅ COMO RECUPERAR PELO MENOS 1 HORA POR DIA:\n[sugestão concreta e realista]"
                        )
                        res = vida_ia(prompt)
                        salvar_plano("Tempo", "Análise de rotina", res)
                        st.session_state['tempo_temp'] = res
                else:
                    st.warning("Descreva sua rotina.")

            if st.session_state.get('tempo_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['tempo_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['tempo_temp'], file_name="analise_tempo.txt", mime="text/plain", key="vidainte19")

        # ========================
        # HÁBITOS
        # ========================

    with _tab_Habitos:
            st.header("🔥 Hábitos")
            st.markdown("Crie e acompanhe hábitos novos.")

            col1, col2 = st.columns(2)
            with col1:
                novo_habito = st.text_input("➕ Novo hábito:", placeholder="ex: Beber 2L de água, Ler 10 páginas, Meditar 5min...", key="vidainte20")
                if st.button("➕ Adicionar hábito", key="vidainte21"):
                    if novo_habito.strip() and novo_habito not in st.session_state.habitos_ativos:
                        st.session_state.habitos_ativos.append(novo_habito)
                        verificar_conquistas()
                        st.success(f"✅ Hábito '{novo_habito}' adicionado!")
                        st.rerun()
            with col2:
                if st.session_state.habitos_ativos:
                    remover = st.selectbox("➖ Remover hábito:", ["Nenhum"] + st.session_state.habitos_ativos, key="vidainte22")
                    if st.button("➖ Remover", key="vidainte23") and remover != "Nenhum":
                        st.session_state.habitos_ativos.remove(remover)
                        st.rerun()

            if st.session_state.habitos_ativos:
                st.markdown("### 📋 Seus hábitos ativos")
                for h in st.session_state.habitos_ativos:
                    st.markdown(f"<span class='badge-verde'>🔥 {h}</span>", unsafe_allow_html=True)

                if st.button("🧠 PEDIR ESTRATÉGIA PARA CONSOLIDAR MEUS HÁBITOS", key="vidainte24"):
                    with st.spinner("Criando estratégia..."):
                        prompt = (
                            f"Crie uma estratégia para consolidar estes hábitos: {', '.join(st.session_state.habitos_ativos)}.\n\n"
                            f"FORMATO:\n\n"
                            f"🔥 ESTRATÉGIA DE HÁBITOS\n\n"
                            f"[Para cada hábito, sugira: melhor horário, gatilho para lembrar, e como começar pequeno]\n\n"
                            f"📅 COMO ENCAIXAR TODOS NA ROTINA SEM SOBRECARREGAR:\n[ordem sugerida e timing]\n\n"
                            f"💡 DICA DE CONSISTÊNCIA:\n[1 técnica prática para não desistir nas primeiras semanas]"
                        )
                        res = vida_ia(prompt)
                        salvar_plano("Hábitos", "Estratégia de hábitos", res)
                        st.session_state['habito_estrategia_temp'] = res

                if st.session_state.get('habito_estrategia_temp'):
                    st.markdown(f"<div class='card-green'>{st.session_state['habito_estrategia_temp']}</div>", unsafe_allow_html=True)
            else:
                st.info("Nenhum hábito cadastrado ainda. Adicione o primeiro acima!")

        # ========================
        # DIÁRIO INTELIGENTE
        # ========================

    with _tab_Diario:
            st.header("📖 Diário Inteligente")
            st.markdown("Reflexão guiada de fim de dia.")

            col1, col2, col3 = st.columns(3)
            with col1:
                deu_certo = st.text_area("✅ O que deu certo hoje?", height=100, key="vidainte25")
            with col2:
                deu_errado = st.text_area("❌ O que deu errado hoje?", height=100, key="vidainte26")
            with col3:
                melhorar = st.text_area("🔧 Como melhorar amanhã?", height=100, key="vidainte27")

            if st.button("📖 SALVAR REFLEXÃO DO DIA", key="vidainte28"):
                if deu_certo.strip() or deu_errado.strip() or melhorar.strip():
                    entrada = {
                        'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                        'deu_certo': deu_certo, 'deu_errado': deu_errado, 'melhorar': melhorar,
                    }
                    st.session_state.diario_entradas.append(entrada)
                    verificar_conquistas()
                    st.success("📖 Reflexão salva no seu diário!")
                    st.rerun()
                else:
                    st.warning("Preencha pelo menos um campo.")

            if st.session_state.diario_entradas:
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown(f"### 📚 Suas reflexões ({len(st.session_state.diario_entradas)})")
                for i, entrada in enumerate(reversed(st.session_state.diario_entradas[-10:])):
                    with st.expander(f"📖 {entrada['data']}"):
                        if entrada.get('deu_certo'): st.markdown(f"**✅ Deu certo:** {entrada.get('deu_certo', '')}")
                        if entrada.get('deu_errado'): st.markdown(f"**❌ Deu errado:** {entrada.get('deu_errado', '')}")
                        if entrada.get('melhorar'): st.markdown(f"**🔧 Melhorar:** {entrada.get('melhorar', '')}")

        # ========================
        # GRANDES METAS
        # ========================

    with _tab_Metas:
            st.header("🏆 Grandes Metas")
            st.markdown("Acompanhe metas de longo prazo.")

            col1, col2 = st.columns(2)
            with col1:
                nome_meta = st.text_input("🏆 Nome da meta:", placeholder="ex: Comprar casa própria, Trocar de carro...", key="vidainte29")
                valor_meta = st.number_input("💰 Valor total necessário (R$):", min_value=0.0, value=0.0, step=1000.0, key="vidainte30")
            with col2:
                valor_atual = st.number_input("💰 Quanto você já tem (R$):", min_value=0.0, value=0.0, step=500.0, key="vidainte31")
                prazo_meta = st.text_input("📅 Prazo desejado:", placeholder="ex: 2 anos, até 2028...", key="prazo_meta_input")

            if st.button("🏆 ADICIONAR/ATUALIZAR META", key="vidainte32"):
                if nome_meta.strip() and valor_meta > 0:
                    meta_existente = next((m for m in st.session_state.grandes_metas if m['nome'] == nome_meta), None)
                    if meta_existente:
                        meta_existente['valor_total'] = valor_meta
                        meta_existente['valor_atual'] = valor_atual
                        meta_existente['prazo'] = prazo_meta
                    else:
                        st.session_state.grandes_metas.append({
                            'nome': nome_meta, 'valor_total': valor_meta, 'valor_atual': valor_atual, 'prazo': prazo_meta,
                        })
                    verificar_conquistas()
                    st.success("🏆 Meta salva!")
                    st.rerun()
                else:
                    st.warning("Informe nome e valor total da meta.")

            if st.session_state.grandes_metas:
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 📊 Suas Metas")
                for meta in st.session_state.grandes_metas:
                    pct = min(100, round(meta.get('valor_atual', '') / meta['valor_total'] * 100)) if meta['valor_total'] > 0 else 0
                    falta = max(0, meta['valor_total'] - meta.get('valor_atual', ''))
                    st.markdown(f"""
                    <div class="card">
                        <strong>🏆 {meta['nome']}</strong> — {meta.get('prazo','sem prazo definido')}<br>
                        <div class="barra-bg" style="margin:8px 0;"><div class="barra-fill" style="width:{pct}%;background:#6366F1;"></div></div>
                        R$ {meta.get('valor_atual', ''):,.2f} de R$ {meta['valor_total']:,.2f} ({pct}%) — faltam R$ {falta:,.2f}
                    </div>
                    """, unsafe_allow_html=True)

        # ========================
        # MODO CRISE
        # ========================

    with _tab_Crise:
            st.header("🚨 Modo Crise")
            st.markdown("Quando a vida sai do controle, vamos reorganizar tudo com você.")

            situacao_crise = st.text_area("O que está acontecendo?", height=120,
                placeholder="ex: Perdi o emprego, Tive um problema de saúde, Aconteceu algo grave na família...", key="vidainte3_d2")

            if st.button("🚨 REORGANIZAR MINHA ROTINA", key="vidainte33"):
                if situacao_crise.strip():
                    with st.spinner("Reorganizando com cuidado..."):
                        notas_txt = ", ".join([f"{a}: {n}/10" for a, n in st.session_state.notas_areas_vida.items()])
                        prompt = (
                            f"SITUAÇÃO DE CRISE: {situacao_crise}\n"
                            f"Notas atuais das áreas de vida: {notas_txt}\n\n"
                            f"A pessoa está passando por um momento difícil. Ajude a reorganizar a vida dela com cuidado e realismo.\n\n"
                            f"FORMATO:\n\n"
                            f"🚨 ACOLHIMENTO:\n[1-2 frases reconhecendo a dificuldade, sem minimizar nem dramatizar]\n\n"
                            f"⚡ PRIORIDADES IMEDIATAS (próximos 7 dias):\n[o que precisa de atenção AGORA — geralmente segurança financeira/emocional básica]\n\n"
                            f"📅 ROTINA SIMPLIFICADA TEMPORÁRIA:\n[uma rotina mais leve e realista para esse momento, não a rotina ideal]\n\n"
                            f"🎯 O QUE PODE ESPERAR:\n[o que NÃO precisa ser resolvido agora, para reduzir a sobrecarga mental]\n\n"
                            f"🤝 REDE DE APOIO:\n[sugestões de quem/onde buscar apoio para esse tipo de situação]\n\n"
                            f"💪 PRÓXIMO PASSO QUANDO ESTABILIZAR:\n[1 frase sobre o que vem depois, com esperança realista]"
                        )
                        res = vida_ia(prompt, "MODO CRISE: seja acolhedor, realista e prático. A pessoa precisa de clareza e cuidado, não de pressão para produtividade.")
                        salvar_plano("Modo Crise", situacao_crise[:60], res)
                        st.session_state['crise_temp'] = res
                        app_sugerido = detectar_app_recomendado(situacao_crise)
                        if app_sugerido:
                            st.session_state['app_sugerido_crise'] = app_sugerido
                else:
                    st.warning("Descreva a situação.")

            if st.session_state.get('crise_temp'):
                st.markdown(f"<div class='card-red'>{st.session_state['crise_temp']}</div>", unsafe_allow_html=True)
                if st.session_state.get('app_sugerido_crise'):
                    renderizar_encaminhamento(st.session_state['app_sugerido_crise'])
                st.download_button("📋 Baixar (.txt)", data=st.session_state['crise_temp'], file_name="modo_crise.txt", mime="text/plain", key="vidainte34")

        # ========================
        # REVISÃO NOTURNA
        # ========================

    with _tab_Revisao:
            st.header("🌙 Revisão Noturna")
            st.markdown("Antes de dormir, vamos revisar o dia.")

            cumpriu = st.radio("Você cumpriu sua missão de hoje?", ["Sim, totalmente","Parcialmente","Não consegui"], horizontal=True, key="vidainte35")
            pendente = st.text_area("O que ficou pendente?", height=80, key="vidainte36")
            mudar_amanha = st.text_area("O que deve mudar amanhã?", height=80, key="vidainte37")

            if st.button("🌙 SALVAR REVISÃO E DORMIR EM PAZ", key="vidainte38"):
                entrada = {
                    'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'tipo': 'revisao_noturna',
                    'cumpriu': cumpriu, 'pendente': pendente, 'mudar_amanha': mudar_amanha,
                }
                st.session_state.diario_entradas.append(entrada)
                verificar_conquistas()
                st.success("🌙 Revisão salva. Bom descanso!")

        # ========================
        # RELATÓRIO SEMANAL
        # ========================

    with _tab_Relatorio:
            st.header("📈 Relatório Semanal")

            total_planos = len(st.session_state.historico_planos)
            total_missoes = len(st.session_state.missoes_concluidas_hoje)
            total_diario = len(st.session_state.diario_entradas)
            total_habitos = len(st.session_state.habitos_ativos)

            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_planos}</div><div>Planos criados</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_missoes}</div><div>Dias com missão completa</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_diario}</div><div>Reflexões no diário</div></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_habitos}</div><div>Hábitos em acompanhamento</div></div>", unsafe_allow_html=True)

            if st.button("📈 GERAR RELATÓRIO COMPLETO DA SEMANA", key="vidainte39"):
                with st.spinner("Montando seu relatório..."):
                    notas_txt = ", ".join([f"{a}: {n}/10" for a, n in st.session_state.notas_areas_vida.items()])
                    ultimas_reflexoes = "; ".join([e.get('deu_certo','') + " " + e.get('deu_errado','') for e in st.session_state.diario_entradas[-7:]])
                    prompt = (
                        f"Gere um relatório semanal de evolução pessoal.\n"
                        f"Planos criados na semana: {total_planos}. Dias com missão completa: {total_missoes}.\n"
                        f"Notas atuais das áreas: {notas_txt}.\n"
                        f"Reflexões recentes do diário: {ultimas_reflexoes or 'sem reflexões recentes'}.\n"
                        f"Hábitos ativos: {', '.join(st.session_state.habitos_ativos) if st.session_state.habitos_ativos else 'nenhum'}.\n\n"
                        f"FORMATO:\n\n"
                        f"📈 RELATÓRIO SEMANAL — {st.session_state.usuario.upper()}\n\n"
                        f"🏆 DESTAQUES DA SEMANA:\n[reconheça o que foi bem]\n\n"
                        f"⚠️ PADRÃO DE ATENÇÃO:\n[algo que se repetiu e merece ajuste]\n\n"
                        f"📊 EVOLUÇÃO POR ÁREA:\n[comente brevemente as áreas com base nas notas]\n\n"
                        f"🎯 FOCO PARA A PRÓXIMA SEMANA:\n[1-2 prioridades claras]\n\n"
                        f"💬 MENSAGEM DO SEU GERENTE PESSOAL:\n[1-2 frases motivadoras e realistas para a próxima semana]"
                    )
                    res = vida_ia(prompt)
                    salvar_plano("Relatório Semanal", datetime.now().strftime('%d/%m/%Y'), res)
                    st.session_state['relatorio_temp'] = res

            if st.session_state.get('relatorio_temp'):
                st.markdown(f"<div class='card-dark'>{st.session_state['relatorio_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar relatório (.txt)", data=st.session_state['relatorio_temp'], file_name="relatorio_semanal.txt", mime="text/plain", key="vidainte40")

        # ========================
        # SISTEMA DE CONQUISTAS
        # ========================

    with _tab_Conquistas:
            st.header("🎖️ Sistema de Conquistas")

            col_conq1, col_conq2 = st.columns(2)
            for i, c in enumerate(CONQUISTAS_DEFINIDAS):
                col = col_conq1 if i % 2 == 0 else col_conq2
                desbloqueada = c['id'] in st.session_state.conquistas_desbloqueadas
                classe = "conquista-card" if desbloqueada else "conquista-card conquista-bloqueada"
                with col:
                    st.markdown(f"""
                    <div class="{classe}">
                        <div class="conquista-emoji">{c['emoji'] if desbloqueada else '🔒'}</div>
                        <div>
                            <div style="font-weight:600;">{c['nome']}</div>
                            <div style="font-size:0.78em;color:#888;">{'Desbloqueada' if desbloqueada else 'Bloqueada'}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            pct_conquistas = round(len(st.session_state.conquistas_desbloqueadas) / len(CONQUISTAS_DEFINIDAS) * 100)
            st.markdown(f"<div class='card' style='text-align:center;'>🎖️ Você desbloqueou <strong>{len(st.session_state.conquistas_desbloqueadas)}/{len(CONQUISTAS_DEFINIDAS)}</strong> conquistas ({pct_conquistas}%)</div>", unsafe_allow_html=True)

        # ========================
        # CENTRAL DE DECISÕES
        # ========================

    with _tab_Decisoes:
            st.header("❤️ Central de Decisões")
            st.markdown("Tem uma dúvida importante? Vamos analisar vantagens, riscos e impacto nos seus objetivos.")

            duvida = st.text_area("💭 Qual decisão você está em dúvida?", height=100,
                placeholder="ex: Mudo de emprego? Compro esse carro? Faço esse curso?", key="vidainte2")
            contexto_decisao = st.text_area("📋 Contexto adicional:", height=80,
                placeholder="ex: O novo emprego paga 20% mais mas é mais distante de casa...", key="vidainte1_d2")

            if st.button("❤️ ANALISAR ESSA DECISÃO", key="vidainte41"):
                if duvida.strip():
                    with st.spinner("Analisando..."):
                        notas_txt = ", ".join([f"{a}: {n}/10" for a, n in st.session_state.notas_areas_vida.items()])
                        prompt = (
                            f"Ajude a analisar esta decisão.\n"
                            f"Decisão: {duvida}\nContexto: {contexto_decisao or 'não informado'}\n"
                            f"Notas atuais das áreas de vida da pessoa: {notas_txt}\n\n"
                            f"FORMATO:\n\n"
                            f"❤️ ANÁLISE DA DECISÃO\n\n"
                            f"✅ VANTAGENS:\n[liste com base no contexto]\n\n"
                            f"⚠️ RISCOS E DESVANTAGENS:\n[liste com honestidade]\n\n"
                            f"💰 IMPACTO FINANCEIRO/PRÁTICO:\n[se aplicável]\n\n"
                            f"🎯 IMPACTO NOS SEUS OBJETIVOS DE VIDA:\n[considerando as áreas que a pessoa já avaliou]\n\n"
                            f"🧠 CAMINHO SUGERIDO:\n[uma sugestão clara, mas deixando explícito que a decisão final é da pessoa]"
                        )
                        res = vida_ia(prompt)
                        salvar_plano("Decisão", duvida[:60], res)
                        st.session_state['decisao_temp'] = res
                        app_sugerido = detectar_app_recomendado(duvida + " " + contexto_decisao)
                        if app_sugerido:
                            st.session_state['app_sugerido_decisao'] = app_sugerido
                else:
                    st.warning("Descreva sua dúvida.")

            if st.session_state.get('decisao_temp'):
                st.markdown(f"<div class='card-pink'>{st.session_state['decisao_temp']}</div>", unsafe_allow_html=True)
                if st.session_state.get('app_sugerido_decisao'):
                    renderizar_encaminhamento(st.session_state['app_sugerido_decisao'])
                st.markdown("""<div class="disclaimer">⚠️ Esta análise é um apoio à reflexão, não uma recomendação definitiva — a decisão final e a responsabilidade por ela são sempre suas.</div>""", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['decisao_temp'], file_name="analise_decisao.txt", mime="text/plain", key="vidainte42")

    # --- RODAPÉ ---
    st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Vida Inteligente — Gerente Pessoal de Vida com IA · Quiz Com Prêmios"
        "</div>", unsafe_allow_html=True
    )

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
