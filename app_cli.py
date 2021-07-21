from app_gui import *


class Calculate:
    def __init__(self, shape='', radius=None, width=None, height=None, ax=None, ay=None, c_quarter=0, value=1, level=1):
        self.shape = shape
        self.radius = None if radius is None else abs( float( radius.get() ) )
        self.width = None if width is None else float( width.get() )
        self.height = None if height is None else float( height.get() )
        self.ax = None if ax is None else float( ax.get() )
        self.ay = None if ay is None else float( ay.get() )
        self.c_quarter = c_quarter
        self.value = value
        self.level = level

    def applist(self, listt):
        if self.shape == '◯':
            listt.append( {'figure': self.shape, 'radius': self.radius, 'ax': self.ax,
                           'ay': self.ay, 'value': self.value} )
        elif self.shape == '◖':
            listt.append( {'figure': self.shape, 'radius': self.radius, 'ax': self.ax,
                           'ay': self.ay, 'value': self.value} )
        elif self.shape == '◗':
            listt.append( {'figure': self.shape, 'radius': self.radius, 'ax': self.ax,
                           'ay': self.ay, 'value': self.value} )
        elif self.shape == '◓':
            listt.append( {'figure': self.shape, 'radius': self.radius, 'ax': self.ax,
                           'ay': self.ay, 'value': self.value} )
        elif self.shape == '◒':
            listt.append( {'figure': self.shape, 'radius': self.radius, 'ax': self.ax,
                           'ay': self.ay, 'value': self.value} )
        elif self.shape == '◔':
            listt.append( {'figure': self.shape, 'radius': self.radius, 'ax': self.ax,
                           'ay': self.ay, 'quarter': self.c_quarter, 'value': self.value} )
        elif self.shape == '◼':
            listt.append( {'figure': self.shape, 'width': self.width, 'height': self.height,
                           'ax': self.ax, 'ay': self.ay, 'value': self.value} )
        elif self.shape == '◣':
            listt.append( {'figure': self.shape, 'width': self.width, 'height': self.height,
                           'ax': self.ax, 'ay': self.ay, 'value': self.value} )
        elif self.shape == '│':
            listt.append( {'figure': self.shape, 'width': self.width,
                           'ax': self.ax, 'ay': self.ay, 'level': self.level} )

    @staticmethod
    def area(listt, alistt):
        alistt.clear()
        for i in listt:
            if i['figure'] == '◯':
                alistt.append( np.pi * np.power( i['radius'], 2 ) * i['value'] )
            elif i['figure'] == '◖':
                alistt.append( np.pi * np.power( i['radius'], 2 ) * 0.5 * i['value'] )
            elif i['figure'] == '◗':
                alistt.append( np.pi * np.power( i['radius'], 2 ) * 0.5 * i['value'] )
            elif i['figure'] == '◓':
                alistt.append( np.pi * np.power( i['radius'], 2 ) * 0.5 * i['value'] )
            elif i['figure'] == '◒':
                alistt.append( np.pi * np.power( i['radius'], 2 ) * 0.5 * i['value'] )
            elif i['figure'] == '◔':
                alistt.append( np.pi * np.power( i['radius'], 2 ) * 0.25 * i['value'] )
            elif i['figure'] == '◼':
                alistt.append( abs( i['width'] ) * abs( i['height'] ) * i['value'] )
            elif i['figure'] == '◣':
                alistt.append( abs( i['width'] ) * abs( i['height'] ) * 0.5 * i['value'] )
            elif i['figure'] == '│':
                alistt.append( 0 )
        return alistt

    @staticmethod
    def ax_coord_func(listt, ax_coord):
        ax_coord.clear()
        for i in listt:
            if (i['figure'] == '◯' or
                    i['figure'] == '◓' or
                    i['figure'] == '◒' or
                    i['figure'] == '◼'):
                ax_coord.append( i['ax'] )
            elif i['figure'] == '◖':
                ax_coord.append( i['ax'] - (4 * i['radius']) / (3 * np.pi) )
            elif i['figure'] == '◗':
                ax_coord.append( i['ax'] + (4 * i['radius']) / (3 * np.pi) )
            elif i['figure'] == '◔':
                if i['quarter'] == 1:
                    ax_coord.append( i['ax'] + (4 * i['radius']) / (3 * np.pi) )
                elif i['quarter'] == 2:
                    ax_coord.append( i['ax'] - (4 * i['radius']) / (3 * np.pi) )
                elif i['quarter'] == 3:
                    ax_coord.append( i['ax'] - (4 * i['radius']) / (3 * np.pi) )
                elif i['quarter'] == 4:
                    ax_coord.append( i['ax'] + (4 * i['radius']) / (3 * np.pi) )
            elif i['figure'] == '◣':
                ax_coord.append( i['ax'] + i['width'] / 3 )
            elif i['figure'] == '│':
                if i['level'] == 1:
                    ax_coord.append( i['ax'] + i['width']/2 )
                elif i['level'] == -1:
                    ax_coord.append( i['ax'])
        return ax_coord

    @staticmethod
    def ay_coord_func(listt, ay_coord):
        ay_coord.clear()
        for i in listt:
            if (i['figure'] == '◯' or
                    i['figure'] == '◖' or
                    i['figure'] == '◗' or
                    i['figure'] == '◼'):
                ay_coord.append( i['ay'] )
            elif i['figure'] == '◓':
                ay_coord.append( i['ay'] + (4 * i['radius']) / (3 * np.pi) )
            elif i['figure'] == '◒':
                ay_coord.append( i['ay'] - (4 * i['radius']) / (3 * np.pi) )
            elif i['figure'] == '◔':
                if i['quarter'] == 1:
                    ay_coord.append( i['ay'] + (4 * i['radius']) / (3 * np.pi) )
                elif i['quarter'] == 2:
                    ay_coord.append( i['ay'] + (4 * i['radius']) / (3 * np.pi) )
                elif i['quarter'] == 3:
                    ay_coord.append( i['ay'] - (4 * i['radius']) / (3 * np.pi) )
                elif i['quarter'] == 4:
                    ay_coord.append( i['ay'] - (4 * i['radius']) / (3 * np.pi) )
            elif i['figure'] == '◣':
                ay_coord.append( i['ay'] + i['height'] / 3 )
            elif i['figure'] == '│':
                if i['level'] == 1:
                    ay_coord.append( i['ax'])
                elif i['level'] == -1:
                    ay_coord.append( i['ax'] + i['height']/2 )
        return ay_coord

    @staticmethod
    def ax_static_moment(area_list, ayc_list):
        static_moment_ax = []
        static_moment_ax.clear()
        for area, ay_c in zip( area_list, ayc_list ):
            static_moment_ax.append( area * ay_c )
        return sum( static_moment_ax )

    @staticmethod
    def ay_static_moment(area_list, axc_list):
        static_moment_ay = []
        static_moment_ay.clear()
        for area, ax_c in zip( area_list, axc_list ):
            static_moment_ay.append( area * ax_c )
        return sum( static_moment_ay )

    def ax_cmi_func(self, listt, alistt, ay_coord, ax_cmi):
        ax_cmi.clear()
        area_list = self.area( listt, alistt )
        ayc_list = self.ay_coord_func( listt, ay_coord )
        for i, area, ay_c in zip( listt, area_list, ayc_list ):
            jx0 = 0
            d0 = 0
            if i['figure'] == '│':
                d0 = 0
            else:
                d0 = np.power( i['ay'] - self.ay_static_moment( area_list, ayc_list ) / sum( area_list ), 2 )
            steiner = area * d0
            if i['figure'] == '◯':
                jx0 = area * np.power( i['radius'], 2 ) / 4
            elif (i['figure'] == '◖' or
                    i['figure'] == '◗'):
                jx0 = area * np.power( i['radius'], 2 ) / 4
            elif (i['figure'] == '◓' or
                    i['figure'] == '◒'):
                jx0 = area * np.power( i['radius'], 2 ) * (0.25 - 16 / (9 * np.power( np.pi, 2 )))
            elif i['figure'] == '◔':
                jx0 = area * np.power( i['radius'], 2 ) / 4
            elif i['figure'] == '◼':
                jx0 = area * np.power( i['height'], 2 ) / 12
            elif i['figure'] == '◣':
                jx0 = area * np.power( i['height'], 2 ) / 18
            jx = jx0 + steiner
            ax_cmi.append( jx )
        return ax_cmi

    def ay_cmi_func(self, listt, alistt, ax_coord, ay_cmi):
        ay_cmi.clear()
        area_list = self.area( listt, alistt )
        axc_list = self.ax_coord_func( listt, ax_coord )
        for i, area, ax_c in zip( listt, area_list, axc_list ):
            jy0 = 0
            d0 = 0
            if i['figure'] == '│':
                d0 = 0
            else:
                d0 = np.power( i['ax'] - self.ax_static_moment( area_list, axc_list ) / sum( area_list ), 2 )
            steiner = area * d0
            if i['figure'] == '◯':
                jy0 = area * np.power( i['radius'], 2 ) / 4
            elif (i['figure'] == '◖' or
                    i['figure'] == '◗'):
                jy0 = area * np.power( i['radius'], 2 ) / 4
                # area * np.power( i['radius'], 2 ) * (0.25 - 16 / (9 * np.power( np.pi, 2 )))
            elif (i['figure'] == '◓' or
                    i['figure'] == '◒'):
                jy0 = area * np.power( i['radius'], 2 ) / 4
            elif i['figure'] == '◔':
                jy0 = area * np.power( i['radius'], 2 ) / 4
            elif i['figure'] == '◼':
                jy0 = area * np.power( i['width'], 2 ) / 12
            elif i['figure'] == '◣':
                jy0 = area * np.power( i['width'], 2 ) / 18
            jy = jy0 + steiner
            ay_cmi.append( jy )
        return ay_cmi

    def __int__(self, command, listtt, alisttt, ax_coord, ay_coord, ax_cmii, ay_cmii):
        area_list = self.area( listtt, alisttt )
        axc_list = self.ax_coord_func( listtt, ax_coord )
        ayc_list = self.ay_coord_func( listtt, ay_coord )
        ax_cmi_list = self.ax_cmi_func( listtt, alisttt, ay_coord, ax_cmii )
        ay_cmi_list = self.ay_cmi_func( listtt, alisttt, ax_coord, ay_cmii )
        if command == 'area':
            return sum( area_list )
        elif command == 'ax stat':
            return self.ax_static_moment( area_list, ayc_list )
        elif command == 'ay stat':
            return self.ay_static_moment( area_list, axc_list )
        elif command == 'ax mass':
            return self.ay_static_moment( area_list, axc_list ) / sum( area_list )
        elif command == 'ay mass':
            return self.ax_static_moment( area_list, ayc_list ) / sum( area_list )
        elif command == 'ax cmi':
            return sum( ax_cmi_list )
        elif command == 'ay cmi':
            return sum( ay_cmi_list )
