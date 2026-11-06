import random
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Duelo de Cartas", page_icon="🃏", layout="centered")

# Inicializar el estado del juego si no existe
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "round_message" not in st.session_state:
    st.session_state.round_message = "¡Presiona 'Robar Carta' para comenzar el juego!"
if "player_card" not in st.session_state:
    st.session_state.player_card = None
if "computer_card" not in st.session_state:
    st.session_state.computer_card = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Definición de la baraja
suits = ["♠️", "♥️", "♦️", "♣️"]
values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def get_random_card():
  val_name = random.choice(list(values.keys()))
  suit = random.choice(suits)
  return {"name": val_name, "suit": suit, "value": values[val_name]}


# Interfaz Gráfica
st.title("🃏 Duelo de Cartas: Streamlit Edition")
st.write(
    "¡Bienvenido! Cada ronda ambos roban una carta. El valor más alto gana un"
    " punto. ¡El primero en llegar a **5 puntos** gana la partida!"
)

# Mostrar Puntuación
col_score1, col_score2 = st.columns(2)
with col_score1:
  st.metric(label="Tus Puntos", value=st.session_state.player_score)
with col_score2:
  st.metric(label="Puntos de la Computadora", value=st.session_state.computer_score)

st.markdown("---")

# Contenedor de las cartas
col_card1, col_card2 = st.columns(2)

with col_card1:
  st.subheader("Tu Carta")
  if st.session_state.player_card:
    card = st.session_state.player_card
    st.markdown(
        f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: #f9f9f9;">
                <h1 style="color: black; margin: 0;">{card['name']}</h1>
                <h2 style="margin: 0;">{card['suit']}</h2>
            </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.info("Sin carta")

with col_card2:
  st.subheader("Carta de la Computadora")
  if st.session_state.computer_card:
    card = st.session_state.computer_card
    st.markdown(
        f"""
            <div style="border: 2px solid #ccc; border-radius: 10px; padding: 20px; text-align: center; background-color: #f9f9f9;">
                <h1 style="color: black; margin: 0;">{card['name']}</h1>
                <h2 style="margin: 0;">{card['suit']}</h2>
            </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.info("Sin carta")

st.markdown("### Resultado de la ronda:")
st.info(st.session_state.round_message)

# Controles del juego
if not st.session_state.game_over:
  if st.button("🎴 Robar Carta", type="primary", use_container_width=True):
    p_card = get_random_card()
    c_card = get_random_card()

    st.session_state.player_card = p_card
    st.session_state.computer_card = c_card

    if p_card["value"] > c_card["value"]:
      st.session_state.player_score += 1
      st.session_state.round_message = (
          f"🎉 ¡Ganaste la ronda! ({p_card['name']} {p_card['suit']} le gana"
          f" a {c_card['name']} {c_card['suit']})"
      )
    elif p_card["value"] < c_card["value"]:
      st.session_state.computer_score += 1
      st.session_state.round_message = (
          f"💻 La computadora gana la ronda. ({c_card['name']} {c_card['suit']}"
          f" le gana a {p_card['name']} {p_card['suit']})"
      )
    else:
      st.session_state.round_message = (
          f"🤝 ¡Empate! Ambos sacaron {p_card['name']}."
      )

    # Verificar si alguien ganó el juego (5 puntos)
    if st.session_state.player_score >= 5:
      st.session_state.game_over = True
      st.session_state.round_message = (
          "🏆 ¡Felicidades! Has ganado la partida completa."
      )
    elif st.session_state.computer_score >= 5:
      st.session_state.game_over = True
      st.session_state.round_message = (
          "💀 La computadora ha ganado la partida. ¡Inténtalo de nuevo!"
      )

    st.rerun()
else:
  st.success("¡El juego ha terminado!")
  if st.button("🔄 Jugar de Nuevo", use_container_width=True):
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.round_message = (
        "¡Presiona 'Robar Carta' para comenzar el juego!"
    )
    st.session_state.player_card = None
    st.session_state.computer_card = None
    st.session_state.game_over = False
    st.rerun()