import functools

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED

import text, inga_actions

# myscene is set by scene.py
myscene = None

def init():
    myscene.ui.inventory.visible = True
    cart_lady = myscene.actors['cart_lady']
    cart_lady.prepare_walkpath_move('cart_lady_right')
    cart_lady.next_action()
    text.init(myscene)

def cart_lady_walk(actor, point):
    if point == 'cart_lady_left':
        actor.prepare_walkpath_move('cart_lady_right')
    elif point == 'cart_lady_right':
        actor.prepare_walkpath_move('cart_lady_left')
    else:
        print 'unknown cart lady event'

def inga_walk(actor, point):
    if point == 'inga_walk_right':
        myscene.handler.notify('midterm3', 2)

def ask_about_beans():
    myscene.convo.begin_conversation('beans_1')
    bean_salesman = myscene.actors['bean_salesman']

def end_conversation(convo_name):
    myscene.actors['main'].update_state('stand_front')

walk_handlers = {
    'cart_lady': cart_lady_walk,
    'main': inga_walk
}

def handle_event(event, *args):
    if event == WALK_PATH_COMPLETED:
        info = args[0]
        actor = info['actor']
        point = info['point']
        if walk_handlers.has_key(actor.identifier):
            walk_handlers[actor.identifier](actor, point)
    print "Handled", event, "with", args

def actor_clicked(clicked_actor):    
    print "Clicked on %s" % clicked_actor.name
    if clicked_actor.identifier == 'main':
        actions = {
            'Eat': inga_actions.eat,
            'Pray': inga_actions.pray,
            'Love': inga_actions.love,
            'Jump': clicked_actor.jump
        }
        myscene.ui.show_cam(clicked_actor, actions)
    if clicked_actor.identifier == 'key_1':
        actions = {
            'Pick Up': lambda: clicked_actor.scene.ui.inventory.put_item(clicked_actor),
            'Destroy': None,
            'Throw': None
        }
        myscene.ui.show_cam(clicked_actor, actions)
    if clicked_actor.identifier == 'bean_salesman':
        myscene.ui.show_cam(clicked_actor, {
            'Ask about beans': ask_about_beans
        })
    
#return True when the actor can accept the item, and take the appropriate action for having been given that item
#otherwise return False    
def give_actor(actor, item):
    if actor.identifier == 'bean_salesman':
        myscene.convo.begin_conversation('key_accept')
        return True
    else:
        return False