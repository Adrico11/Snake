# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:40:10 2020

@author: snice
"""

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
#import sys

#pygame.init()


class cube(object):
    rows = 20
    w = 500
    
    def __init__(self,start,dirnx=1,dirny=0,color=(0,255,0)): #dirnx and dinrny are optional parameters which have default values
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def move(self,dirnx,dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self,surface,eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface,self.color,(i*dis+1,j*dis+1,dis-2,dis-2)) #on dessine le cube (petits offsets pour pas cacher les lines de la grille)
        
        if eyes: # Draws the eyes
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
    
class snake(object):
    body=[]
    turns={}
    
    def __init__(self,color,pos):
        self.color=color
        self.head=cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
    
    def move(self):
       for event in pygame.event.get(): #Tous les evts possibles
           if event.type == pygame.QUIT:
               pygame.quit()
               #sys.exit()
           keys = pygame.key.get_pressed()   #Dico de toutes les keys avec un booléen qui indique si elles sont appuyées ou non 
           #print(keys)
           for key in keys:
               
               if keys[pygame.K_LEFT]:
                   self.dirnx = -1
                   self.dirny = 0
                   #Dico qui assigne la direction prise en la position de la tête du snake (ie où il a tourné)
                   self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] 
               
               elif keys[pygame.K_RIGHT]: #elif to avoid multiple keys pressed at the same time
                   self.dirnx = 1
                   self.dirny = 0
                   self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] 
                   
               elif keys[pygame.K_UP]: 
                   self.dirnx = 0
                   self.dirny = -1
                   self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] 
               
               elif keys[pygame.K_DOWN]:  
                   self.dirnx = 0
                   self.dirny = 1
                   self.turns[self.head.pos[:]] = [self.dirnx,self.dirny] 
    
           for i,c in enumerate(self.body): #list of cubes
               p = c.pos[:] #position of a cube
               if p in self.turns: #if we turn at this position
                   turn = self.turns[p] 
                   c.move(turn[0],turn[1]) #cube moves accordingly (dirnx and dirny)
                   if i == len(self.body)-1: #if we have just turned the last cube of the snake body
                       self.turns.pop(p) #we don't need to worry about this turn anymore so we pop it
               else: #we still have to move the snake even if it is not turning
                   if c.dirnx == -1 and c.pos[0] <=0 : c.pos = (c.rows-1,c.pos[1]) #pacman style moving (come back in through the other side of screen)
                   elif c.dirnx == 1 and c.pos[0] >= c.rows-1 : c.pos = (0,c.pos[1])
                   elif c.dirny == 1 and c.pos[1] >= c.rows-1 : c.pos = (c.pos[0],0)
                   elif c.dirny == -1 and c.pos[1] <=0 : c.pos = (c.pos[0],c.rows-1)
                   else: c.move(c.dirnx,c.dirny) #otherwise move normally
    
    def reset(self,pos): #close to init function
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1 
    
    def addCube(self):
        tail = self.body[-1]
        dx,dy = tail.dirnx,tail.dirny
        
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
        
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
    
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0: #if we are dealing with the head of the snake
                c.draw(surface,True) #add little eyes
            else:
                c.draw(surface) #draw normally the other cubes
 
    

    
def drawGrid(w,rows,surface):
    sizeBtw = w//rows
    x = 0
    y = 0
    for l in range(rows):
        x += sizeBtw
        y += sizeBtw
        pygame.draw.line(surface,(255,255,255),(x,0),(x,w)) #Lignes verticales
        pygame.draw.line(surface,(255,255,255),(0,y),(w,y)) #Lignes horizontales
      

def redrawWindow(surface):
    global rows,width,s, snack
    surface.fill((0,0,0)) #Mettre un fond noir
    s.draw(surface) #draws the snake on the screen
    snack.draw(surface)
    drawGrid(width,rows,surface) #Pas besoin de référencer ces variables car elles sont globales
    pygame.display.update() #Toujours update le display à chaque changement
    

def randomSnack(rows,item):
    positions = item.body
    while True : 
        x = random.randrange(rows)
        y = random.randrange(rows)
        #Liste de filtrée de positions qui ne garde qu'un élément du corps du snake si celui-ci est au même endroit que le snack 
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: 
            continue #we need to generate another position for the snack
        else:
            break
    return (x,y)    
            
def message_box(subject,content):
    root = tk.Tk() #new window
    root.attributes("-topmost", True) #comes out on top
    root.withdraw() #makes the box visible
    messagebox.showinfo(subject,content)
    try: #essaye de détruire messagebox jusqu'à ce que l'utilisateur appiue sur la croix t la ca ferme la box
        root.destroy() 
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    #On crée la fenêtre de jeu
    win = pygame.display.set_mode((width,width))
    s = snake((0,255,0),(10,10))
    snack = cube(randomSnack(rows,s), color =(255,0,0))
    flag = True
    
    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(50) #Pour que le jeu ne s'execute pas trop vite
        clock.tick(10) #max 10 fps sur le jeu
        s.move()
        if s.body[0].pos == snack.pos: #if snake eats the snack
            s.addCube()
            snack = cube(randomSnack(rows,s),color=(255,0,0))
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])): #on check si une partie du snake est à la même pos que ce qui suit (collision)
                print('Score: ',len(s.body)) #pas besoin du + si on met une virgule à la place
                message_box('You Lost !', 'Play again ?')
                s.reset((10,10))
                break
        
        redrawWindow(win)
        
main()        