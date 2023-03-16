import nb_log
from pyfiglet import Figlet,FigletFont

fonts_str = '''univers
thin
stop
stellar
starwars
speed
slant
roman
doh
'''

# for font in FigletFont().getFonts():
for font in  fonts_str.split('\n'):
    # f = Figlet(font="slant", width=300)  # 字体和宽度，可以为空即默认
    font = font.replace(' ', '')
    if font == '':
        continue
    print('font:',font)
    f =  Figlet(font=font, width=1000,)  # 字体和宽度，可以为空即默认

    # print(f.renderText("FUNBOOST"))
    nb_log.defaul_logger.warning(f.renderText("FUNBOOST"))
"""
  _______________________
 /_  __/ ____/ ___/_  __/
  / / / __/  \__ \ / /
 / / / /___ ___/ // /
/_/ /_____//____//_/

"""


'''
univers
thin
stop
stellar
starwars
speed
slant
roman
doh
'''