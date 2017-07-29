from drawImage import DrawImage
import ecl
from qrcode import  util

class BarCode:
     def __init__(self,version=2,ecl = ecl.ERROR_CORRECTION_L,mask = 0,box_size=10,boder=4):
          self.version = version
          self.modleLen = self.getModleLen(version)
          self.modle = self._initData()
          self.listData = []
          self.dataEncode = None
          self.ec = ecl
          self.maskPattern = mask
          self.qr = DrawImage(self.modleLen,boder,box_size,"white")

     def _initData(self):
          modle = [[None for x in range(self.modleLen)] for y in range(self.modleLen)]
          return modle

     def addData(self,data):
          self.listData.append(util.QRData(data))
          self.dataEncode = util.create_data(self.version,1,self.listData)

     def makeImage(self):
          self.setupFindPattren(0,0)
          self.setupFindPattren(0,self.modleLen-7)
          self.setupFindPattren(self.modleLen-7,0)
          self.setupAlignPattern()
          self.setupTimingPattern()
          self.setupFormtInfo(self.ec,self.maskPattern)# EC-L Mask - 0
          self.setupVersionInfo(self.version)
          self.dataMap(self.dataEncode,self.maskPattern)

          for r in range(self.modleLen):
               for c in range(self.modleLen):
                    if self.modle[r][c]:
                         self.qr.drawRect(c,r)
          return self.qr

     def setupFindPattren(self,row,col):
          for r in range(-1,8):
               if r + row <= -1 or r + row >= self.modleLen:
                    continue

               for c in range(-1,8):
                    if c + col <= -1 or c + col >= self.modleLen:
                         continue

                    if (r <= 6 and r >= 0 and (c == 0 or c == 6)
                         or (c >= 0 and  c <= 6 and (r == 0 or r == 6))
                         or (2 <= r and r <= 4 and 2 <= c and c <= 4)):
                         self.modle[r + row][c + col] = True
                    else:
                         self.modle[r + row][c + col] = False

     def setupAlignPattern(self):
          pos = ecl.getPosAlin(self.version)

          for i in range(len(pos)):
               for j  in range(len(pos)):
                    row = pos[i]
                    col = pos[j]

                    if self.modle[row][col] is not None:
                        continue
                    for r in range(-2,3):
                         for c in range(-2,3):
                              if (r == -2 or c == -2 or r == 2 or c == 2
                                  or (c == 0 and r == 0)):
                                   self.modle[row + r][col + c] = True
                              else:
                                   self.modle[row + r][col + c] = False

     def setupTimingPattern(self):

          for r in range(8,self.modleLen - 8):

               self.modle[r][6] = ((r % 2) == 0)
          for c in range(8,self.modleLen - 8):

               self.modle[6][c] = ((c % 2) == 0)

     def dataMap(self,data,maskPattern):
          maskPatternFunc = ecl.getMaskPattenFunc(maskPattern)
          byteIndex = 0
          bitIndex = 7
          dataLen = len(data)
          row = self.modleLen -1
          inc = -1

          for c in range(self.modleLen - 1,0,-2):
               if c <= 6:
                    c -= 1
               colRange = [c,c -1]

               while True:
                    for col in colRange:

                         if self.modle[row][col] is None:
                              color = False
                              if byteIndex < dataLen:
                                   color = (((data[byteIndex] >> bitIndex) & 1) == 1)
                              if maskPatternFunc(row,col):
                                   color = not color
                              self.modle[row][col] = color
                              bitIndex -= 1

                              if bitIndex == -1:
                                   bitIndex = 7
                                   byteIndex += 1
                    row += inc

                    if row < 0 or row >= self.modleLen:
                         row -= inc
                         inc = -inc
                         break

     def setupFormtInfo(self,ec,mask):
          #get BCH for (version << 3) | mask
          bits = ecl.getFormtInfo(ec,mask)
          for i in range(15):
               mod = (((bits >> i)&1)==1)
               if i < 6:
                    self.modle[i][8] = mod
               elif i < 8:
                    self.modle[i+1][8] = mod
               else:
                    self.modle[self.modleLen - 15 + i][8] = mod
          for i in range(15):
               mod = (((bits >> i)&1)==1)
               if i < 8:
                    self.modle[8][self.modleLen - 1 -i] = mod
               elif i < 9:
                    self.modle[8][15 - i] = mod
               else:
                    self.modle[8][15 - i - 1] = mod
          self.modle[self.modleLen - 8][8] = True

     def setupVersionInfo(self,version):

          if version < 7:
               return None

          bits = ecl.getVersionInfo(version)
          for i in range(18):
               mod = (((bits >> i) & 1) == 1)
               self.modle[i / 3][i%3 + self.modleLen - 8 - 3] = mod
               self.modle[i%3 + self.modleLen - 8 - 3][i / 3] = mod


     def getModleLen(self,version):
          return (version * 4 + 17)

def createQRCode(ec,boxsize,boder,v=2,data=None,save=None,reImgae=None):
     bc = BarCode(version=v,ecl = ec,boder=boder,box_size=boxsize)
     if data:
          bc.addData(data)
     img = bc.makeImage()
     if reImgae:
          img.replaceImage(reImgae)
     if not save:
          img.save('qrcode.png')
     else:
          img.save(save)

if __name__ == '__main__':
     bc = BarCode(version=5,boder=4,mask=4)
     bc.addData('XianRong,Happy Birthday')
     img = bc.makeImage()
     img.replaceImage('gril.png')
     img.show()
     #createQRCode(1,10,4,data='http://baidu.com',reImgae='gril.png')
     #img.save()


          
