from tkinter import *
import random
import math
import time
import collections
import _thread
from functools import partial


x_build = 100
y_build = 100
resources = collections.OrderedDict()
resources['Resources'] = '\n'
window = Tk()
window.title('Game')
window.geometry('1500x800+150+100')
window.grab_set()
background = PhotoImage(file='bg.gif', width=1200, height=800)
window_background = Canvas(window, width=1200, height=800)
window_background.create_image(600, 400, image=background)
window_background.create_image(600, 800, image=background)
resources_amount = Label(window, width=37, height=20, bg='gray85', fg='black', text='Resources:\n', font='Arial 10 bold')
resources_amount.place(x=1200, y=0)
hunters_hut_img = PhotoImage(file='hunters_hut.gif')
lumberjack_hut_img = PhotoImage(file='lumberjack_hut.gif')
miner_hut_img = PhotoImage(file='miner_hut.gif')
barrack_img = PhotoImage(file='barrack.gif')
stone = PhotoImage(file='stone.gif')
wood = PhotoImage(file='wood.gif')
food = PhotoImage(file='food.gif')
window_background.focus_set()
window_background.pack(expand=YES, fill=BOTH)


class BarrackRequestHandler:
    def __init__(self, successer):
        self.successer = successer

    def handle(self, *args):
        # do smth
        return None

    def error_message(self, msg):
        error = Tk()
        error.title('Error')
        error.geometry('300x40+800+350')
        error_desc = Text(error)
        error_desc.insert(1.0, msg)
        error_desc.pack()
        error.mainloop()

    def unpack(self):
        for i in buildings[3][1][0].division_buttons:
            i.place_forget()
        buildings[3][1][0].division_buttons = list()


class PlaceButtonsHandler(BarrackRequestHandler):
    def handle(self, *args):
        if buildings[3][1][0] is not None:
            buildings[3][1][0]._place_division_buttons(self.successer, *args)
        else:
            self.error_message('Barrack does not exist!')


class DivisionMoveHandler(BarrackRequestHandler):
    def handle(self, *args):
        self.unpack()
        if divisions[args[0]][1][0][args[1]]._get_size() == 0:
            self.error_message(divisions[args[0]][0] + ' is empty!')
        else:
            self.successer(*args)


class AddUnitHandler(BarrackRequestHandler):
    def handle(self, *args):
        self.unpack()
        if divisions[args[0]][1][0][args[1]]._get_size() == divisions[args[0]][1][0][args[1]].capacity:
            del buildings[3][1][0]._units[-1]
            self.error_message(divisions[args[0]][0] + ' is full!')
        else:
            self.successer(*args)


class HealDivisionHandler(BarrackRequestHandler):
    def handle(self, *args):
        self.unpack()
        if isinstance(divisions[args[0]][1][0][args[1]], AdditionalAbilities):
            self.successer(*args)
        else:
            self.error_message(divisions[args[0]][0] + 'is not upgraded!')


class UpgradeDivisionHandler(BarrackRequestHandler):
    def handle(self, *args):
        self.unpack()
        if isinstance(divisions[args[0]][1][0][args[1]], AdditionalAbilities):
            self.successer(*args)
        else:
            self.error_message(divisions[args[0]][0] + 'is already upgraded!')


def construct(num):
    global buildings
    buildings[num][1][0] = buildings[num][1][1](x_build, y_build)
    if buildings[num][1][2] is not None:
        buildings[num][1][2]._building_to_collect = buildings[num][1][0]
    window_background.update()
    for i in side_buttons[0]:
        i.place_forget()


def new_division(num):
    global divisions
    divisions[num][1][0].append(divisions[num][1][1]())
    Barbarians.subscribe(divisions[num][1][0][-1])
    for i in side_buttons[1]:
        i.place_forget()


def pack_side_buttons(buttons, func, key):
    for i in range(0, len(buttons) // 3):
        for j in range(0, 3):
            side_buttons[key].append(Button(window, width=12, height=3, bg='gray85', text=buttons[i * 3 + j][0],
                                           command=partial(func, i * 3 + j)))
            side_buttons[key][i * 3 + j].place(x=1200 + j*94, y=386 + i * 60)
    i = len(buttons) // 3
    for j in range(0, len(buttons) % 3):
        side_buttons[key].append(Button(window, width=12, height=3, bg='gray85', text=buttons[i * 3 + j][0],
                                       command=partial(func, i * 3 + j)))
        side_buttons[key][i * 3 + j].place(x=1200 + j * 94, y=386 + i * 60)


def set_coords(e):
    global x_build, y_build
    x_build = window.winfo_pointerx() - window.winfo_rootx()
    y_build = window.winfo_pointery() - window.winfo_rooty()


window_background.bind('<Button-3>', set_coords)
window_background.bind('m', lambda event: PlaceButtonsHandler(DivisionMoveHandler(buildings[3][1][0]._move_division).handle).handle(x_build, y_build))
window_background.bind('h', lambda event: PlaceButtonsHandler(HealDivisionHandler(buildings[3][1][0]._heal_division).handle).handle(buildings[3][1][0]._x_coord, buildings[3][1][0]._y_coord))
window_background.bind('u', lambda event: PlaceButtonsHandler(UpgradeDivisionHandler(buildings[3][1][0]._upgrade_division).handle).handle(buildings[3][1][0]._x_coord, buildings[3][1][0]._y_coord))
window_background.bind('i', lambda event: Barbarians.start_invasion())


class Squad:
    def __init__(self):
        self.units = list()
        self.capacity = 10
        self.in_action = False

    def _add_unit(self, unit):
        self.units.append(unit)

    def _move(self, x, y, delta_x, delta_y):
        for i in self.units:
            _thread.start_new(i._move,(x, y, delta_x, delta_y))

    def __getattr__(self, item):
        if item == '_hit_points':
            result = 0
            for i in self.units:
                result += i._hit_points
            return result

    def _get_size(self):
        return len(self.units)

    def sum_damage(self):
        damage = 0
        for i in range(0, len(self.units)):
            if not self.units[i]._dead:
                damage += self.units[i]._damage
        return damage

    def get_damage(self, damage):
        self.units[-1]._hit_points -= damage
        if self.units[-1]._hit_points < 0:
            del self.units[-1]
            self.units.pop()
        window_background.update()

    def recieve_notification(self, quantity, x, y):
        _thread.start_new(self.defend, (quantity, x, y))

    def defend(self, quantity, x, y):
        self._move(x, y, 10, 10)
        while Barbarians.army._get_size() > 0:
            Barbarians.army.get_damage(self.sum_damage())
            time.sleep(1.5)


class Army(Squad):
    def __init__(self):
        super().__init__()
        self.capacity = 100

    def _get_size(self):
        result = 0
        for i in range(0, len(self.units)):
            if hasattr(self.units[i], '__iter__'):
                result += self.units[i]._get_size()
            else:
                result += 1
        return result


class AdditionalAbilities(Army):
    def __init__(self, division):
        super().__init__()
        self.units = division.units
        self.in_action = division.in_action
        if isinstance(division, Squad):
            self.capacity = 10
        else:
            self.capacity = 100

    def healing(self):
        for i in self.units:
            if i._hit_points < i._max_hit_points:
                i._hit_points += 1
        time.sleep(1)


def singleton(cls):
    instances = {}

    def getinstance(*args):
        if cls not in instances or instances[cls]._deleted:
            instances[cls] = cls(*args)
        else:
            error = Tk()
            error.title('Error')
            error.geometry('300x40+800+350')
            error_desc = Text(error)
            error_desc.insert(1.0, instances[cls]._name + " already exists!")
            error_desc.pack()
            error.mainloop()
            # to run tests without GUI
        return instances[cls]
    return getinstance


class Resource:
    def __init__(self, name, btc, img, x, y):
        self._building_to_collect = btc
        self._name = name
        self._x_coord = x
        self._y_coord = y
        self._image = img
        resources[self._name] = 0
        self._button = Button(image=img, bg='green')
        self._button.place(x=x, y=y)
        self._button.bind('<Button-3>', self._collect)

    def _unit_collect(self, unit):
        while True:
            unit._move(self._x_coord, self._y_coord, self._image.width(), self._image.height())
            ctr = 0
            while ctr < unit._capacity:
                ctr += unit._production
                time.sleep(5)
            unit._move(self._building_to_collect._x_coord, self._building_to_collect._y_coord, 50, 50)
            resources[self._name] += ctr
            time.sleep(1.5)
            resources_amount.configure(text='\n'.join('{}: {}'.format(key, val) for key, val in resources.items()))

    def _collect(self, e):
        if self._building_to_collect is not None:
            for i in self._building_to_collect._units:
                if (not i._dead) and (not i._now_working):
                    i._now_working = True
                    args = list()
                    args.append(i)
                    _thread.start_new(self._unit_collect, tuple(args))


class Building:
    def __init__(self, hp, x, y, properties, ut, img, nm):
        def _open_list(e):
            for i in range(0, len(self._props)):
                self._buttons[i].place(x=self._x_coord, y=self._y_coord + i * 26)

        self._hit_points = hp
        self._name = nm
        self._image = img
        self._main_button = Button(window, image=img, bg='green')
        self._unit_type = ut
        self._units = []
        self._buttons = []
        self._deleted = False
        self._x_coord = x
        self._y_coord = y
        self._props = properties
        self._main_button.bind("<Button-1>", _open_list)
        self._main_button.place(x=x, y=y)
        for i in range(0, len(self._props) - 1):
            self._buttons.append(Button(window, text=self._props[i], width=15, height=1, bg='grey', fg='black',
                                       command=partial(self._make_unit, self._unit_type[i])))
        self._buttons.append(Button(window, text=self._props[-1], width=15, height=1, bg='grey', fg='black',
                                   command=self._destroy))

    def _destroy(self):
        self._main_button.destroy()
        for i in self._buttons:
            i.destroy()
        for i in self._units:
            i._destroy()
        self._deleted = True

    def _make_unit(self, unit_type):
        u = unit_type(self._x_coord + random.choice([-15, self._image.width() + 45]) + random.randrange(-10, 10),
               self._y_coord + random.choice([-15, self._image.height() + 15]) + random.randrange(-10, 10))
        self._units.append(u)
        for i in self._buttons:
            i.place_forget()


class Unit:
    def __init__(self, hp, spd, x, y, clr, unit_name):
        self._x_coord = x
        self._y_coord = y
        self._hit_points = hp
        self._max_hit_points = hp
        self._move_speed = spd
        self._point = window_background.create_oval(x, y, x+10, y+10, fill=clr, tag=unit_name)
        self._dead = False

    def __del__(self):
        window_background.delete(self._point)

    def _destroy(self):
        window_background.delete(self._point)
        self._dead = True

    def _move(self, x, y, delta_x, delta_y):
        while (self._x_coord - x) not in range(-self._move_speed - 1, self._move_speed + 1 + delta_x):
            window_background.move(self._point, math.copysign(self._move_speed, x - self._x_coord), 0)
            window_background.update()
            self._x_coord += math.copysign(self._move_speed, x - self._x_coord)
            time.sleep(0.1)
        while (self._y_coord - y) not in range(-self._move_speed - 1, self._move_speed + 1 + delta_y):
            window_background.move(self._point, 0, math.copysign(self._move_speed, y - self._y_coord))
            self._y_coord += math.copysign(self._move_speed, y - self._y_coord)
            window_background.update()
            time.sleep(0.1)


class Worker(Unit):
    def __init__(self, hp, spd, pr, cp, x, y, clr, unit_name):
        Unit.__init__(self, hp, spd, x, y, clr, unit_name)
        self._capacity = cp
        self._production = pr
        self._now_working = False


class Warrior(Unit):
    def __init__(self, hp, spd, dmg, x, y, clr, unit_name):
        Unit.__init__(self, hp, spd, x, y, clr, unit_name)
        self._damage = dmg


class Hunter(Worker):
    def __init__(self, x, y):
        Worker.__init__(self, 10, 10, 1, 3, x, y, 'brown', 'hunter')


class Lumberjack(Worker):
    def __init__(self, x, y):
        Worker.__init__(self, 10, 10, 1, 3, x, y, 'green', 'lumberjack')


class Miner(Worker):
    def __init__(self, x, y):
        Worker.__init__(self, 10, 10, 1, 3, x, y, 'grey', 'miner')


class Swordsman(Warrior):
    def __init__(self, x, y):
        Warrior.__init__(self, 30, 7, 10, x, y, 'snow3', 'swordsman')


class Archer(Warrior):
    def __init__(self, x, y):
        Warrior.__init__(self, 20, 12, 7, x, y, 'OliveDrab4', 'archer')


class Horseman(Warrior):
    def __init__(self, x, y):
        Warrior.__init__(self, 40, 20, 15, x, y, 'gold2', 'horseman')


class Barbarian(Warrior):
    def __init__(self, x, y):
        Warrior.__init__(self, 30, 15, 7, x, y, 'red', 'barbarian')


@singleton
class HuntersHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Hunter', 'Destroy'], [Hunter], hunters_hut_img, 'Hunters Hut')


@singleton
class LumberjackHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Lumberjack', 'Destroy'], [Lumberjack], lumberjack_hut_img, 'Lumberjack Hut')


@singleton
class MinerHut(Building):
    def __init__(self, x, y):
        Building.__init__(self, 30, x, y, ['New Miner', 'Destroy'], [Miner], miner_hut_img, 'Miner Hut')


@singleton
class Barrack(Building):
    def __init__(self, x, y):
        Building.__init__(self, 100, x, y, ['New Swordsman', 'New Archer', 'New Horseman', 'Destroy'],
                          [Swordsman, Archer, Horseman], barrack_img, 'Barrack')
        self.division_buttons = list()

    def _place_division_buttons(self, func, x, y):
        global divisions
        for j in range(0, 2):
            for i in range(0, len(divisions[j][1][0])):
                self.division_buttons.append(Button(window, text=divisions[j][0] + ' ' + str(i + 1), width=15,
                                                    height=1, bg='grey', fg='black', command=partial(func, j, i)))
        for i in range(0, len(self.division_buttons)):
            self.division_buttons[i].place(x=x, y=y + i * 26)

    def _add_unit_to_division(self, division_type, key):
        divisions[division_type][1][0][key]._add_unit(self._units[-1])

    def _make_unit(self, unit_type):
        PlaceButtonsHandler(AddUnitHandler(self._add_unit_to_division).handle).handle(self._x_coord, self._y_coord)
        super()._make_unit(unit_type)

    def _move_division(self, division_type, key):
        divisions[division_type][1][0][key]._move(x_build, y_build, 20, 20)

    def _upgrade_division(self, division_type, key):
        divisions[division_type][1][0][key] = AdditionalAbilities(divisions[division_type][1][0][key])

    def _heal_army(self, division_type, key):
        divisions[division_type][1][0][key].healing()


class Enemy:
    def __init__(self):
        self.army = Army()
        self.subscribers = list()

    def spawn_enemies(self, quantity=20, x=100, y=100):
        for i in range(0, quantity):
            self.army._add_unit(Barbarian(x + random.choice([-15, 15]) + random.randrange(-10, 10),
                                  y + random.choice([-15, 15]) + random.randrange(-10, 10)))

    def subscribe(self, obj):
        self.subscribers.append(obj)

    def attack_notify(self, quantity=20, x=100, y=100):
        for i in self.subscribers:
            i.recieve_notification(quantity, x, y)

    def start_invasion(self):
        self.spawn_enemies()
        self.attack_notify()



Barbarians = Enemy()
stone_res = Resource('Stone', None, stone, random.randrange(100, 1000), random.randrange(100, 500))
wood_res = Resource('Wood', None, wood, random.randrange(100, 1000), random.randrange(100, 500))
food_res = Resource('Food', None, food, random.randrange(100, 1000), random.randrange(100, 500))
buildings = [['Hunters Hut', [None, HuntersHut, food_res]], ['Lumberjack Hut', [None, LumberjackHut, wood_res]],
             ['Miner Hut', [None, MinerHut, stone_res]], ['Barrack', [None, Barrack, None]]]
Armies = list()
Squads = list()
divisions = [['Army', [Armies, Army]], ['Squad', [Squads, Squad]]]
side_buttons = [[], []]
create_building = Button(window, width=12, height=3, bg='gray85', text='Create Building',
                         command=partial(pack_side_buttons, buildings, construct, 0))
create_building.place(x=1200, y=326)
create_division = Button(window, width=12, height=3, bg='gray85', text='Create Division',
                         command=partial(pack_side_buttons, divisions, new_division, 1))
create_division.place(x=1294, y=326)
window.mainloop()
#to run tests without GUI



