# -*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import copy
import time

#========================================================================================
#========================================================================================
# ドラッグアンドドロップ実行用の為の関数
class PoQListWidget(QtGui.QListWidget):
    def __init__( self, parent ):
        super( PoQListWidget, self ).__init__(  )
        self.setParent(parent)
    
    #---------------------------------------------------------------------
    # mimeをドロップ先に渡す為の設定を行う関数。
    def startDrag(self, dropAction):
        # create mime data object
        print 'startDrag'
        mime = QtCore.QMimeData()
        #mime.setUrls(['test','popo'])
        #mime.setData('application/x-item', '???')
        mime.setText(self.selectedItems()[0].metaData)
        mime.tempData =self.selectedItems()[0].icon().pixmap(100, 100)
        #mime.setPixmap()
        # start drag
        drag = QtGui.QDrag(self)
        drag.setMimeData(mime)
        drag.start(QtCore.Qt.CopyAction | QtCore.Qt.CopyAction)


#========================================================================================
#========================================================================================
# ItemMangerで実行する関数
class ExObject():
    def __init__(self):
        pass
    def execute(self):
        print 'execute'


#========================================================================================
#========================================================================================
# スクリーショット用クラス
class ScreenShot( QtGui.QGraphicsView ):
    def __init__( self, arg ):
        super( ScreenShot, self ).__init__( )
        self.qlabel=QtGui.QLabel(self)
        self.Qbutton = QtGui.QPushButton('test', parent=self)
        self.Qbutton.clicked.connect(self.shot)
        self.widget=arg
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setGeometry(5, 25, 1024, 680)
        self.setBackgroundColor()
        
        self.QGscene = QtGui.QGraphicsScene()
        self.painter = QtGui.QPainter(self)
        self.QGscene.drawForeground(self.painter, QtCore.QRectF())
        self._startPos = None
        self._currentPos = None
    
    #-----------------------------------------------------------------
    # QPainterの設定
    def settingPainter(self):
        self.pen = QtGui.QPen()
        ##self.pen.setStyle(QtCore.Qt.DashDotLine)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)
        self.pen.setWidth(3)
        self.pen.setBrush(QtCore.Qt.red)
        self.pen.setCapStyle(QtCore.Qt.RoundCap)
        self.pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self.painter.setPen(self.pen)
    
    #-----------------------------------------------------------------
    # スクリーンショット用枠の表示
    def paintEvent(self, event):
        self.painter.begin(self)
        self.settingPainter()
        
        if (self._startPos !=None) and (self._currentPos !=None):
            self.painter.drawLine(self._startPos.x(), self._startPos.y(), self._currentPos.x(), self._startPos.y())
            self.painter.drawLine(self._currentPos.x(), self._startPos.y(), self._currentPos.x(), self._currentPos.y())
            self.painter.drawLine(self._startPos.x(), self._startPos.y(), self._startPos.x(), self._currentPos.y())
            self.painter.drawLine(self._startPos.x(), self._currentPos.y(), self._currentPos.x(), self._currentPos.y())
        
        self.painter.end()
    
    #-----------------------------------------------------------------
    # スクリーンショット保存
    def shot(self):
        print 'shot'
        stPos = self._startPos
        enPos = self._currentPos
        st_x, st_y = stPos.x(), stPos.y()
        en_x, en_y = enPos.x(), enPos.y()
        print st_x, st_y, en_x, en_y
        # 上下逆の場合の入れ替え ※入れ替えの仕様違いに注意
        if st_x > en_x:
            st_x, en_x=en_x, st_x
        if st_y > en_y:
            st_y, en_y=en_y, st_y
        
        penPixel = 4
        
        shotRec = (st_x+penPixel, st_y+penPixel, en_x-st_x-penPixel*2, en_y-st_y-penPixel*2)
        #shotRec = (0, 0, QtGui.QApplication.desktop().screenGeometry().width(),
        #           QtGui.QApplication.desktop().screenGeometry().height())
        #p = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId(), *shotRec)
        self.hide()
        p = QtGui.QPixmap.grabWindow(self.winId(), *shotRec)
        p.save('~/screenshot.jpg', 'jpg')
        self.qlabel.setPixmap(p)
        time.sleep(0.1)
        self.show()
    
    #-----------------------------------------------------------------
    # スクリーンショット用外枠表示開始点設定
    def mousePressEvent(self, event):
        self._startPos = event.pos()
        self.QGscene.addText("Hello, world!");
    
    #-----------------------------------------------------------------
    # スクリーンショット用外枠表示
    def mouseMoveEvent(self, event):
        position = event.pos()
        self._currentPos = position
        self.update()
    
    #-----------------------------------------------------------------
    # マウスボタンを離した際にスクリーンショット実行
    def mouseReleaseEvent(self, event):
        position = event.pos()
        self._currentPos = position
        self.update()
        #self.shot()
    
        '''
        self.QGscene.addLine(self._startPos.x(), self._startPos.y(), position.x(), position.y(), QtCore.Qt.red)
        start = QtCore.QPointF(self.mapToScene(self._startPos))
        end = QtCore.QPointF(self.mapToScene(event.pos()))
        self.QGscene.addItem(QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))
        for point in (start, end):
            text = self.QGscene.addSimpleText('(%d, %d)' % (point.x(), point.y()))
            text.setBrush(QtCore.Qt.red)
            text.setPos(point)
        '''
    #-----------------------------------------------------------------
    # 背景色を設定。
    def setBackgroundColor(self, arg=None, color=(30, 30, 40, 100)):
        if arg is None:
            arg = self
        p = arg.palette()
        p.setColor(arg.backgroundRole(), QtGui.QColor(*color))
        arg.setPalette(p)

#========================================================================================
#========================================================================================
# pixmapと関連付けし関数を実行する為のマネージャー
class ItemManager():
    def __init__( self ):
        self.itemDic = {}
    
    def setItem( self, keyitem ):
        self.itemDic.update({keyitem:ExObject() })
    
    def getItem( self, keyitem ):
        print keyitem, self.itemDic[str(keyitem)]
        return self.itemDic[str(keyitem)]


#========================================================================================
#========================================================================================
# itemをワークスペースに設定する為の観覧用QListWidget
class ItemViewer( QtGui.QWidget ):
    def __init__( self ):
        super( ItemViewer, self ).__init__( )
        self.listwidget = PoQListWidget(self)#QtGui.QListWidget(self)
        self.listwidget.setGeometry(30, 40, 500, 300)
        self.listwidget.setViewMode( self.listwidget.IconMode )
        self.listwidget.setGridSize( QtCore.QSize(50,50) )
    
    #-----------------------------------------------------------------
    # テスト用アイテム設定関数
    def setTestItems( self ):
        imagepath = '/Library/Application Support/Apple/iChat Icons/Flags/'
        import glob
        self.pixmapItems =[]
        for num, i in enumerate(glob.glob(imagepath+'/*')):
            tempPixmap = QtGui.QPixmap(i)
            tempIcon = QtGui.QIcon(tempPixmap)
            tempItem = QtGui.QListWidgetItem()
            tempItem.setIcon(tempIcon)
            tempItem.metaData = i
            tempPixmap.metaData = i
            self.setItem_inManager(i)
            self.listwidget.addItem(tempItem)
                
                
    #-----------------------------------------------------------------
    # metaData iconFilaPathからlistWidgetItemを追加
    def addItem(self, metaData, filePath):
        imagepath = '/Library/Application Support/Apple/iChat Icons/Flags/'
        import glob
        self.pixmapItems =[]
        for num, i in enumerate(glob.glob(imagepath+'/*')):
            tempPixmap = QtGui.QPixmap(i)
            tempIcon = QtGui.QIcon(tempPixmap)
            tempItem = QtGui.QListWidgetItem()
            tempItem.setIcon(tempIcon)
            tempItem.metaData = i
            tempPixmap.metaData = i
            self.setItem_inManager(i)
            self.listwidget.addItem(tempItem)



    #-----------------------------------------------------------------
    # 設定したitemManagerからitemを取得。キーにはpixmapを使用。
    def getItem_fromManager( self, arg ):
        self.iManager.getItem(arg)

    #-----------------------------------------------------------------
    # itemをpixmapから使用/設定する為のitemManagerを設定。
    def setItemManager( self, arg ):
        self.iManager = arg
    
    #-----------------------------------------------------------------
    # 設定したitemManagerから取得。キーにはpixmapを使用。
    def setItem_inManager( self, pixmap ):
        self.iManager.setItem(pixmap)

    #-----------------------------------------------------------------
    # 背景色を設定。
    def setBackgroundColor(self, arg=None):
        if arg is None:
            arg = self
        p = arg.palette()
        p.setColor(arg.backgroundRole(), QtGui.QColor(30, 30, 40))
        arg.setPalette(p)


#========================================================================================
#========================================================================================
#setGridSize /.setSizeHint( QSize( value, value ) )
#QListView
# ワーキスペース用のイメージビュワー
class ImageViewer( QtGui.QGraphicsView ):
    def __init__( self ):
        super( ImageViewer, self ).__init__( )
        
        self.setCacheMode( QtGui.QGraphicsView.CacheBackground )
        self.setRenderHints( QtGui.QPainter.Antialiasing |
                            QtGui.QPainter.SmoothPixmapTransform |
                            QtGui.QPainter.TextAntialiasing
                            )


        imagepath = '/Library/Application Support/Apple/iChat Icons/Flags/'
        self.QGscene = QtGui.QGraphicsScene()
        self.sceneSize = 10
        self.pixmapItems =[]
        self.setBackgroundColor()
        #Qpainted = QtGui.QPainter()
        #Qpainted.fillRect(0, 0, 1000, 100, QtGui.QColor(30, 30, 40))
        #self.QGscene.drawBackground(Qpainted, QtCore.QRectF(1, 1, 100, 200))
        
        
        import glob
        ''' for test
        for num, i in enumerate(glob.glob(imagepath+'/*')):
            tempPixmap = QtGui.QPixmap(i)
            tempPixmap = self.QGscene.addPixmap(tempPixmap)
            #tempPixmap.setPos(tempPixmap.getPosition()[0]*self.sceneSize, 1)
            tempPixmap.oPosition = [num*10, 0]
            tempPixmap.setFlags(QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsSelectable )
            self.pixmapItems.append(tempPixmap)
            print self.QGscene
        '''
        
        self.setAcceptDrops(True)
        
        self.setScene(self.QGscene)
        #self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self._scale = 1.0
        #self.setInteractive(True)
        #self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        #self.setViewportUpdateMode(QtGui.QGraphicsView.MinimalViewportUpdate)
    
    
    #---------------------------------------------------------------------
    # ダブルクリック時に選択中のアイテムからitemManagerを用いて関数を実行、または取得。
    def mouseDoubleClickEvent( self, event ):
        pos = self.mapToScene(event.pos())
        for i in self.pixmapItems:
            if i.isSelected():
                print i.metaData
                self.getItem_fromManager(i.metaData)
                print i.pos()

    #---------------------------------------------------------------------
    # dropイベント用ダミー。
    def dragEnterEvent( self, event ):
        print 'enter'
        event.accept()
    
    #---------------------------------------------------------------------
    # QGraphicシーンにpixmapをイメージファイルパスを用いて追加。
    def addItems( self, imagefile=None, position=[0,0] ):
        tempPixmap = QtGui.QPixmap(imagefile)
        tempPixmap = self.QGscene.addPixmap(tempPixmap)
        tempPixmap.oPosition = position
        tempPixmap.setFlags(QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsSelectable )
        self.pixmapItems.append(tempPixmap)
    
    #---------------------------------------------------------------------
    # QGraphicシーンにpixmapを追加。
    def addPixmap( self, pixmap=None, position=[0,0], metaData=None ):
        print self.QGscene
        tempPixmap = self.QGscene.addPixmap(pixmap)
        tempPixmap.oPosition = position
        tempPixmap.setFlags(QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsSelectable )
        tempPixmap.metaData =metaData
        tempPixmap.setPos(*position)
        self.pixmapItems.append(tempPixmap)
    
    #---------------------------------------------------------------------
    # ドロップイベント設定。受け取ったmimeからドロップ時のマウス位置にmimeに設定されたpixmapを追加。
    def dropEvent( self, event ):
        pos = self.mapToScene(event.pos())
        print pos
        pos = (float(pos.x()), float(pos.y()))
        print pos
        print 'drop'
        mimedata= event.mimeData()
        print mimedata.text()
        print event.mimeData().data("application/x-item")
        #print mindata.formats().takeAt(1)
        print event.mimeData().urls()
        print mimedata.tempData
        self.addPixmap(mimedata.tempData, pos, mimedata.text())
    
    #-----------------------------------------------------------------
    # ドロップイベントcallbackの為のダミー。
    def dragMoveEvent( self, event ):
        print 'drag'
    
    #-----------------------------------------------------------------
    # マウスホイールが縦に使用された場合のシーンのスケール処理。
    def wheelEvent( self, event ):
        scaleFactor =0.001
        if event.orientation()==2:
            currentScale = self._scale +(event.delta()*scaleFactor)
            #self._scale = currentScale
            self.scale( currentScale, currentScale )

    #-----------------------------------------------------------------
    # 設定したitemManagerからitemを取得。キーにはpixmapを使用。
    def getItem_fromManager( self, arg ):
        self.iManager.getItem(arg)
    
    #-----------------------------------------------------------------
    # itemをpixmapから使用する為のitemManagerを設定。
    def setItemManager( self, arg ):
        self.iManager = arg
    
    #-----------------------------------------------------------------
    # 背景色を設定。
    def setBackgroundColor(self, arg=None):
        if arg is None:
            arg = self
        p = arg.palette()
        p.setColor(arg.backgroundRole(), QtGui.QColor(40, 40, 50))
        arg.setPalette(p)

#========================================================================================
#========================================================================================

# ---------------------------------------------------------------------
# テスト実行部
if __name__ == '__main__':
    app = QtGui.QApplication( sys.argv )
    
    __itemManager=ItemManager()
    viewer = ImageViewer()
    viewer.show()
    viewer.setItemManager(__itemManager)
    hogettest = ItemViewer()
    hogettest.show()
    hogettest.setItemManager(__itemManager)
    hogettest.setTestItems()
    
    testHoge=ScreenShot(viewer)
    testHoge.show()
    
    sys.exit( app.exec_() )