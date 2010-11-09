import pyglet
import functools
import re

from engine import actor
from engine.interpolator import PulseInterpolator, LinearInterpolator
from engine.util.const import WALK_PATH_COMPLETED
from engine import ui
from engine import cam
from engine import gamestate
from engine import convo
from engine import scenehandler

# myscene is set by scene.py
myscene = None

levity_exposition = False
levity_direction = "right"

do_sit = False

def init():
    myscene.ui.inventory.visible = True
    # gamestate.event_manager.enter_cutscene()
    myscene.actors['levity'].prepare_walkpath_move("levity_4")
    myscene.actors['levity'].next_action()
    scenehandler.soundplayer.play_track("simple.ogg")

def inga_walk(actor, point):
    if point == "inga_attempt_silver_class":
        if not myscene.ui.inventory.has_item("membership_card"):        # TODO: PLACEHOLDER CONDITION
            sneelock = myscene.actors['sneelock']
            sneelock.prepare_walkpath_move("sneelock_block")
            sneelock.next_action()
            myscene.convo.begin_conversation("you_shall_not_pass")
    if re.match("seat_\d+", point) and do_sit:
        myscene.actors['main'].current_state = "sit"
            
def inga_sit(seat):
    inga = myscene.actors['main']
    inga.prepare_walkpath_move(seat.identifier)
    inga.next_action()
    do_sit = True
    
#TODO: Find a more pythonic way to do some of this...
def levity_walk(actor, point):
    print "Walk handler called..."
    global levity_exposition            #gross how can we un-global this? (i.e. static local var in C)
    global levity_direction
    levity = myscene.actors['levity']
    next_point = point
    if point == "levity_left" or point == "levity_right":   
        if point == "levity_left":
            levity_direction = "right"
            next_point = "levity_1"
        elif point == "levity_right":
            levity_direction = "left"
            next_point = "levity_4"
        #levity.prepare_walkpath_move(next_point)
        #pyglet.clock.schedule_once(levity.prepare_walkpath_move(next_point), 25)
        pyglet.clock.schedule_once(levity.next_action, 26)
        
    else:
        if point == "levity_1":
            next_point = "levity_2" if levity_direction == "right" else "levity_left"
        elif point == "levity_2":
            next_point = "levity_3" if levity_direction == "right" else "levity_1"
        elif point == "levity_3":
            next_point = "levity_4" if levity_direction == "right" else "levity_2"
        elif point == "levity_4":
            if levity_exposition is False:
                levity_exposition = True
                #begin convo
                actor.update_state("stand_right")
                myscene.begin_conversation("introduction")
            else:
                next_point = "levity_right" if levity_direction == "right" else "levity_3"
        
        if next_point is not point:    
            levity.prepare_walkpath_move(next_point)
    print "Moving from %s to %s..." % (point, next_point)

def end_conversation(convo_name):
    if convo_name == "introduction":
        # Create the items to be given to Inga
    #     nuts = actor.Actor("tasty_nuts", "tasty_nuts", scene = myscene, attrs = {'start_state': 'tasty_nuts'})
    #     myscene.add_actor(nuts)
    #     myscene.ui.inventory.put_item(nuts)
    #     
    #     lemonade = actor.Actor("lemonade", "lemonade", scene = myscene, attrs = {'start_state': 'lemonade'})
    #     myscene.add_actor(lemonade)
    #     myscene.ui.inventory.put_item(lemonade)
    #     
    #     myscene.begin_conversation("introduction_continued")
    #     myscene.begin_background_conversation("mumblestiltskin")
    # if convo_name == "introduction_continued":
        #Set levity to do her walk around the level
        myscene.actors['levity'].prepare_walkpath_move("levity_right")
        myscene.actors['levity'].next_action()
        # gamestate.event_manager.exit_cutscene()

def talk_to_briggs():
    #myscene.end_background_conversation('mumblestiltskin')
    myscene.begin_conversation("briggs_exposition")

walk_handlers = {
    'main': inga_walk,
    'levity': levity_walk
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
    print clicked_actor
    if re.match("seat_\d+", clicked_actor.identifier) and clicked_actor.current_state == "couch":
        myscene.ui.show_cam(clicked_actor, {'Sit': lambda: inga_sit(clicked_actor) })
    if clicked_actor.identifier == "gregg_briggs":
        #show a CAM with options
        myscene.ui.show_cam(clicked_actor, {'Greet the Odd Fellow': talk_to_briggs, 'Avoid Eye Contact': None})
    if clicked_actor.identifier == "tourist":
        myscene.begin_conversation("meet_the_tourists")
    if clicked_actor.identifier == "vladimir" or clicked_actor.identifier == "petro" or clicked_actor.identifier == "nikolai":
        myscene.begin_conversation("making_connections")
    if clicked_actor.identifier == "shamus":
        myscene.begin_conversation("a_young_irish_boy")
