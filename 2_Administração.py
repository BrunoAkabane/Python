import streamlit as st
import json
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent.parent

CONFIG_DIR = BASE_DIR / "config"

SISTEMAS_FILE = CONFIG_DIR / "sistemas.json"
JUSTIFICATIVAS_FILE = CONFIG_DIR / "justificativas.json"

with open(SISTEMAS_FILE, encoding="utf-8") as f:
    sistemas = json.load(f)

with open(JUSTIFICATIVAS_FILE, encoding="utf-8") as f:
    justificativas = json.load(f)

st.title("⚙️ Administração")

# Mensagem de confirmação que sobrevive ao st.rerun()
if "mensagem" in st.session_state:
    st.success(st.session_state.pop("mensagem"))

# ======================
# Sistema
# ======================

st.subheader("Novo Sistema")

novo_sistema = st.text_input(
    "Nome do Sistema"
)

if st.button("Adicionar Sistema"):

    novo_sistema = novo_sistema.strip()

    if novo_sistema:

        if novo_sistema not in sistemas:

            sistemas[novo_sistema] = []

            with open(
                SISTEMAS_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    sistemas,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            st.success(
                "Sistema cadastrado"
            )

        else:

            st.warning(
                "Este sistema já existe."
            )

# ======================
# Perfil
# ======================

st.divider()

if sistemas:

    sistema_admin = st.selectbox(
        "Sistema",
        list(sistemas.keys())
    )

    novo_perfil = st.text_input(
        "Novo Perfil"
    )

    if st.button("Adicionar Perfil"):

        novo_perfil = novo_perfil.strip()

        if novo_perfil:

            if novo_perfil not in sistemas[sistema_admin]:

                sistemas[sistema_admin].append(
                    novo_perfil
                )

                with open(
                    SISTEMAS_FILE,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        sistemas,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )

                st.success(
                    "Perfil cadastrado"
                )

            else:

                st.warning(
                    "Este perfil já existe neste sistema."
                )

else:

    st.info(
        "Cadastre um sistema para poder adicionar perfis."
    )

# ======================
# Justificativa
# ======================

st.divider()

nova_justificativa = st.text_input(
    "Nova Justificativa"
)

if st.button(
    "Adicionar Justificativa"
):

    nova_justificativa = nova_justificativa.strip()

    if nova_justificativa:

        if nova_justificativa not in justificativas["justificativas"]:

            justificativas[
                "justificativas"
            ].append(
                nova_justificativa
            )

            with open(
                JUSTIFICATIVAS_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    justificativas,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            st.success(
                "Justificativa cadastrada"
            )

        else:

            st.warning(
                "Esta justificativa já existe."
            )

st.divider()

st.subheader("Sistemas")

st.json(sistemas)

st.divider()

st.subheader("Justificativas")

st.write(
    justificativas["justificativas"]
)

st.divider()

# ======================
# Remover Perfil
# ======================

st.subheader("🗑️ Remover Perfil")

if sistemas:

    sistema_remover = st.selectbox(
        "Sistema para Remoção",
        list(sistemas.keys()),
        key="sistema_remover"
    )

    if sistemas[sistema_remover]:

        perfil_remover = st.selectbox(
            "Perfil",
            sistemas[sistema_remover],
            key="perfil_remover"
        )

        if st.button(
            "Excluir Perfil",
            key="btn_excluir_perfil"
        ):

            sistemas[sistema_remover].remove(
                perfil_remover
            )

            with open(
                SISTEMAS_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    sistemas,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            st.session_state["mensagem"] = "Perfil removido com sucesso."

            st.rerun()

    else:

        st.info(
            "Este sistema não possui perfis."
        )

else:

    st.info(
        "Não há sistemas cadastrados."
    )

# ======================
# Remover Sistema
# ======================

st.divider()

st.subheader("🗑️ Remover Sistema")

if sistemas:

    sistema_excluir = st.selectbox(
        "Sistema",
        list(sistemas.keys()),
        key="sistema_excluir"
    )

    confirmar = st.checkbox(
        f"Confirmo a exclusão de {sistema_excluir}"
    )

    if confirmar:

        if st.button(
            "Excluir Sistema",
            key="btn_excluir_sistema"
        ):

            del sistemas[sistema_excluir]

            with open(
                SISTEMAS_FILE,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    sistemas,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            st.session_state["mensagem"] = "Sistema removido."

            st.rerun()

else:

    st.info(
        "Não há sistemas cadastrados."
    )

# ======================
# Remover Justificativa
# ======================

st.divider()

st.subheader("🗑️ Remover Justificativa")

if justificativas["justificativas"]:

    justificativa_remover = st.selectbox(
        "Justificativa",
        justificativas["justificativas"],
        key="justificativa_remover"
    )

    if st.button(
        "Excluir Justificativa",
        key="btn_excluir_justificativa"
    ):

        justificativas[
            "justificativas"
        ].remove(
            justificativa_remover
        )

        with open(
            JUSTIFICATIVAS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                justificativas,
                f,
                indent=4,
                ensure_ascii=False
            )

        st.session_state["mensagem"] = "Justificativa removida."

        st.rerun()

else:

    st.info(
        "Não há justificativas cadastradas."
    )

# ======================
# Resumo dos Sistemas
# ======================

st.divider()

st.subheader("📋 Resumo dos Sistemas")

dados = []

for sistema, perfis in sistemas.items():

    dados.append(
        {
            "Sistema": sistema,
            "Quantidade de Perfis": len(perfis)
        }
    )

df_sistemas = pd.DataFrame(dados)

st.dataframe(
    df_sistemas
)


# ======================
# Perfis por Sistema
# ======================