import tkinter, math

mul_m_m = lambda X,Y: [[sum(a*b for a,b in zip(x_row, y_col)) for y_col in zip(*Y)] for x_row in X]

def rotate(x, y, phi):
    rotation_mtx = \
    [[ math.cos(phi), math.sin(phi), 0],
     [-math.sin(phi), math.cos(phi), 0],
     [ 0            , 0            , 1]]
    v = [[x,y,1]]
    return mul_m_m(v, rotation_mtx)

class SimpleClass:
    def __init__(self, canvas, x, y, w, h, title):
        self.title = title
        self.canvas = canvas
        self.x  = x
        self.y = y
        self.width = w
        self.height = h
        self.arrows = []
        self.items_to_delete = []

    def add_arrow(self, arrow):
        self.arrows.append(arrow)

    def set_tag(self, tag):
        self.tag = tag
        
    def draw(self):
        shape = self.canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill = 'gray')
        self.items_to_delete.append(shape)
        
        canvas_id = canvas.create_text(self.x + self.width/2, self.y + self.height/2)
        canvas.itemconfig(canvas_id, text=self.title)
        self.items_to_delete.append(canvas_id)
        
        for arrow in self.arrows:
            arrow.redraw()
        
    def redraw(self):
        while len(self.items_to_delete) > 0:
            self.canvas.delete(self.items_to_delete[0])
            self.items_to_delete = self.items_to_delete[1:]
        
        self.draw()

    def is_inside(self, x,y):
        return self.x < x < self.x + self.width and self.y < y < self.height + self.y

class SimpleArrow:
    def __init__(self, canvas, _from, _to):
        self.set_from_to(_from, _to)
        self.tag = self.__hash__()

    def set_from_to(self, _from, _to):
        self.sx = _from.x + _from.width / 2
        self.sy = _from.y + _from.height
        self.fx = _to.x + _to.width / 2
        self.fy = _to.y
        self.canvas = canvas
        self._from = _from
        self._to = _to
        _from.add_arrow(self)
        _to.add_arrow(self)
        self.items_to_delete = []

    def draw(self):
        width = ((self.fx - self.sx) * (self.fx - self.sx) + (self.fy - self.sy) * (self.fy - self.sy)) ** 0.5
        fx0, fy0 = width, 0
        fx1, fy1 = width - 10, -10
        fx2, fy2 = width - 10, 10
        
        phi = math.atan2(-self.sy + self.fy, self.fx - self.sx)

        r0 = rotate(fx0, fy0, phi)[0]
        r1 = rotate(fx1, fy1, phi)[0]
        r2 = rotate(fx2, fy2, phi)[0]

        fx0, fy0 = self.sx + r0[0], self.sy + r0[1]
        fx1, fy1 = self.sx + r1[0], self.sy + r1[1]
        fx2, fy2 = self.sx + r2[0], self.sy + r2[1]
        self.items_to_delete.append(self.canvas.create_line(self.sx, self.sy, fx0, fy0, tags = self.tag))
        self.items_to_delete.append(self.canvas.create_line(fx0, fy0, fx1, fy1, tags = self.tag))
        self.items_to_delete.append(self.canvas.create_line(fx0, fy0, fx2, fy2, tags = self.tag))

    def redraw(self):
        while len(self.items_to_delete) > 0:
            self.canvas.delete(self.items_to_delete[0])
            self.items_to_delete = self.items_to_delete[1:]
        self.sx = self._from.x + self._from.width / 2
        self.sy = self._from.y + self._from.height
        self.fx = self._to.x + self._to.width / 2
        self.fy = self._to.y

        self.draw()

    def set_from(self, _from):
        self._from = _from

    def set_to(self, _to):
        self._to = _to
    

bx, by = 100, 100
fx, fy = 50, 10
dx, dy = 0, 10
prev_x, prev_y = None, None
canvas, classes = None, []    
current = None

def on_start_drag(event):
    global current
    global prev_x
    global prev_y
    print('start at: (%d. %d)'%(event.x, event.y))
    prev_x, prev_y = event.x, event.y
    c = [x for x in classes if x.is_inside(event.x, event.y)]
    if len(c) > 0:
         current = c[0]
    
def on_drag(event):
    global current
    global prev_x
    global prev_y
    #print('darg to: (%d, %d)'%(event.x, event.y))
    if current != None:
        current.x -= prev_x - event.x
        current.y -= prev_y - event.y
        prev_x, prev_y = event.x, event.y
        current.redraw()

def on_release(event):
    global current
    global prev_x
    global prev_y
    print('release at: (%d. %d)'%(event.x, event.y))
    current, prev_x, prev_y = None, None, None
    
        

main_window = tkinter.Tk()

canvas = tkinter.Canvas(main_window, width = 500, height = 500, bd=4)
canvas.pack()

simple_class1 = SimpleClass(canvas, 10, 10, 120, 25, 'from')
simple_class1.set_tag('1')
simple_class1.draw()

simple_class2 = SimpleClass(canvas, 150, 50, 170, 25, 'to')
simple_class2.set_tag('2')
simple_class2.draw()

simple_class3 = SimpleClass(canvas, 250, 50, 170, 25, 'to 2')
simple_class3.set_tag('3')
simple_class3.draw()

simple_arrow1 = SimpleArrow(canvas, simple_class1, simple_class2)
simple_arrow1.draw()

simple_arrow2 = SimpleArrow(canvas, simple_class1, simple_class3)
simple_arrow2.draw()

classes.append(simple_class1)
classes.append(simple_class2)
classes.append(simple_class3)

canvas.bind('<ButtonPress-1>', on_start_drag)
canvas.bind('<B1-Motion>', on_drag)
canvas.bind('<ButtonRelease-1>', on_release)

main_window.mainloop()
