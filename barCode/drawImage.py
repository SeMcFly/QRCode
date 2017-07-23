from PIL import Image , ImageDraw

class DrawImage:


     def __init__(self,width,boder,box_size,color):
          self.size = (width + boder * 2) * box_size
          self.boder = boder
          self.box_size = box_size
          mode = 'RGB'
          self.img = Image.new(mode,(self.size,self.size),color)
          self.drw = ImageDraw.Draw(self.img)

     def save(self,name):
          self.img.save(name)

     def show(self):
          self.img.show()
          
     def drawRect(self,row,col):
          pos = self.getPos(row,col)
          self.drw.rectangle(pos,fill = "black" )

     def getPos(self,row,col):
          r = (row + self.boder) * self.box_size
          c = (col + self.boder) * self.box_size
          return [(r,c),(r + self.box_size -1,c + self.box_size -1)]

     def replaceImage(self,imgName):
          icon = Image.open(imgName)
          fact = 4
          size_w = size_h = int(self.size/4)
          icon_w,icon_h = icon.size

          if icon_w > size_w:
               icon_w = size_w
          if icon_h > size_h:
               icon_h = size_h
          icon = icon.resize((icon_w,icon_h),Image.ANTIALIAS)
          w = int((self.size - icon_w)/2)
          h = int((self.size - icon_h)/2)
          self.img.paste(icon,(w,h),icon)

if __name__ == '__main__':
     img = DrawImage(21,4,10,'white')
     img.drawRect(20,0)
     img.drawRect(20,20)
     img.drawRect(0,20)
     img.replaceImage('gril.png')
     img.show()
     
