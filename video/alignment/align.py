#!/usr/bin/env python3
#!/cygdrive/c/Python35-32/python -u

# align.py
# alignment tool -- aligns two images using translation, rigid motion,
# affine motion, or homography, depending on numbers of "anchors" placed
# also added rectified (x-only) motion

# NOTE: for newer PIL documentation, see http://effbot.org/imagingbook/
# as of this writing, it covers PIL 1.1.6, which includes PERSPECTIVE transformations
#
# documentation linked from http://www.pythonware.com/products/pil/ is older
# 
# Daniel Scharstein
# 7/24/2012 - first working version, up to affine transformations
# 7/25/2012 - includes homographies
# 7/7/2016 - ported to Python3, Pillow, removed scipy dependency

# TODO:
# doesn't work right if image is larger than window
# need to add saving of transformations (.txt) and warped images

import os, sys, glob, math
import tkinter as tk
from PIL import Image, ImageTk, ImageChops, ImageDraw
import numpy as np
# from scipy import linalg

if len(sys.argv) != 3:
    print("usage: %s im1 im2" % sys.argv[0])
    sys.exit()

instructions = """\
Drag: move relative      Shift/Tab: blink images         u: undo        r: reset
Right button: set/move/clear anchors       Esc,q: quit      """


class aligner:

    def __init__(self, imn1, imn2):
        self.root = tk.Tk()
        #self.root.configure(bg = "blue")
        ww = min(900, self.root.winfo_screenwidth() - 100)
        wh = min(700, self.root.winfo_screenheight() - 130)
        self.root.geometry("%dx%d+5+5" % (ww, wh))
        self.root.title("Aligntool")
        self.winsize = (self.root.winfo_width(), self.root.winfo_height())

        f1 = tk.Frame(self.root)
        self.lname1 = tk.Label(f1)
        self.lname2 = tk.Label(f1)
        self.lname1.pack(side = "left", anchor = "c", fill = "x", expand = 1)
        self.lname2.pack(side = "left", anchor = "c", fill = "x", expand = 1)
        f1.pack(side = "top", fill = "x", expand = 0)

        self.linfo = tk.Label(self.root, text = "info", bg = "white", anchor = "w")
        self.linfo.pack(side = "top", fill = "x", expand = 0)
        
        self.pimg1 = ImageTk.PhotoImage("RGB")
        self.limg = tk.Label(self.root, image = self.pimg1, cursor = "crosshair", bg="red", borderwidth=0)
        self.limg.pack(side = "top", fill = "none", expand = 1)
        #self.limg.place(x=0, y=0)
        
        linstr = tk.Label(self.root, text=instructions, justify="left", bg="white")
        linstr.pack(side = "top", anchor = "w", fill = "x", expand = 0)

        # initialize everything

        self.imname1 = imn1
        self.imname2 = imn2
        self.name1 = os.path.basename(self.imname1)
        self.name2 = os.path.basename(self.imname2)
        self.fullim1 = Image.open(self.imname1)
        self.fullim2 = Image.open(self.imname2)
        self.transf = eye3()
        self.oldtransf = eye3()
        self.tstack = [] # stack of old transforms for undo
        self.down = 0, 0
        self.move = 0, 0
        self.anchors = []
        self.diff = False
        self.xonly = False
        self.blinkoff()
        self.diffon()
        self.update()
        
        # key bindings
        self.root.bind("<Configure>", lambda e: self.winresize(e))
        #self.root.bind_all("<ButtonRelease-1>", lambda e: self.checkwinresize())
        self.root.bind("q", lambda e: self.quit())
        self.root.bind("Q", lambda e: self.quit())
        self.root.bind("<Escape>", lambda e: self.quit())
        self.root.bind("u", lambda e: self.undo())
        self.root.bind("c", lambda e: self.clearanchors())
        self.root.bind("r", lambda e: self.reset())
        self.root.bind("x",  lambda e: self.toggleXonly())
        self.root.bind("p",  lambda e: self.printtransf())
        self.root.bind("<Left>",  lambda e: self.transl(( 1,  0)))
        self.root.bind("<Right>", lambda e: self.transl((-1,  0)))
        self.root.bind("<Up>",    lambda e: self.transl(( 0,  1)))
        self.root.bind("<Down>",  lambda e: self.transl(( 0, -1)))
        #self.root.bind("z",  lambda e: self.changezoom(e, 1))
        #self.root.bind("x",  lambda e: self.changezoom(e, -1))
        #self.root.bind("c",  lambda e: self.center(e))
        self.root.bind("<KeyPress-Tab>", lambda e: self.blinkon())
        self.root.bind("<KeyRelease-Tab>", lambda e: self.blinkoff())
        self.root.bind("<KeyPress-Shift_L>", lambda e: self.diffoff())
        self.root.bind("<KeyRelease-Shift_L>", lambda e: self.diffon())
        #self.root.bind("s", lambda e: self.diffoff())
        #self.root.bind("<KeyRelease>",  lambda e: self.update())
        #self.root.bind("<KeyPress>",  lambda e: sys.stdout.write("key:'%s'\n" % e.keysym))
        #self.root.bind("<KeyRelease>",  lambda e: sys.stdout.write("key up:'%s'\n" % e.keysym))

        # mouse bindings for dragging
        self.limg.bind("<Button-1>", lambda e: self.buttondown(e))
        self.limg.bind("<B1-Motion>", lambda e: self.buttonmove(e))
        self.limg.bind("<ButtonRelease-1>", lambda e: self.buttonup(e))
        self.limg.bind("<Button-3>", lambda e: self.selectanchor(e))
        self.limg.bind("<B3-Motion>", lambda e: self.moveanchor(e))
        self.limg.bind("<ButtonRelease-3>", lambda e: self.removeanchor(e))
        self.limg.bind("<MouseWheel>", lambda e: self.mousewheel(e))
        # and for motion
        #self.limg.bind("<Motion>", lambda e: self.updatecursor(e))

        self.root.bind("s", lambda e: self.saveimgs())

        # go!
        self.root.mainloop()

    # end of __init__


    def quit(self):
        self.root.destroy()

    def saveimgs(self):
        #fn1 = "transf-" + self.imname1  # won't work if in subdir
        #fn2 = "transf-" + self.imname2 
        fn1 = "transf-im0.png"
        fn2 = "transf-im1.png"
        self.img1.save(fn1)
        self.img2.save(fn2)
        print("saved transformed images as:")
        print(fn1)
        print(fn2)

    def printtransf(self):
        print("[%.3f %.4f %.1f;  %.4f %.3f %.1f;  %.4f %.4f %.1f]" %
                tuple(self.transf.flatten().tolist()))
        t = self.transf
        for a in self.anchors:
            x0, y0 = a
            x1, y1 = transApply(t, a)
            print("point %d, %d in im0;  %d, %d in im1" % (x0, y0, x1, y1))
        
    def clearanchors(self):
        self.anchors = []
        self.update()
        
    def reset(self):
        self.transf = eye3()
        self.oldtransf = eye3()
        self.tstack = []
        self.down = 0, 0
        self.move = 0, 0
        self.anchors = []
        self.update()

    def toggleXonly(self):
        self.xonly = not self.xonly
        if self.xonly:
            self.tstack.append(self.transf)
            self.transf[1] = 0, 1, 0
            self.transf[2] = 0, 0, 1
        self.updatetransf()
        self.update()
        
    def winresize(self, e):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if (w, h) != self.winsize:
            self.winsize = (w, h)
            #self.maxcropsize = (w - 8, h - 107)
            #self.setcropsize()
            

    def blinkon(self):
        if self.diff:
            return
        self.lname1.configure(bg = "white")
        self.lname2.configure(bg = "#ffb")
        self.blink = True
        if self.pimg2 == None:
            self.update()
        self.limg.configure(image = self.pimg2)
        #self.showpos()

    def blinkoff(self):
        if self.diff:
            return
        self.lname1.configure(bg = "#ffb")
        self.lname2.configure(bg = "white")
        self.blink = False
        if self.pimg1 == None:
            self.update()
        self.limg.configure(image = self.pimg1)
        #self.showpos()

    def diffon(self):
        self.lname1.configure(bg = "white")
        self.lname2.configure(bg = "white")
        if self.diff:
            return          # important if Shift is used because of key repeat!!!!
        self.diff = True
        self.update()

    def diffoff(self):
        if not self.diff:
            return
        self.diff = False
        self.update()
        
    def buttondown(self, event):
        self.oldtransf = self.transf
        self.down = event.x, event.y

    def buttonmove(self, event):
        self.move = event.x, event.y
        self.updatetransf()
        self.update()

    def buttonup(self, event):
        self.tstack.append(self.oldtransf)
        self.oldtransf = self.transf

    def mousewheel(self, event):
        print("wheel", event.delta)
        # TODO: add zoom

    def undo(self):
        if self.tstack == []:
            self.transf = eye3()
        else:
            self.transf = self.tstack.pop()
        self.oldtransf = self.transf
        self.update()
        
        
    def selectanchor(self, event): # selects anchors at clicked location or adds new one
        pos = event.x, event.y
        self.anchorclick = -1000, -1000  # so new anchors won't get deleted
        # did we click on an existing anchor?
        for k, a in enumerate(self.anchors):
            if t2norm(t2sub(a, pos)) <= 7:  # if yes, remove it first
                del self.anchors[k]
                self.anchorclick = pos  # remember we clicked on existing anchor
                break
        if len(self.anchors) == 4: # max number of anchors? (at most 3 are used for transf)
            del self.anchors[0]    # if yes, remove oldest
        # add selected or new anchor to end of list
        self.anchors.append(pos)
        self.update()

    def moveanchor(self, event): # moves anchor last selected
        pos = event.x, event.y
        self.anchors[-1] = pos
        self.update()

    def removeanchor(self, event): # removes anchor if just clicked, not moved
        pos = event.x, event.y
        if t2norm(t2sub(self.anchorclick, pos)) <= 2:
            self.anchors.pop() # remove last
            self.update()


    def transl(self, t):
        tx, ty = t
        transf = mat3(1, 0, 0.25*tx,  0, 1, 0.25*ty)
        self.applytransf(transf, "transl")
        self.oldtransf = self.transf
        self.update()


    # update transf
    def updatetransf(self):
        x0, y0 = self.move
        x1, y1 = self.down
        if self.xonly:
            if len(self.anchors) == 0:
                txt = "x-translation"
                transf = mat3(1, 0, x1-x0,  0, 1, 0)
            elif len(self.anchors) == 1:
                txt = "x-scale"
                px, py = self.anchors[0]
                sx = (px - x1) / avoidzero(px - x0)
                tx = px * (1.0 - sx)
                transf = mat3(sx, 0, tx,  0, 1, 0)
            else: # len(self.anchors) == 2
                txt = "x-affine motion"
                px, py = self.anchors[0]
                qx, qy = self.anchors[1]
                m = mat3(px, py, 1,  qx, qy, 1,  x0, y0, 1)
                bx = vec3(px, qx, x1)
                a, b, c = np.linalg.solve(m, bx)
                transf = mat3(a, b, c,  0, 1, 0)
        else: # not restricted in x
            if len(self.anchors) == 0:
                txt = "translation"
                transf = mat3(1, 0, x1-x0,  0, 1, y1-y0)
            elif len(self.anchors) == 1:
                txt = "similarity"
                px, py = self.anchors[0]
                dx, dy = px - x0, py - y0
                ex, ey = px - x1, py - y1
                a = (dx*ex + dy*ey) / avoidzero(dx*dx + dy*dy)
                b = (a*dx - ex) / avoidzero(dy)
                tx = (1 - a) * px + b * py
                ty = (1 - a) * py - b * px
                transf = mat3(a, -b, tx,  b, a, ty)
            elif len(self.anchors) == 1.1: # not used....
                txt = "scale x, y"
                px, py = self.anchors[0]
                sx = (px - x1) / avoidzero(px - x0)
                sy = (py - y1) / avoidzero(py - y0)
                tx = px * (1.0 - sx)
                ty = py * (1.0 - sy)
                transf = mat3(sx, 0, tx,  0, sy, ty)
            elif len(self.anchors) == 2:
                txt = "affine motion"
                px, py = self.anchors[0]
                qx, qy = self.anchors[1]
                m = mat3(px, py, 1,  qx, qy, 1,  x0, y0, 1)
                bx = vec3(px, qx, x1)
                by = vec3(py, qy, y1)
                a, b, c = np.linalg.solve(m, bx)
                d, e, f = np.linalg.solve(m, by)
                transf = mat3(a, b, c,  d, e, f)
            else:
                txt = "homography"
                px, py = self.anchors[0]
                qx, qy = self.anchors[1]
                rx, ry = self.anchors[2]
                m = np.vstack([hmat(px, py, px, py),
                               hmat(qx, qy, qx, qy),
                               hmat(rx, ry, rx, ry),
                               hmat(x0, y0, x1, y1)])
                v = np.array([px, py, qx, qy, rx, ry, x1, y1])
                a, b, c,  d, e, f,  g, h = np.linalg.solve(m, v)
                transf = mat3(a, b, c,  d, e, f,  g, h, 1)
        self.applytransf(transf, txt)

    def applytransf(self, transf, txt):
        self.transf = np.dot(self.oldtransf, transf)
        txt += ("[%5.3f %5.4f %5.1f ;  %5.3f %5.4f %5.1f ;  %.4e %.4e %5.1f]" %
                tuple(self.transf.flatten().tolist()))
        self.linfo.configure(text = txt)
        if False: # print debug info
            print("%.2f %.2f" % t2sub(transApply(transf, (x0, y0)), (x1, y1)))
            for x in self.anchors:
                print("%.2f %.2f" % t2sub(transApply(transf, x), x))

    # update images
    def update(self):
        self.img1 = self.fullim1
        self.pimg1 = None

        imsize = self.fullim2.size
        filter = Image.BILINEAR
        #self.img2 = self.fullim2.transform(imsize, Image.AFFINE, self.transf, filter)
        #q = affToQuad(imsize, self.transf)
        #q = transToQuad(imsize, self.transf)
        #self.img2 = self.fullim2.transform(imsize, Image.QUAD, q, filter)
        tr = tuple(self.transf.flatten().tolist()[:-1])
        self.img2 = self.fullim2.transform(imsize, Image.PERSPECTIVE, tr, filter)
        self.pimg2 = None

        if self.diff: # residual
            residscale = 3
            resid = ImageChops.subtract(self.img1, self.img2, 1.0/residscale, 128)
            draw = ImageDraw.Draw(resid)
            for p in self.anchors:
                drawCross(draw, p)

            #if z > 1:
            #    resid = resid.resize(cz)
            self.presid = ImageTk.PhotoImage(resid)
            self.limg.configure(image = self.presid)
        else:
            if self.blink:
                im2 = self.img2 # if z == 1 else self.img2.resize(cz)
                self.pimg2 = ImageTk.PhotoImage(im2)
                self.limg.configure(image = self.pimg2)
            else:
                im1 = self.img1 # if z == 1 else self.img1.resize(cz)
                self.pimg1 = ImageTk.PhotoImage(im1)
                self.limg.configure(image = self.pimg1)
        #update labels:
        t1 = self.name1 #+ "  %+d%+d " % cp1
        t2 = self.name2 #+ "  %+d%+d " % cp2
        self.lname1.configure(text = t1)
        self.lname2.configure(text = t2)
        #self.showpos()


# utility functions

def avoidzero(x):
    if x == 0:
        return 1e-6
    return float(x)

# t2 - operations on tuples of 2 ints
def t2add(a, b):
    a1, a2 = a
    b1, b2 = b
    return (a1+b1, a2+b2)

def t2sub(a, b):
    a1, a2 = a
    b1, b2 = b
    return (a1-b1, a2-b2)

def t2mul(a, s):
    a1, a2 = a
    return (int(s*a1), int(s*a2))

def t2div(a, s):
    a1, a2 = a
    return (int(a1/s), int(a2/s))

def t2norm(a):
    x, y = a
    return math.sqrt(x*x + y*y)

def drawCross(draw, loc):
    x, y = loc
    d = 8
    draw.line((x-d, y, x+d, y), "yellow", width=2)
    draw.line((x-d, y+1, x+d, y+1), "yellow", width=2) # bug in imagedraw
    draw.line((x, y-d, x, y+d), "yellow", width=2)
    draw.line((x-d, y, x+d, y), "black")
    draw.line((x, y-d, x, y+d), "black")

# operations for 3x3 homogeneous transforms

def eye3():
    return np.eye(3)

def vec3(a, b, c=1):
    return np.array([a, b, c])

def mat3(a, b, c,  d, e, f,  g=0, h=0, i=1):
    return np.array([[a, b, c],
                     [d, e, f],
                     [g, h, i]])

def transApply(t, p): # apply 3x3 transform to point p
    px, py = p
    v = vec3(px, py, 1)
    x, y, z = np.dot(t, v)
    return x/z, y/z
    
def transToQuad(imsize, t): # turn 3x3 transform into PIL's quad transform
    w, h = imsize
    w -= 0
    h -= 0
    x0, y0 = transApply(t, (0, 0))
    x1, y1 = transApply(t, (0, h))
    x2, y2 = transApply(t, (w, h))
    x3, y3 = transApply(t, (w, 0))
    print(x0, y0, x1, y1, x2, y2, x3, y3)
    return x0, y0, x1, y1, x2, y2, x3, y3

def hmat(x0, y0, x1, y1):
    return np.array([[x0, y0, 1,  0,  0, 0, -x0*x1, -y0*x1],
                     [0,  0,  0, x0, y0, 1, -x0*y1, -y0*y1]])
    
# run the whole thing
aligner(sys.argv[1], sys.argv[2])
