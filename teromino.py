import random, time, pygame, sys
import jieba
import pickle,os
from pygame.locals import *
import msvcrt
import serial # 导入串口包
import time # 导入时间包
#下面两行是初始化串口数据和调整定义波特率对应传感器接受数据
#ser = serial.Serial("COM8",115200,timeout = 5)
#ser.flushInput() # 清空缓冲区
flag=True
#flag=False #3由于多次尝试都没有成功打通关，所以用这种方式来跳入成功后的循环内容实现预览
FPS = 25  #游戏刷新率
WINDOWWIDTH =640 #整个游戏屏幕的宽
WINDOWHEIGHT =480#整个游戏屏幕的高
BOXSIZE = 20#每个小格子的宽和高
BOARDWIDTH = 10#游戏窗口本身有10个方块的宽度
BOARDHEIGHT = 20#游戏窗口本身有20个方块的高度
BLANK = '.'#表示空白空格
#对玩家命令的设置
MOVESIDEWAYSFREQ = 0.15 #按向左箭头键或向右箭头键每次持续按下超过0.15秒的时候，砖块相应的移动一个空格
MOVEDOWNFREQ = 0.1  #按向下头键每次持续按下超过0.1秒的时候，砖块向下一个空格
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)#(0INDOWWIDTH是总窗口的宽度-游戏界面一行上的方块个数*每个方块的宽度)/2窗口左边或右边剩下的像素数
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5#TOPMARGIN：游戏窗口上面剩下的像素数=总窗口的高度-（游戏界面一列上的方块个数*每个方块的高度）-5
#定义各种颜色RGB色域
WHITE  = (255, 255, 255)#白色
GRAY  = (185, 185, 185)#灰色
BLACK  = ( 0, 0, 0)#黑色
RED   = (155, 80,32)#红色
GREEN  = ( 0, 155, 0)#绿色
BLUE  = ( 0, 0, 155)#蓝色
YELLOW  = (155, 155, 0)#
PINK = (255,192,203)
LIKE = (123,128,68)  #随机定义的颜色
BORDERCOLOR = WHITE#边界颜色
BGCOLOR = PINK#背景颜色
TEXTCOLOR = WHITE#文字颜色
COLORS  = (BLUE,GREEN,RED,YELLOW,LIKE) #方块五种颜色，存于COLORS元组中
TEMPLATEWIDTH = 5#砖块模板宽templatewidth
TEMPLATEHEIGHT = 5#砖块模板高templateheight

S_SHAPE_TEMPLATE = [['.....', #S形状的模板
      '.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....', #S逆时针变化的形状
      '..O..',
      '..OO.',
      '...O.',
      '.....']]

Z_SHAPE_TEMPLATE = [['.....', #Z形模板
      '.....',
      '.OO..',
      '..OO.',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '.O...',
      '.....']]

I_SHAPE_TEMPLATE = [['..O..', #I型模板
      '..O..',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      'OOOO.',
      '.....',
      '.....']]

PLUS_SHAPE_TEMPLATE = [['.....', #PLUS型模板
      '.....',
      '.O...',
      'OOO..',
      '.O...']]
PLUSPLUS_SHAPE_TEMPLATE = [['.....', #PLUSPLUS型模板
      '.....',
      '.O...',
      'O.O..',
      '.O...']]
PLUSPLUSPLUS_SHAPE_TEMPLATE = [['.....', #PLUSPLUSPLUS型模板
      '.....',
      '.O.O.',
      'O.O.O',
      '.O.O.']]
O_SHAPE_TEMPLATE = [['.....', #O型模板
      '.....',
      '.OO..',
      '.OO..',
      '.....']]

U_SHAPE_TEMPLATE = [['.....', #U型模板
      '.O..O',
      '.OOOO',
      '.....',
      '.....'],
     ['.....',
      '..OO.',
      '..O..',
      '..O..',
      '..OO.'],
     ['.....',
      '.....',
      'OOOO.',
      'O..O.',
      '.....'],
     ['.OO..',
      '..O..',
      '..O..',
      '.OO..',
      '.....']]
UU_SHAPE_TEMPLATE = [['.....', #UU型模板
      '.O.OO',
      '.OOOO',
      '.....',
      '.....'],
     ['.....',
      '..OO.',
      '..O..',
      '..OO.',
      '..OO.'],
     ['.....',
      '.....',
      'OOOO.',
      'OO.O.',
      '.....'],
     ['.OO..',
      '.OO..',
      '..O..',
      '.OO..',
      '.....']]

J_SHAPE_TEMPLATE = [['.....', #J型模板
      '.O...',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..OO.',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '...O.',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....']]
JJ_SHAPE_TEMPLATE = [['.....', #JJ型模板
      '.O...',
      '..OO.',
      '.....',
      '.....'],
     ['.....',
      '...O.',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OO..',
      '...O.',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '.O...',
      '.....']]
JJJ_SHAPE_TEMPLATE = [['.....', #JJJ型模板
      '.O...',
      '..O..',
      '...O.',
      '.....'],
     ['.....',
      '...O.',
      '..O..',
      '.O...',
      '.....'],
     ['.....',
      '.O...',
      '..O..',
      '...O.',
      '.....'],
     ['.....',
      '...O.',
      '..O..',
      '.O...',
      '.....']]



T_SHAPE_TEMPLATE = [['.....', #T型模板
      '..O..',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....']]
TT_SHAPE_TEMPLATE = [['.....', #TT型模板
      '..O..',
      '.O.O.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '...O.',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.O.O.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.O...',
      '..O..',
      '.....']]
TTT_SHAPE_TEMPLATE = [['.....', #TTT型模板
      '..O.O',
      '.O.O.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '...O.',
      '..O..',
      '...O.'],
     ['.....',
      '.....',
      '.O.O.',
      'O.O..',
      '.....'],
     ['.....',
      '..O..',
      '.O...',
      '..O..',
      '.O...']]
TTTT_SHAPE_TEMPLATE = [['.....', #TTTT型模板
      'O.O.O',
      '.O.O.',
      '.....',
      '.....'],
     ['...O.',
      '..O..',
      '...O.',
      '..O..',
      '...O.'],
     ['.....',
      '.....',
      '.O.O.',
      'O.O.O',
      '.....'],
     ['.O...',
      '..O..',
      '.O...',
      '..O..',
      '.O...']]
LOVE_SHAPE_TEMPLATE = [['.....', #LOVE型模板
      '.OO..',
      '..OO.',
      '..O.',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '...O.',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..OO.',
      '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE, #PIECES是一个字典，它储存了所有不同的模板(列表)。每个模板都拥有一个形状所有可能的旋转(列表)。
   'Z': Z_SHAPE_TEMPLATE,
   'J': J_SHAPE_TEMPLATE,
 #  'L': L_SHAPE_TEMPLATE,
   'I': I_SHAPE_TEMPLATE,
   'O': O_SHAPE_TEMPLATE,
   'U': U_SHAPE_TEMPLATE,
  # 'LOVE': LOVE_SHAPE_TEMPLATE,
   'PLUS': PLUS_SHAPE_TEMPLATE,
   'T': T_SHAPE_TEMPLATE}





#设置函数运行,设置基础的窗格和工具箱
def main(): #main()函数创建全局常量，并且显示了在游戏运行的时候出现的初始屏幕。
 global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT,flag,pause,a,b  #设置频率，上下边界
 pygame.init()
 #在inport pygame之后 调用其他函数之前总要调用这个函数，用于初始化
 #我们已经知道python有一个特殊的“工具包（模块）”叫pygame了。在我们要动手用它完成我们的想法之前，
 #电脑这个强迫症需要我们检查一遍，这个工具包是否完整，能否正常给我们提供帮助。而这个检查的动作，就是pygame.init()
 FPSCLOCK = pygame.time.Clock()
 #设计速率让计算机在一个固定的速度运行，在游戏每一次迭代都会设置一个暂停，以防程序运行过快.
 DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
 #displaysurf,pygame.display.set_mode()的参数是一个元组,该元祖中有两个参数,
 #即：创建窗口的宽和高，单位是像素，该函数返回pygame.Surface对象
 BASICFONT = pygame.font.Font('freesansbold.ttf', 20)#字体，第一个参数是字体，第二个是字体大小
 BIGFONT = pygame.font.Font('freesansbold.ttf', 20)
 pygame.display.set_caption("welcome cxy's teromino!")#窗口标题
 showTextScreen("welcome cxy's teromino !!!!!")#设置在开始界面显示的文字
 pygame.init()
 screen = pygame.display.set_mode((640,480))
 pygame.display.set_caption("欢迎来到方块世界")

 bg_size = width,height = 600,400
 #image = "pause.jpg"
 #pygame.image.load("pause.jpg").convert_alpha()
 #unpause_imgae = pygame.image.load(r"D:\python\pythonwork\小游戏\cxy's tetris\源代码部分\keep.jpg").convert_alpha()
# pause_imgae = pygame.image.load("pause.jpg").convert_alpha()
# unpause_imgae = pygame.image.load("keep.jpg").convert_alpha()
 #pause_rect = pause_imgae.get_rect()
 #pause_rect.center = width // 2,height // 2
 clock = pygame.time.Clock()
 pause=False


 while True:
  while flag:

      APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
      os.chdir(APP_FOLDER)
      #file=r'D:\python\pythonwork\小游戏\俄罗斯方块\我走后.mp3'	# 音乐的路径
      pygame.mixer.init()			      # 初始化
      pygame.mixer.music.load('我走后5.mp3')	# 加载音乐文件
      pygame.mixer.music.play()			# 开始播放音乐流
      pygame.mixer.music.set_volume(0.25)
      pygame.mixer.Sound("00.ogg")
      pause = False

      #if pygame.mixer.music.get_busy()==False:
      # pygame.mixer.music.load("我走后.mp3")
      #if level==2:
      #pygame.mixer.music.load("我走后2.mp3")
      runGame() #调用runGame()开始游戏，当游戏失败的时候,runGame()将返回main(),
      pygame.mixer.music.stop()#然后main()会停止背景音乐
      showTextScreen('gameover 0.0 try again')#并显示游戏结束屏幕。当玩家按下一个键，showTextScreen()

 #以下是代码部分对应蓝牙串口和数据的接受操作
 #     count = ser.inWaiting() # 获取串口缓冲区数据
 #     if count !=0 :
 #          recv = ser.read(ser.in_waiting).decode("gbk") # 读出串口数据，数据采用gbk编码
 #           a,b = map(int,recv.split(","))
 #           print(a,b) # 打印一下子
 #     time.sleep(0.1) # 延时0.1秒，免得CPU出问题
     # 读取数据之后对数据设置阈值，得到想应对应的按键操作
 #      a,b = map(int,input(recv).split(" "))
  #     if a >0:
   #          a=key_LEFT
    #   else:
     #        a =key_RIGHT
     #  if b>0:
      #       b=KEYUP
      #在后面的判断语句中加入or  判断进行可以利用串口或者是按键识别

  while not flag:
      BGCOLOR = RED#背景颜色
      APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
      os.chdir(APP_FOLDER)
      #file=r'D:\python\pythonwork\小游戏\俄罗斯方块\我走后.mp3'	# 音乐的路径
      pygame.mixer.init()			      # 初始化
      pygame.mixer.music.load('我走后3.mp3')	# 加载音乐文件
      pygame.mixer.music.play()			# 开始播放音乐流

      pygame.mixer.Sound("00.ogg")
      for event in pygame.event.get():
            if event.type ==  QUIT:
                  sys.exit()
            if event.type==MOUSEBUTTONDOWN:
                  if event.button==1:
                        pygame.mixer.Sound("3.mp3").play()
                  if event.button==2:
                        pygame.mixer.Sound('00.ogg').play()
            if event.type == KEYDOWN:
                  if event.key == K_SPACE:
                        pause = not pause
            screen.fill((0,0,0))

            #if pause:
            #      screen.blit(pause_imgae,pause_rect)
            #else:
            #      screen.blit(unpause_imgae,pause_rect)

            pygame.display.flip()
            clock.tick(30)
      lastMoveDownTime = time.time()#lastMoveDownTime最后按向下方向键的时间
      lastMoveSidewaysTime = time.time()#lastMoveSidewaysTime最后按左右向键的时间
      lastFallTime = time.time()#最后下落砖块的时间
      movingDown = False #没有按下向下方向键
      movingLeft = False #没有按下向左方向键
      movingRight = False #没有按下向右方向键
      score = 0 #得分
      fallingPiece = getNewPiece() #fallingPiece变量将设置为能够被玩家操作的当前下落的砖块
      nextPiece = getNewPiece()
      level, fallFreq = calculateLevelAndFallFreq(score)
      board = getBlankBoard()
      DISPLAYSURF.fill(BGCOLOR)
      #drawBoard(board)
      drawStatus(score, level)
      drawNextPiece(nextPiece)
      showTextScreen('you are winner!!')

def runGame():  #运行的游戏代码
#初始化数据
 board = getBlankBoard()       #创建一个空白游戏板数据结构
 lastMoveDownTime = time.time()#lastMoveDownTime最后按向下方向键的时间
 lastMoveSidewaysTime = time.time()#lastMoveSidewaysTime最后按左右向键的时间
 lastFallTime = time.time()#最后下落砖块的时间
 movingDown = False #没有按下向下方向键
 movingLeft = False #没有按下向左方向键
 movingRight = False #没有按下向右方向键
 score = 0 #得分
 level, fallFreq = calculateLevelAndFallFreq(score)#外置函数，计算关卡数和下落频率，因为此时score=0，所以经计算后level=1,fallFreq=0.25

 fallingPiece = getNewPiece() #fallingPiece变量将设置为能够被玩家操作的当前下落的砖块
 nextPiece = getNewPiece() #nextPice为在屏幕的Next部分出现的砖块，即下一个将要下落的砖块


 while True:                        # 游戏主循环，它负责砖块在落向底部的过程中
  #count = ser.inWaiting() # 获取串口缓冲区数据
  #if count !=0 :
  #    recv = ser.read(ser.in_waiting).decode("gbk") # 读出串口数据，数据采用gbk编码
  #    a,b = map(int,recv.split(","))
  #    print(a,b) # 打印一下子
  #time.sleep(0.1)
  #if a>0:#467-514 修改即可
  #      a=K_KEFT
  #else :
  #      a=K_RIGHT
  #if b>0:
  #      b=K_UP
  if fallingPiece == None:          #在下落的砖块已经着陆之后，fallingPiece变量设置为None
   fallingPiece = nextPiece         #这意味着nextPiece中的砖块将会复制到fallingPiece中。
   nextPiece = getNewPiece()        #生成新的新的nextPiece砖块，砖块可以通过getNewPiece()函数生成。
   lastFallTime = time.time() #该变量也重新设置为当前时间，以便砖块能够在fallFreq中所设置的那么多秒之内下落。
   if not isValidPosition(board, fallingPiece):
     #游戏结束判定，isValidPosition判定是否还有空白位置
    return #在这种情况下 runGame()函数将被返回。

  for event in pygame.event.get(): #事件处理循环负责玩家旋转下落的砖块，移动下落的砖块。
    #松开一个箭头键将会把movingLeft或movingRight或movingDown变量设置为False,表示玩家不再想
    #要让砖块朝着该方向移动。随后的代码将会根据这些“moving”变量中的Boolean值来确定做什么。

   if event.type == KEYUP:#当按键弹起的时候响应KEYUP事件
    if (event.key == K_LEFT):#判断当前弹起的按键是否为左方向键
     movingLeft = False #是的话置为False,表示玩家不再想要让砖块朝着该方向移动。
    elif (event.key == K_RIGHT):
     movingRight = False
    elif (event.key == K_DOWN):
     movingDown = False
  #  elif event.key == pygame.QUIT :
  #    pygame.quit()
  #   exit()
   elif event.type == KEYDOWN:#当按键按下的时候响应KEYDOWN事件
    if (event.key == K_LEFT) and isValidPosition(board, fallingPiece, adjX=-1):
    #当按下的按键为向左方向键，并且向左移动一个位置有效
     fallingPiece['x'] = fallingPiece['x'] -1 #左移
     movingLeft = True #将movingLeft变量设置为True，并且为了确保落下的砖块不会既向左又向右移动
     movingRight = False #将 movingRight设置为False
     lastMoveSidewaysTime = time.time() #lastMoveSidewaysTime更改为当前时间
#设置了movingLeft，movingRigh=true表示玩家按住左键没有松开，保持移动

    elif (event.key == K_RIGHT ) and isValidPosition(board, fallingPiece, adjX=1):
     fallingPiece['x'] =fallingPiece['x'] + 1
     movingRight = True
     movingLeft = False
     lastMoveSidewaysTime = time.time()

      #向上键，旋转，字典遍历加一即可，如果+1后超过字典内元素个数，对字典长度取余即可
    elif event.key == K_UP :
     fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
     if not isValidPosition(board, fallingPiece):
     #由于新的旋转位置与游戏板上已有的一些方块重叠而导致新的旋转位置无效，那么，
     #我们想要通过从fallingPiece['rotation']减去1而切换回最初的旋转。我们也可以使用len(PIECES[fallingPiece['shape']])来模除
     #它，以便如果新的值为-1，模除将其改为列表中的最后一次旋转。????
      fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])



    #向下键，加速
    elif (event.key == K_DOWN ):
     movingDown = True # movingDown设置为True
     if isValidPosition(board, fallingPiece, adjY=2):#下一个位置有效
      fallingPiece['y'] = fallingPiece['y'] +2 #移动
     lastMoveDownTime = time.time()
     #lastMoveDownTime重新设置为当前时间。随后将检查这些变量，以确保只要按下向下箭头键的时候，砖块就会以较快的速率下降
    #elif event.key ==

  if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:#MOVESIDEWAYSFREQ = 0.15 按向左或向右超过0.15秒
   if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):#如果是向左方向键，并且向左一个位置有效
    fallingPiece['x'] =fallingPiece['x'] - 1#左移动一个位置
   elif movingRight and isValidPosition(board, fallingPiece, adjX=1):#如果是向右方向键，并且向左一个位置有效
    fallingPiece['x'] =fallingPiece['x'] + 1#右移动一个位置
   lastMoveSidewaysTime = time.time() #将lastMoveSidewaysTime更新为当前时间。

  if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
  #MOVEDOWNFREQ = 0.1 按向下方向键超过0.1秒，并且向下一个位置有效
   fallingPiece['y'] = fallingPiece['y'] + 1#向下移动一个位置
   lastMoveDownTime = time.time()#将laslastMoveDownTime更新为当前时间。

  #让砖块自然落下
  if time.time() - lastFallTime > fallFreq:#fallFreq向下移动的速率
   if not isValidPosition(board, fallingPiece, adjY=1):#当砖块下一个位置无效时，即表示砖块当前已经着陆了。
    addToBoard(board, fallingPiece) #在游戏板数据结构中记录这个着陆的砖块
    score = score + removeCompleteLines(board)# removeCompleteLines()将负责删除掉游戏板上任何已经填充完整的行，并且将方块向下推动。
    #removeCompleteLines()函数还会返回一个整数值，表明消除了多少行，以便我们将这个数字加到得分上。
    level, fallFreq = calculateLevelAndFallFreq(score)#由于分数已经修改了，我们调用calculateLevelAndFallFreq()函数来更新当前的关卡以及砖块下落得频率。
    if level ==2 :
        PIECES["T"]=TT_SHAPE_TEMPLATE
    if level ==3:
        PIECES["T"]=TTT_SHAPE_TEMPLATE
        PIECES["J"]=JJ_SHAPE_TEMPLATE
        PIECES["PLUS"]=PLUSPLUS_SHAPE_TEMPLATE
    if level ==4:
        PIECES["T"]=TTTT_SHAPE_TEMPLATE
        PIECES["J"]=JJ_SHAPE_TEMPLATE
        PIECES["PLUS"]=PLUSPLUSPLUS_SHAPE_TEMPLATE
    if level ==5:
        PIECES["T"]=O_SHAPE_TEMPLATE
        PIECES["J"]=O_SHAPE_TEMPLATE
        PIECES["PLUS"]=O_SHAPE_TEMPLATE
        PIECES["Z"]=O_SHAPE_TEMPLATE
        PIECES["I"]=O_SHAPE_TEMPLATE
        PIECES["U"]=O_SHAPE_TEMPLATE
    if level == 6:
          flag=False
    fallingPiece = None#最后我们将fallingPiece变量设置为None,以表示下一个砖块应该变为新的下落砖块，并且应该生成一个随机的新砖块作为下一个砖块。
   else:
    # 如果砖块没有着陆，我们直接将其Y位置向下设置一个空格，并且将lastFallTime重置为当前时间
    fallingPiece['y'] = fallingPiece['y'] +1
    lastFallTime = time.time()

  # drawing everything on the screen
  DISPLAYSURF.fill(BGCOLOR)
  drawBoard(board)
  drawStatus(score, level)
  drawNextPiece(nextPiece)
  if fallingPiece != None:#砖块没有下落到底部
   drawPiece(fallingPiece)
  pygame.display.update()
  FPSCLOCK.tick(FPS)





def makeTextObjs(text, font, color): #输入文本的简易函数
 surf = font.render(text, True, color)
 return surf, surf.get_rect()

def checkForKeyPress():
 # checkForKeyPress()函数和它在Wormy游戏中所做的事件相同。首先，
 # 它调用checkForQuit()来处理任何的QUIT事件(或者是专门针对Esc键的KEYUP事件)，
 # 如果有任何这样的事件 #就会终止程序。然后，它从事件队列中提取出所有的KEYDOWN, KEYUP事件。
 # 它会忽略掉 # 任何的KEYDOWN事件(针对pygame.event.get()指定了KEYDOWN,从而从事件队列中清
 # 除掉该类事件)。
 #如果事件队列中没有KEYUP事件，那么该函数返回None。
 #for event in pygame.event.get([KEYDOWN, KEYUP]):
 for event in pygame.event.get(QUIT):
    pygame.quit()
    sys.exit()
 for event in pygame.event.get(KEYUP):
  if event.key ==K_ESCAPE:
   pygame.quit()
   sys.exit()
   pygame.event.post(event)
  if event.type == KEYDOWN:
    continue
  return event.key

#原来的代码
 # if event.type == KEYDOWN:
  #    continue
  #return event.key

 return None

def calculateLevelAndFallFreq(score):
  #每次玩家填满一行，起分数都将增加1分。每增加5分，游戏就进入下一个关卡，砖块下落得会更快。关卡和下落的频率都是通过传递
 level = int(score / 2) + 1 #给该函数的分数来计算的。要计算关卡，我们使用int()来舍入除以5以后的分数。因此如果分数是0-4之间的任何数字，int()调用会将其
 fallFreq = 0.32 - (level * 0.03) #舍入到0。代码这里的+1部分，是因为我们想要第一个关卡作为第一关，而不是第0关。当分数达到10分的时候，int(10/10)将会计算为1


 return level, fallFreq
 #并且+1将会使得关卡变为2，改变频率下落
 #为了计算下落的频率，我们首先有一个基准值0.27(这意味着每0.27秒，砖块会自然地下落一次)。然后，我们将关卡值乘以0.02，并且从基准时间0.27中减去它。因此，对于关卡1，
 #我们从0.27中减去0.02*1得到0.25。在关卡2中我们减去0.02*2得到0.23。对于每一个关卡来说，砖块下落的速度都比之前的关卡块了0.02秒。

#getNewPiece()函数产生一个随机的砖块，放置于游戏板的顶部(设置'y'=-2)。
def getNewPiece():
 shape = random.choice(list(PIECES.keys()))
 #PIECES是一个字典，它的键为代表形状的字母，值为一个形状所有可能的旋转(列表的列表)。
 #PIECES.keys()返回值是(['Z','J','L','I','O','T'])的元组，list(PIECES.keys())返回值是['Z','J','L','I','O','T']列表
 #这样转换是因为random.choice()函数只接受列表值作为其参数。 random.choice()函数随机地返回列表中的一项的值，即可能是'Z'。
 newPiece = {'shape': shape,
    'rotation': random.randint(0, len(PIECES[shape]) - 1), #rotation：随机出砖块是多个旋转形装的哪个
    #PIECES['Z']的返回值为[[形状],[形状]]，len(PIECES['z'])的返回值为2 2-1=1 random.randint(0,1)随机范围是[0,1]
    'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2), #'x'代表砖块5x5数据结构左上角第一个方格的横坐标，键的值总是要设置为游戏板的中间。
    'y': -2, #'x'代表砖块5x5数据结构左上角第一个方格的纵坐标，'y'键的值总是要设置为-2以便将其放置到游戏板上面一点点(游戏板的首行是0行)
    'color': random.randint(0, len(COLORS) - 1)#COLORS：不同颜色的一个元组
    }
 return newPiece#getNewPiece()函数返回newPiece字典

#给游戏板数据结构添加砖块(这里已经不再是可以移动的砖块，而是把游戏板底部重新绘制出来)
def addToBoard(board, piece): #记录已经着陆的砖块，这个函数是测出有效砖块之后把他放到游戏板里面
 for x in range(TEMPLATEWIDTH): #位置在检测到一个砖块着陆之后运行
  for y in range(TEMPLATEHEIGHT):#嵌套for遍历5x5砖块数据结构,当找到一个有效砖块时，将其添加到游戏板中  template width template height
   if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
    board[x + piece['x']][y + piece['y']] = piece['color'] #游戏板数据结构的值有两种形式：数字(表示砖块颜色)，'.'即空白，表示该处没有有效砖块

def getBlankBoard(): #创建一个新的游戏板数据结构。
 board = [] #创建一个空白的游戏板
 for i in range(BOARDWIDTH):# range(10)=[0,9] BOARDWIDTH=10 BLANK = '.' #表示空白空格
  board.append([BLANK] * BOARDHEIGHT)
 #board[0]-board[9]每一个变量的值都是20个.组成的列表
 return board

def isOnBoard(x, y):#isOnBoard()函数检查参数x,y坐标是否存在于游戏板上
 return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT#BOARDWIDTH=10，BOARDHEIGHT=20

def isValidPosition(board, piece, adjX=0, adjY=0):
#board:游戏板 piece：砖块 adjX,adjY表示5x5砖块左上角方块的坐标（在游戏板里的坐标位置）
#isValidPosition()如果砖块中所有的方块都在游戏板上并且没有和游戏板上任何方块重叠，那么返回True
#isValidPosition()函数还有名为adjX和adjY的可选参数。通常，isValidPosition()函数检查作为第二个参数传递的砖块对象所提供的位置数据(此时adjX=0, adjY=0)。
#然而，有时候我们不想要检查砖块的当前位置，而是要检查该位置之上的一些空格
##如果给adjX递-1.那么它不会检查砖块的数据结构中的位置的有效性，而是检查砖块所处的位置的左边一个空格是否是有效的。
#给adjX传递1的话，将会检查砖块右边的一个空格。还有一个可选的adjY参数。传递-1给adjY,将会检查砖块当前所处位置的上面一个空格，
#而给adjY传递值3将会检查砖块所在位置下面的3个空格。
 for x in range(TEMPLATEWIDTH): #TEMPLATEWIDTH=5 TEMPLATEWIDTH=5
  for y in range(TEMPLATEHEIGHT):# 遍历砖块模板的所有方块
   isAboveBoard = y + piece['y'] + adjY < 0 #模板还没完全进入游戏板
   if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:#在5x5模板中不等于'.'的方块，即有效方块
    continue
   if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):#有效砖块不在游戏板上
    return False
   if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:#有效砖块和游戏板上的方块重叠
    return False
 return True

def isCompleteLine(board, y):#判断y行是否填满，填满返回True
 for x in range(BOARDWIDTH):#遍历该行的所有砖块
  if board[x][y] == BLANK:#如果存在空白，则没填满
   return False
 return True

def removeCompleteLines(board):#完成的行进行消除
 numLinesRemoved = 0
 y = BOARDHEIGHT - 1 # BOARDHEIGHT=20-1=19即从最低行开始
 while y >= 0:#注意当删除一行时y没有生变化，因为此时它的值已经更新为新的一行了
  if isCompleteLine(board, y):#如果该行填满
   pygame.mixer.Sound("1.mp3").play()
   pygame.mixer.Sound("1.mp3").set_volume(0.2)
   for pullDownY in range(y, 0, -1): #range(y, 0, -1)范围[y,1]
    for x in range(BOARDWIDTH):
     board[x][pullDownY] = board[x][pullDownY-1]#将删除的行之上的每一行的值都复制到下一行
   for x in range(BOARDWIDTH):#删除第一行
    board[x][0]=BLANK
   numLinesRemoved=numLinesRemoved+1

  else:
   y =y- 1 #移到下一行
 return numLinesRemoved

def convertToPixelCoords(boxx, boxy):#将游戏板上方块的坐标转化成像素坐标
 return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))
 #XMARGIN为游戏板左顶点的横坐标，TOPMARGIN为游戏板左顶点的纵坐标

def drawBoard(board):#绘制游戏板边界，绘制有效方块划线，
 pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
 #pygame.draw.rect(DISPLAYSURF对象,RED颜色,(x,y,width,height),线的宽度) rect:矩形 x,y表示左上角的坐标 width表示矩形的宽度 height表示高度
 #线的宽度为0(默认)表示全部填充，为1会画很细的线
 # xmargin边缘
 pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN,  TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT)) #填充游戏板的背景颜色
 for x in range(BOARDWIDTH):#遍历游戏板
  for y in range(BOARDHEIGHT):
   drawBox(x, y, board[x][y])#这个函数会自动找出有效方块并绘制

#绘制一个砖块的一个有效方块(每个砖块有多个有效方块)
def drawBox(boxx, boxy, color, pixelx=None, pixely=None):#绘制一个有效方块
 if color == BLANK: #如果这不是一个有效方块，这是5x5一个空白
  return
 if pixelx == None and pixely == None:
  pixelx, pixely = convertToPixelCoords(boxx, boxy)#将游戏板上方块的坐标转化成像素坐标
 pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
 #留出1像素的空白，这样才能在砖块中看到组成砖块
 #的有效方块，不然砖块看起来就只有一片颜色。

#绘制一个砖块
def drawPiece(piece, pixelx=None, pixely=None):#pixelx, pixely为5x5砖块数据结构左上角在游戏板上的的坐标
 shapeToDraw = PIECES[piece['shape']][piece['rotation']]#PIECES[piece['shape']][piece['rotation']]为一个图形的一种旋转方式
 if pixelx == None and pixely == None:
 #然而，'Next'砖块并不会绘制到游戏板上。在这种情况下，我们忽略砖块数据结构中包含的位置信息，而是让drawPiece()函数的调用者
#为pixelx何pixely参数传递实参，以指定应该将砖块确切地绘制到窗口上的什么位置。
  pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])#将砖块坐标转换为像素坐标。
 for x in range(TEMPLATEWIDTH): #遍历5x5砖块数据结构
  for y in range(TEMPLATEHEIGHT):
   if shapeToDraw[y][x] != BLANK:
    drawBox(None, None, piece['color'], pixelx+(x * BOXSIZE), pixely + (y * BOXSIZE))
    #有效方块左上角在游戏板中的坐标=有效方块左上角在方块板数据结构中的坐标+方块数据额结构左上角在游戏板中的坐标，这里这不过换成了像素格式


#界面绘制布局：下一个预览，分数，等级，游戏结束文本
def drawNextPiece(piece):
 nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
 nextRect = nextSurf.get_rect()
 nextRect.topleft = (WINDOWWIDTH - 150, 80)
 DISPLAYSURF.blit(nextSurf, nextRect)
 drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=80)

def drawStatus(score, level):
 scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
 scoreRect = scoreSurf.get_rect()
 scoreRect.topleft = (WINDOWWIDTH - 150, 20)
 DISPLAYSURF.blit(scoreSurf, scoreRect)
 levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
 levelRect = levelSurf.get_rect()
 levelRect.topleft = (WINDOWWIDTH - 150, 50)
 DISPLAYSURF.blit(levelSurf, levelRect)

def showTextScreen(text):
 titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
 titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
 DISPLAYSURF.blit(titleSurf, titleRect)
 pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
 pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
 DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
 while checkForKeyPress() == None:
  pygame.display.update()
  FPSCLOCK.tick()



if __name__ == '__main__':
 main()
