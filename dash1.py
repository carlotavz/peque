import dash
from dash import html, dcc, Input, Output, State

# Inicialización de la app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Archivos multimedia
VIDEO_URL = "assets/converted_output.mp4"  # Video
IMAGE_1_URL = "assets/oz.jpg"             # Primera imagen
IMAGE_2_URL = "assets/glinda.jpg"         # Segunda imagen
IMAGE_FINAL_URL = "assets/entradas.png"   # Imagen final
AUDIO_1_URL = "assets/Oz.mp3"             # Primer audio
AUDIO_2_URL = "assets/Ari.mp3"            # Segundo audio

# Layout de la app
app.layout = html.Div(
    [
        dcc.Store(id="state", data="video"),  # Estado inicial
        html.Div(
            id="media-container",
            children=[
                html.Video(
                    id="video-player",
                    src=VIDEO_URL,
                    controls=True,
                    autoPlay=True,
                    muted=True,  # Silenciar para permitir reproducción automática
                    style={"display": "block", "width": "100%"},  # Visible inicialmente
                ),
                html.Img(
                    src=IMAGE_1_URL,
                    id="image-1",
                    style={"display": "none", "cursor": "pointer", "width": "100%"},
                ),
                html.Img(
                    src=IMAGE_2_URL,
                    id="image-2",
                    style={"display": "none", "cursor": "pointer", "width": "100%"},
                ),
                html.Img(
                    src=IMAGE_FINAL_URL,
                    id="final-image",
                    style={
                        "display": "none",
                        "width": "50%",
                        "margin": "auto",  # Centramos horizontalmente
                        "textAlign": "center",
                    },
                ),
            ],
            style={"textAlign": "center"},
        ),
        html.Audio(
            id="audio-player",
            controls=False,
            autoPlay=False,  # Se activará dinámicamente
            style={"display": "none"},
        ),
        html.Button(
            "Continuar",
            id="continue-button",
            style={
                "display": "none",  # Ocultar inicialmente
                "margin": "20px auto",  # Centramos el botón
                "textAlign": "center",
                "padding": "10px 20px",
                "fontSize": "16px",
                "cursor": "pointer",
            },
        ),  # Botón para avanzar manualmente
    ]
)

# Callback para mostrar el botón "Continuar" después del video
@app.callback(
    Output("continue-button", "style"),
    Input("video-player", "n_clicks"),  # Simulamos el final con un clic en el video
    State("state", "data"),
    prevent_initial_call=True,
)
def show_continue_button(video_clicks, state):
    if state == "video":
        return {
            "display": "block",  # Mostrar botón continuar
            "margin": "20px auto",
            "textAlign": "center",
            "padding": "10px 20px",
            "fontSize": "16px",
            "cursor": "pointer",
        }
    return dash.no_update

# Callback para manejar el flujo completo
@app.callback(
    [
        Output("video-player", "style"),
        Output("image-1", "style"),
        Output("image-2", "style"),
        Output("final-image", "style"),
        Output("audio-player", "src"),
        Output("audio-player", "autoPlay"),
        Output("audio-player", "style"),
        Output("state", "data"),
    ],
    [
        Input("continue-button", "n_clicks"),
        Input("image-1", "n_clicks"),
        Input("image-2", "n_clicks"),
    ],
    [State("state", "data")],
    prevent_initial_call=True,
)
def handle_flow(continue_clicks, img1_clicks, img2_clicks, state):
    # Etapa 1: Mostrar primera imagen después del video
    if state == "video" and continue_clicks:
        return (
            {"display": "none"},  # Ocultar video
            {"display": "block"},  # Mostrar primera imagen
            {"display": "none"},  # Ocultar segunda imagen
            {"display": "none"},  # Ocultar imagen final
            dash.no_update,
            False,
            {"display": "none"},  # Ocultar reproductor de audio
            "image-1",  # Nuevo estado
        )

    # Etapa 2: Reproducir primer audio al hacer clic en la primera imagen
    if state == "image-1" and img1_clicks:
        return (
            {"display": "none"},
            {"display": "block"},
            {"display": "none"},
            {"display": "none"},
            AUDIO_1_URL,  # Reproducir primer audio
            True,  # Activar reproducción automática
            {"display": "block"},  # Mostrar reproductor de audio
            "audio-1",  # Nuevo estado
        )

    # Etapa 3: Cambiar a la segunda imagen
    if state == "audio-1" and continue_clicks:
        return (
            {"display": "none"},
            {"display": "none"},  # Ocultar primera imagen
            {"display": "block"},  # Mostrar segunda imagen
            {"display": "none"},
            dash.no_update,
            False,
            {"display": "none"},  # Ocultar reproductor de audio
            "image-2",  # Nuevo estado
        )

    # Etapa 4: Reproducir segundo audio al hacer clic en la segunda imagen
    if state == "image-2" and img2_clicks:
        return (
            {"display": "none"},
            {"display": "none"},
            {"display": "block"},
            {"display": "none"},
            AUDIO_2_URL,  # Reproducir segundo audio
            True,  # Activar reproducción automática
            {"display": "block"},  # Mostrar reproductor de audio
            "audio-2",  # Nuevo estado
        )

    # Etapa 5: Mostrar imagen final
    if state == "audio-2" and continue_clicks:
        return (
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},  # Ocultar segunda imagen
            {"display": "block"},  # Mostrar imagen final
            dash.no_update,
            False,
            {"display": "none"},  # Ocultar reproductor de audio
            "final",  # Estado final
        )

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
