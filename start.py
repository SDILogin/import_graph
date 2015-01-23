import tkinter, math, parser, random
import tkinter.filedialog

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
        self.random_color = '#%02x%02x%02x' % (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        #self.tag = self.__hash__()

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

        self.items_to_delete.append(self.canvas.create_line(self.sx, self.sy, fx0, fy0, width = 2, fill=self.random_color))
        self.items_to_delete.append(self.canvas.create_line(fx0, fy0, fx1, fy1, width = 2, fill=self.random_color))
        self.items_to_delete.append(self.canvas.create_line(fx0, fy0, fx2, fy2, width = 2, fill=self.random_color))

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
canvas, classes = None, {}    
current = None

def eventxy_to_canvasxy(canvas, x,y):
    retx = canvas.canvasx(x)
    rety = canvas.canvasy(y)
    return (retx, rety)

def on_start_drag(event):
    global current
    global prev_x
    global prev_y
    canvasxy = eventxy_to_canvasxy(event.widget, event.x, event.y)
    print('start at: (%d. %d)'%canvasxy)
    prev_x, prev_y = canvasxy[0], canvasxy[1]
    c = [classes[x] for x in classes if classes[x].is_inside(canvasxy[0], canvasxy[1])]
    if len(c) > 0:
         current = c[0]
    
def on_drag(event):
    global current
    global prev_x
    global prev_y
    #print('darg to: (%d, %d)'%(event.x, event.y))
    canvasxy = eventxy_to_canvasxy(event.widget, event.x, event.y)
    if current != None:
        current.x -= prev_x - canvasxy[0]
        current.y -= prev_y - canvasxy[1]
        prev_x, prev_y = canvasxy[0], canvasxy[1]
        current.redraw()

def on_release(event):
    global current
    global prev_x
    global prev_y
    canvasxy = eventxy_to_canvasxy(event.widget, event.x, event.y)
    print('release at: (%d. %d)'%canvasxy)
    current, prev_x, prev_y = None, None, None

selected_project = '.'

def open_project():
    global selected_project
    selected_project = tkinter.filedialog.askdirectory(initialdir=selected_project)    

    main_window.wm_title(selected_project)

    #dp = parser.DirParser('/Users/SDI/Desktop/IOSProjects/vazhno-ios/Vazhno')
    dp = parser.DirParser(selected_project)
    dp.construct_graph()

    canvas.delete(tkinter.ALL)

    width, height = 200, 35
    offset_x, offset_y = 10, 10
    for node in dp.get_nodes():
        width = len(node.value) * 10
        # if offset_x + width > scrollregion_width:
        #     offset_x = 10
        #     offset_y += height * 1.1
        #     classes[node.value] = SimpleClass(canvas, offset_x, offset_y, width, height, node.value)
        # else:
        #     classes[node.value] = SimpleClass(canvas, offset_x, offset_y, width, height, node.value)

        # offset_x += width + 10
        # offset_y %= scrollregion_height
        classes[node.value] = SimpleClass(canvas, random.randint(0, scrollregion_width - width), random.randint(0, scrollregion_height - height), width, height, node.value)
        classes[node.value].draw()

    for edge in dp.get_edges():
        #import pdb 
        #pdb.set_trace()
        _from = edge[1]
        _to = edge[0]
        arrow = SimpleArrow(canvas, classes[_from.value], classes[_to.value])
        arrow.draw()


def quit():
    import sys
    sys.exit()   

main_window = tkinter.Tk()

menubar = tkinter.Menu(main_window)

filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label='Open project', command = lambda: open_project())
filemenu.add_command(label='Quit', command = lambda: quit())
menubar.add_cascade(label='File', menu=filemenu)

main_window.config(menu=menubar)

canvas_width, canvas_height = 1700, 768

frame = tkinter.Frame(main_window, width = canvas_width, height = canvas_height)
frame.pack()

scrollregion_width, scrollregion_height = 2500, 2500

canvas = tkinter.Canvas(frame, width = canvas_width, height = canvas_height, scrollregion=(0, 0, scrollregion_width, scrollregion_height), bd=4)

hbar = tkinter.Scrollbar(frame, orient=tkinter.HORIZONTAL)
hbar.pack(side=tkinter.BOTTOM,fill=tkinter.X)
hbar.config(command=canvas.xview)

vbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
vbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)
vbar.config(command=canvas.yview)

canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=tkinter.LEFT,expand=True,fill=tkinter.BOTH)

canvas.bind('<ButtonPress-1>', on_start_drag)
canvas.bind('<B1-Motion>', on_drag)
canvas.bind('<ButtonRelease-1>', on_release)

main_window.mainloop()
