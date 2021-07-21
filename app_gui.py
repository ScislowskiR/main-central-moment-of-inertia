import random
import tkinter as tk
from tkinter.messagebox import askyesno
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from app_cli import *


class EntryWithPlaceholder( tk.Entry ):
    def __init__(self, master, placeholder="PLACEHOLDER", color='grey', variabletext=None):
        super().__init__( master, textvariable=variabletext )
        self.variabletext = variabletext
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        self.bind( "<FocusIn>", self.foc_in )
        self.bind( "<FocusOut>", self.foc_out )
        self.put_placeholder()

    def put_placeholder(self):
        self.insert( 0, self.placeholder )
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete( '0', 'end' )
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class VerticalScrolledFrame:
    def __init__(self, master, **kwargs):
        width = kwargs.pop( 'width', None )
        height = kwargs.pop( 'height', None )
        bg = kwargs.pop( 'bg', kwargs.pop( 'background', None ) )
        self.outer = tk.Frame( master, **kwargs )

        self.vsb = tk.Scrollbar( self.outer, orient=tk.VERTICAL )
        self.vsb.pack( fill=tk.Y, side=tk.RIGHT )
        self.canvas = tk.Canvas( self.outer, highlightthickness=0, width=width, height=height, bg=bg )
        self.canvas.pack( side=tk.LEFT, fill=tk.BOTH, expand=True )
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas.bind( "<Enter>", self._mouse_binding )
        self.canvas.bind( "<Leave>", self._mouse_unbinding )
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame( self.canvas, bg=bg )
        self.canvas.create_window( 4, 4, window=self.inner, anchor='nw' )
        self.inner.bind( "<Configure>", self._on_frame_configure )

        self.outer_attr = set( dir( tk.Widget ) )

    def __getattr__(self, item):
        return getattr( self.outer, item ) if item in self.outer_attr else getattr( self.inner, item )

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox( "all" )
        height = self.canvas.winfo_height()
        self.canvas.config( scrollregion=(0, 0, x2, max( y2, height )) )

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll( -1, "units" )
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll( 1, "units" )

    def _mouse_binding(self, event=None):
        self.canvas.bind_all( "<4>", self._on_mousewheel )
        self.canvas.bind_all( "<5>", self._on_mousewheel )
        self.canvas.bind_all( "<MouseWheel>", self._on_mousewheel )

    def _mouse_unbinding(self, event=None):
        self.canvas.unbind_all( "<4>" )
        self.canvas.unbind_all( "<5>" )
        self.canvas.unbind_all( "<MouseWheel>" )

    def __str__(self):
        return str( self.outer )


class ChangeValue( tk.Button ):
    def __init__(self, master):
        super().__init__( master, text="fill", bg="green", command=self.clicked )

    def clicked(self):
        if self['text'] == "fill":
            self.configure( text="unfill", bg="red" )
            return -1
        else:
            self.configure( text="fill", bg="green" )
            return 1

    def __int__(self):
        if self['text'] == "unfill":
            return -1
        if self['text'] == "fill":
            return 1


class ChangeLevel( tk.Button ):
    def __init__(self, master):
        super().__init__( master, text="│", bg="green", command=self.clicked )

    def clicked(self):
        if self['text'] == "│":
            self.configure( text="─", bg="red" )
            return -1
        else:
            self.configure( text="│", bg="green" )
            return 1

    def __int__(self):
        if self['text'] == "─":
            return -1
        if self['text'] == "│":
            return 1


class ChangeQuarter( tk.Button ):
    def __init__(self, master):
        super().__init__( master, text="quarter 1", width=10, command=self.clicked )

    def clicked(self):
        if self['text'] == "quarter 1":
            self.configure( text="quarter 2" )
            return 1
        if self['text'] == "quarter 2":
            self.configure( text="quarter 3" )
            return 2
        if self['text'] == "quarter 3":
            self.configure( text="quarter 4" )
            return 3
        if self['text'] == "quarter 4":
            self.configure( text="quarter 1" )
            return 4

    def __int__(self):
        if self['text'] == "quarter 1":
            return 1
        if self['text'] == "quarter 2":
            return 2
        if self['text'] == "quarter 3":
            return 3
        if self['text'] == "quarter 4":
            return 4


class Plotting:
    def __init__(self, master, shape, radius, width, height, ax, ay, c_quarter, value,
                 plott, canvas, info=0, level=-1):
        self.master = master
        self.shape = shape
        self.radius = None if radius is None else float( radius.get() )
        self.width = None if width is None else float( width.get() )
        self.height = None if height is None else float( height.get() )
        self.ax = None if ax is None else float( ax.get() )
        self.ay = None if ay is None else float( ay.get() )
        self.c_quarter = c_quarter
        self.value = value
        self.plott = plott
        self.canvas = canvas
        self.info = info
        self.level = level

    def clearing(self):
        self.plott.clear()

    def plotting(self, if_clear):
        theta = []
        if self.info == 1:
            if not askyesno( title='Adding figure to main project?',
                             message='First, check the preview using the \"plot\" button.\n '
                                     'You cannot delete a single figure from the main project window.' ):
                return 0
        if if_clear == 1:
            self.clearing()
        # self.toolbar.update()
        color = "#" + ''.join( [random.choice( '0123456789ABCDEF' ) for i in range( 6 )] )
        if self.shape == '◯':
            theta = np.linspace( 0, 2 * np.pi, 100 )
        elif self.shape == '◖':
            theta = np.linspace( 0.5 * np.pi, 1.5 * np.pi, 100 )
        elif self.shape == '◗':
            theta = np.linspace( 1.5 * np.pi, 2.5 * np.pi, 100 )
        elif self.shape == '◓':
            theta = np.linspace( 0, np.pi, 100 )
        elif self.shape == '◒':
            theta = np.linspace( np.pi, 2 * np.pi, 100 )
        if self.shape == '◔':
            if self.c_quarter == 1:
                theta = np.linspace( 0, 0.5 * np.pi, 100 )
            elif self.c_quarter == 2:
                theta = np.linspace( 0.5 * np.pi, 1 * np.pi, 100 )
            elif self.c_quarter == 3:
                theta = np.linspace( 1 * np.pi, 1.5 * np.pi, 100 )
            elif self.c_quarter == 4:
                theta = np.linspace( 1.5 * np.pi, 2 * np.pi, 100 )
        if (self.shape == '◯' or
                self.shape == '◖' or
                self.shape == '◗' or
                self.shape == '◓' or
                self.shape == '◒'):
            x_line = np.linspace( self.radius * np.cos( theta[0] ) + self.ax,
                                  self.radius * np.cos( theta[-1] ) + self.ax, 100 )
            y_line = np.linspace( self.radius * np.sin( theta[0] ) + self.ay,
                                  self.radius * np.sin( theta[-1] ) + self.ay, 100 )
            a = self.radius * np.cos( theta ) + self.ax
            b = self.radius * np.sin( theta ) + self.ay
            if self.value == 1:
                self.plott.fill( a, b, x_line, y_line, color=color )
            elif self.value == -1:
                self.plott.fill( a, b, x_line, y_line, color="#E1E1E1", zorder=1000 )
            self.plott.plot( self.ax, self.ay, '.', color="black", zorder=1000 )
            self.plott.annotate( f"x:{self.ax},y:{self.ay}", (self.ax, self.ay),
                                 color="black", zorder=1000 )
        elif self.shape == '◔':
            x_line = (self.radius * np.cos( theta[0] ) + self.ax,
                      self.ax,
                      self.radius * np.cos( theta[-1] ) + self.ax)
            y_line = (self.radius * np.sin( theta[0] ) + self.ay,
                      self.ay,
                      self.radius * np.sin( theta[-1] ) + self.ay)
            a = self.radius * np.cos( theta ) + self.ax
            b = self.radius * np.sin( theta ) + self.ay
            if self.value == 1:
                self.plott.fill( a, b, x_line, y_line, color=color )
            elif self.value == -1:
                self.plott.fill( a, b, x_line, y_line, color="#E1E1E1", zorder=1000 )
            self.plott.plot( self.ax, self.ay, '.', color="black", zorder=1000 )
            self.plott.annotate( f"x:{self.ax},y:{self.ay}", (self.ax, self.ay),
                                 color="black", zorder=1000 )
        elif self.shape == '◼':
            pointdl = [self.ax - self.width / 2, self.ay - self.height / 2]
            pointdr = [self.ax + self.width / 2, self.ay - self.height / 2]
            pointul = [self.ax - self.width / 2, self.ay + self.height / 2]
            pointur = [self.ax + self.width / 2, self.ay + self.height / 2]
            linex = [pointdl[0], pointdr[0], pointur[0], pointul[0], pointdl[0]]
            liney = [pointdl[1], pointdr[1], pointur[1], pointul[1], pointdl[1]]
            if self.value == 1:
                self.plott.fill( linex, liney, color=color )
            elif self.value == -1:
                self.plott.fill( linex, liney, color="#E1E1E1", zorder=1000 )
            self.plott.plot( self.ax, self.ay, '.', color="black", zorder=1000 )
            self.plott.annotate( f"x:{self.ax},y:{self.ay}", (self.ax, self.ay),
                                 color="black", zorder=1000 )
        elif self.shape == '◣':
            point1 = [self.ax, self.ay]
            point2 = [self.ax + self.width, self.ay]
            point3 = [self.ax, self.ay + self.height]
            linex = [point1[0], point2[0], point3[0], point1[0]]
            liney = [point1[1], point2[1], point3[1], point1[1]]
            if self.value == 1:
                self.plott.fill( linex, liney, color=color )
            if self.value == -1:
                self.plott.fill( linex, liney, color="#E1E1E1", zorder=1000 )
            self.plott.plot( self.ax, self.ay, '.', color="black", zorder=1000 )
            self.plott.annotate( f"x:{self.ax},y:{self.ay}", (self.ax, self.ay),
                                 color="black", zorder=1000 )
        elif self.shape == '│':
            point1 = [self.ax, self.ay]
            point2 = []
            if self.level == 1:
                point2 = [self.ax, self.ay + self.width]
                self.plott.plot([point1[0], point2[0]], [point1[1], point2[1]], color=color)
            elif self.level == -1:
                point2 = [self.ax + self.width, self.ay]
                self.plott.plot([point1[0], point2[0]], [point1[1], point2[1]], color=color)
        elif self.shape == 'X':
            self.clearing()
        self.plott.axis( 'equal' )
        self.canvas.draw()


class WidgetsInScrolledFrame:
    siema = 0

    def __init__(self, master):
        self.master = master
        self.count = 0
        self.frame_list = []
        self.calc_list = []
        calc_list = []
        self.alist = []
        self.ax_coord = []
        self.ay_coord = []
        self.ax_cmii = []
        self.ay_cmii = []
        self.all_frame = VerticalScrolledFrame( master, width=1500, height=800, borderwidth=2,
                                                relief=tk.SUNKEN, background="#c4a990" )
        self.all_frame.grid( column=0, row=0, sticky='we' )
        self.frame_opt = VerticalScrolledFrame( self.all_frame, width=750, height=10, borderwidth=2,
                                                relief=tk.SUNKEN, background="#b4f000" )
        self.frame_opt.grid( column=0, row=0, sticky='nsew' )
        self.frame_plot = VerticalScrolledFrame( self.all_frame, width=700, height=750, borderwidth=2,
                                                 relief=tk.SUNKEN, background="#b4f000" )
        self.frame_plot.grid( column=1, row=0, rowspan=4, sticky='nsew' )
        self.frame = VerticalScrolledFrame( self.all_frame, width=750, height=500, borderwidth=2,
                                            relief=tk.SUNKEN, background="light pink" )
        self.frame.grid( column=0, row=1, sticky='nsew' )
        self.frame_output = VerticalScrolledFrame( self.all_frame, width=700, height=10, borderwidth=2,
                                                   relief=tk.SUNKEN, background="#b4f445" )
        self.frame_output.grid( column=0, row=2, sticky='nsew' )
        self.frame_tool = VerticalScrolledFrame( self.all_frame, width=700, height=10, borderwidth=2,
                                                 relief=tk.SUNKEN, background="#b4f000" )
        self.frame_tool.grid( column=0, row=3, sticky='nsew' )
        # fig1
        self.fig1 = Figure( figsize=(6, 5), dpi=72 )
        self.fig1.suptitle( "Plot single figure here with \"plot\" button" )
        self.plot1 = self.fig1.subplots( 1 )
        self.canvas1 = FigureCanvasTkAgg( self.fig1, master=self.frame_plot )
        self.canvas1.get_tk_widget().grid( column=0, row=0 )
        # fig2
        self.fig2 = Figure( figsize=(6, 5), dpi=72 )
        self.fig2.suptitle( "Then add the figure to the main project with \"add to main\" button" )
        self.plot2 = self.fig2.subplots( 1 )
        self.canvas2 = FigureCanvasTkAgg( self.fig2, master=self.frame_plot )
        self.toolbar2 = NavigationToolbar2Tk( self.canvas2, self.frame_tool )
        self.canvas2.get_tk_widget().grid( column=0, row=1 )
        self.frame_list.append( [
            tk.Button( self.frame_opt, text='◯', command=lambda: self.new_figure( shape='◯' ) ),
            tk.Button( self.frame_opt, text='◖', command=lambda: self.new_figure( shape='◖' ) ),
            tk.Button( self.frame_opt, text='◗', command=lambda: self.new_figure( shape='◗' ) ),
            tk.Button( self.frame_opt, text='◓', command=lambda: self.new_figure( shape='◓' ) ),
            tk.Button( self.frame_opt, text='◒', command=lambda: self.new_figure( shape='◒' ) ),
            tk.Button( self.frame_opt, text='◔', command=lambda: self.new_figure( shape='◔' ) ),
            tk.Button( self.frame_opt, text='◼', command=lambda: self.new_figure( shape='◼' ) ),
            tk.Button( self.frame_opt, text='◣', command=lambda: self.new_figure( shape='◣' ) ),
            tk.Button( self.frame_opt, text='│', command=lambda: self.new_figure( shape='│' ) ),
            tk.Button( self.frame_opt, text='X',
                       command=lambda: (self.clear_all(), Plotting( master=self.frame_plot, shape='X',
                                                                    radius=None, width=None, height=None,
                                                                    ax=None,
                                                                    ay=None,
                                                                    c_quarter=None,
                                                                    value=None,
                                                                    plott=self.plot2,
                                                                    canvas=self.canvas2 ).plotting( if_clear=1 )) ),
            tk.Button( self.frame_opt, text="history", command=lambda: self.popup_window() )
        ] )
        for i in range( 0, len( self.frame_list[-1] ) ):
            self.frame_list[-1][i].grid( column=i, row=self.count, sticky=tk.W )
        self.count += 1
        tk.Button( self.frame_output, text='print',
                   command=lambda: print( self.calc_list )
                   ).grid( column=0, row=0 )
        tk.Button( self.frame_output, text='count area',
                   command=lambda: (print( self.exec(option='area'), "area" ))
                   ).grid( column=1, row=0 )
        tk.Button( self.frame_output, text='static moment',
                   command=lambda:
                   (print( self.exec(option='ax stat'), self.exec(option='ay stat'), "static moments" ))
                   ).grid( column=2, row=0 )
        tk.Button( self.frame_output, text='center of mass',
                   command=lambda:
                   (print( self.exec(option='ax mass'), self.exec(option='ay mass'), "center of mass" ))
                   ).grid( column=3, row=0 )
        tk.Button( self.frame_output, text='main central moment of inertia',
                   command=lambda:
                   (print(self.exec(option='ax cmi'), self.exec(option='ay cmi'), "moment of inertia"))
                   ).grid( column=4, row=0 )

    def exec(self, option):
        return Calculate().__int__( command=option, listtt=self.calc_list, alisttt=self.alist,
                                    ax_coord=self.ax_coord, ay_coord=self.ay_coord,
                                    ax_cmii=self.ax_cmii, ay_cmii=self.ay_cmii )

    def popup_window(self):
        window = tk.Toplevel()

        label = tk.Label( window, text="Hello World!" )
        label.pack( fill='x', padx=50, pady=5 )

        button_close = tk.Button( window, text="Close", command=window.destroy )
        button_close.pack( fill='x' )

    def clear_all(self):
        try:
            self.count = 1
            # self.calc_list = []
            self.calc_list = []
            self.alist = []
            self.ax_coord = []
            self.ay_coord = []
            self.ax_cmii = []
            self.ay_cmii = []
            for i in range( 0, len( self.frame_list ) ):
                i += 1
                for j in range( 0, len( self.frame_list[i] ) ):
                    self.frame_list[i][j].destroy()
            # self.frame_list = []
        except IndexError:
            pass

    def new_figure(self, shape):
        entry1 = EntryWithPlaceholder( self.frame, "radius" )
        entry2 = EntryWithPlaceholder( self.frame, "width" )
        entry3 = EntryWithPlaceholder( self.frame, "height" )
        entry4 = EntryWithPlaceholder( self.frame, "ox middle" )
        entry5 = EntryWithPlaceholder( self.frame, "oy middle" )
        quarter = ChangeQuarter( self.frame )
        change_value = ChangeValue( self.frame )
        change_level = ChangeLevel( self.frame )
        if shape == '◯':
            self.frame_list.append( [
                tk.Label( self.frame, text='◯' ),
                entry1,
                entry4,
                entry5,
                change_value,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◯',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1 ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◯',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1 ).plotting( if_clear=0 ),
                                            Calculate( shape='◯', radius=entry1, ax=entry4, ay=entry5,
                                                       value=change_value.__int__()
                                                       ).applist( self.calc_list )) )] )
        if shape == '◖':
            self.frame_list.append( [
                tk.Label( self.frame, text='◖' ),
                entry1,
                entry4,
                entry5,
                change_value,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◖',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1 ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◖',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1 ).plotting( if_clear=0 ),
                                            Calculate( shape='◖', radius=entry1, ax=entry4, ay=entry5,
                                                       value=change_value.__int__()
                                                       ).applist( self.calc_list )) )] )
        if shape == '◗':
            self.frame_list.append( [
                tk.Label( self.frame, text='◗' ),
                entry1,
                entry4,
                entry5,
                change_value,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◗',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1 ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◗',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1 ).plotting( if_clear=0 ),
                                            Calculate( shape='◗', radius=entry1, ax=entry4, ay=entry5,
                                                       value=change_value.__int__()
                                                       ).applist( self.calc_list )) )] )
        if shape == '◓':
            self.frame_list.append( [
                tk.Label( self.frame, text='◓' ),
                entry1,
                entry4,
                entry5,
                change_value,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◓',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1 ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◓',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1 ).plotting( if_clear=0 ),
                                            Calculate( shape='◓', radius=entry1, ax=entry4, ay=entry5,
                                                       value=change_value.__int__()
                                                       ).applist( self.calc_list )) )] )
        if shape == '◒':
            self.frame_list.append( [
                tk.Label( self.frame, text='◒' ),
                entry1,
                entry4,
                entry5,
                change_value,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◒',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1 ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◒',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1 ).plotting( if_clear=0 ),
                                            Calculate( shape='◒', radius=entry1, ax=entry4, ay=entry5,
                                                       value=change_value.__int__()
                                                       ).applist( self.calc_list )) )] )
        if shape == '◔':
            self.frame_list.append( [
                tk.Label( self.frame, text='◔' ),
                entry1,
                entry4,
                entry5,
                quarter,
                change_value,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◔',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=quarter.__int__(),
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1 ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◔',
                                                      radius=entry1, width=None, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=quarter.__int__(),
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1 ).plotting( if_clear=0 ),
                                            Calculate( shape='◔', radius=entry1, ax=entry4, ay=entry5,
                                                       c_quarter=quarter.__int__(),
                                                       value=change_value.__int__()
                                                       ).applist( self.calc_list )) )] )
        if shape == '◼':
            self.frame_list.append( [
                tk.Label( self.frame, text='◼' ),
                entry2,
                entry3,
                entry4,
                entry5,
                change_value,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◼',
                                                      radius=None, width=entry2, height=entry3,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1 ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◼',
                                                      radius=None, width=entry2, height=entry3,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1 ).plotting( if_clear=0 ),
                                            Calculate( shape='◼', width=entry2, height=entry3, ax=entry4, ay=entry5,
                                                       value=change_value.__int__()
                                                       ).applist( self.calc_list )) )] )
        if shape == '◣':
            self.frame_list.append( [
                tk.Label( self.frame, text='◣' ),
                entry2,
                entry3,
                entry4,
                entry5,
                change_value,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◣',
                                                      radius=None, width=entry2, height=entry3,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1 ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='◣',
                                                      radius=None, width=entry2, height=entry3,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1 ).plotting( if_clear=0 ),
                                            Calculate( shape='◣', width=entry2, height=entry3, ax=entry4, ay=entry5,
                                                       value=change_value.__int__()
                                                       ).applist( self.calc_list )) )] )
        if shape == '│':
            self.frame_list.append( [
                tk.Label( self.frame, text='│' ),
                entry2,
                entry4,
                entry5,
                change_level,
                tk.Button( self.frame, text='plot',
                           command=lambda: (Plotting( master=self.frame_plot, shape='│',
                                                      radius=None, width=entry2, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot1,
                                                      canvas=self.canvas1,
                                                      level=change_level.__int__()
                                                      ).plotting( if_clear=1 )) ),
                tk.Button( self.frame, text='plot on main',
                           command=lambda: (Plotting( master=self.frame_plot, shape='│',
                                                      radius=None, width=entry2, height=None,
                                                      ax=entry4,
                                                      ay=entry5,
                                                      c_quarter=None,
                                                      value=change_value.__int__(),
                                                      plott=self.plot2,
                                                      canvas=self.canvas2,
                                                      info=1,
                                                      level=change_level.__int__()).plotting( if_clear=0 ),
                                            Calculate( shape='│', width=entry2, ax=entry4, ay=entry5,
                                                       value=change_value.__int__(),
                                                       level=change_level.__int__()
                                                       ).applist( self.calc_list )) )] )
        for i in range( 0, len( self.frame_list[-1] ) ):
            self.frame_list[-1][i].grid( column=i, row=self.count, sticky=tk.W )
        self.frame.columnconfigure( self.count, weight=1 )
        try:
            count = self.count - 1
            if count == 0:
                pass
            else:
                for i in range( 0, len( self.frame_list[count] ) ):
                    self.frame_list[count][i].config( state=tk.DISABLED )
        except IndexError:
            pass
        except tk.TclError:
            print( "tk.TclError" )
            pass
        self.count += 1


if __name__ == "__main__":
    root = tk.Tk()
    root.title( "Mass Geometry Calculator" )
    root.configure( background="#C5ECF3" )
    root.geometry( '1350x800+150+0' )
    WidgetsInScrolledFrame( root )
    root.grid_columnconfigure( 0, weight=1 )
    root.grid_rowconfigure( 1, weight=1 )
    root.mainloop()
