from subprocess import run as sprun


def termux_api_toast(msg: str,
                     position: str = "bottom",
                     background_color: str = "white",
                     text_color: str = "black"):
    sprun(['termux-toast',
           '-g', str(position),
           '-b', str(background_color),
           '-c', str(text_color),
           str(msg)],
          check=True)
