import tkinter as tk
import pygame
import random
import time
import pdb

class EtudeSpaceInvaders(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.can = tk.Canvas(self, width=1920, height=1080, background='black')
        self.can.pack()
        self.photo_fond = tk.PhotoImage(file="/home/fab/mes_scripts/space_invaders/image_fond.png")
        self.image_fond = self.can.create_image(0,0,anchor='nw',
                                                image=self.photo_fond)
        self.point_score = 0 
        self.affiche_score = self.can.create_text(1700,0,
                                                  text="Score: "+
                                                  str(self.point_score),
                                                  font=("Courrier",20,'bold'),
                                                  anchor='nw',fill="red",tag=99)
        self.vie = 10
        self.affiche_vie = self.can.create_text(1300,0,
                                                  text="Vie: "+
                                                  str(self.vie),
                                                  font=("Courrier",20,'bold'),
                                                  anchor='nw',fill="red",tag="vie")
        self.compt_bruitage = 0
        
        self.flag_laser = True #utilisé pour gérer bug tir similtanné
        self.projectile = True #
        self.level = 1
        self.gagne_level = False
        self.ligne_y = 760 #utilisé dans level2 ---> projectile_ovni()
        self.liste_item=[]
        ####
        self.bonus = pygame.mixer.Sound(
            '/home/fab/mes_scripts/space_invaders/345299__scrampunk__okay.wav')
        
        self.explosion_ovni =pygame.mixer.Sound(
            '/home/fab/mes_scripts/space_invaders/shipexplosion.wav')
        
        self.fin_de_partie = pygame.mixer.Sound('/home/fab/mes_scripts/space_invaders/fin_de_partie.wav')

        self.son_laser = pygame.mixer.Sound(
            '/home/fab/mes_scripts/space_invaders/shoot.wav')
        self.son0 = pygame.mixer.Sound(
            '/home/fab/mes_scripts/space_invaders/0.wav')
        self.son1 = pygame.mixer.Sound(
            '/home/fab/mes_scripts/space_invaders/1.wav')
        self.son2 = pygame.mixer.Sound(
            '/home/fab/mes_scripts/space_invaders/2.wav')
        self.son3= pygame.mixer.Sound(
            '/home/fab/mes_scripts/space_invaders/3.wav')   
        self.win = pygame.mixer.Sound(
            '/home/fab/mes_scripts/space_invaders/win.wav')
        ####        
        
        #self.flag_perdu = False
        self.image_id= dict()
        self.photo_ovni = dict()
        self.dx = 2  
        self.dy = 0
        self.dx_truc1 = 2
        self.dx_truc2 = -2
        self.dx_truc3 = 2
        self.occupe = False
        self.vitesse_bruitage = 500
        self.vitesse_ovni = 40
        
        
    def bruitage(self):
        """  Gére le bruitage des ovni (truc) """
        if self.compt_bruitage == 0:
            self.son0.play()
            self.compt_bruitage = 1
        elif self.compt_bruitage == 1:
            self.son1.play()
            self.compt_bruitage = 2
        elif self.compt_bruitage == 2:
            self.son2.play()
            self.compt_bruitage = 3
        elif self.compt_bruitage == 3:
            self.son3.play()
            self.compt_bruitage = 0
        self.callback_bruitage = self.after(self.vitesse_bruitage, self.bruitage)
 
    def deplacetag(self,etiquette):
        self.can.move(etiquette, self.dx, self.dy)
        
    def detruit(self):
        self.occupe = True
        while self.liste_item:
            item = self.liste_item.pop()
            print('self item in detruit()', item)
            x, y = self.can.coords(item)
            #print('x',x,'y',y)
        
            if item in self.can.find_withtag("truc"):
                self.photo1 = self.init_ovni("/home/fab/mes_scripts/space_invaders/explosion.png",
                                   999, x, y-10,"truc")
                self.can.delete(item)
                self.score(10)
                
                
            elif item in self.can.find_withtag("tir_ov"):
                self.photo1 = self.init_ovni("/home/fab/mes_scripts/space_invaders/explosion.png",
                                   999, x-40, y-10,"tir_ov")
                #self.can.delete(item)
                self.can.delete("tir_ov")
                self.score(50)
                print('flag tir_ov True')
                self.flag_projectile = True
                pygame.mixer.stop()
                self.bonus.play()
                return 9999 #?
                
            elif item in self.can.find_withtag("vaisseau_humain"):
                self.photo1 = self.init_ovni("/home/fab/mes_scripts/space_invaders/explosion.png",
                                   999, x, y-10,"vaisseau_humain")
                self.can.delete(item)
                self.vie -=1
        
        self.after(70, self.efface_explosion)
                     
    def efface_explosion(self):
        self.can.delete(self.image_id[999])
        self.occupe = False
    def eteint_laser(self):
        self.can.delete(self.laser)
        self.after(300,self.fl)
    def fl(self):
        self.flag_laser = True
        
    def evenement(self):
        self.bind("<KeyPress-w>",
                  lambda gauche: self.can.move("vaisseau_humain", -4, 0))
        
        self.bind("<KeyRelease-w>",
                  lambda gauche:self.can.move("vaisseau_humain", -4, 0))
        
        self.bind("<KeyPress-b>",lambda droite:
                  self.can.move("vaisseau_humain", 4, 0))
        
        self.bind("<KeyRelease-b>",lambda droite:
                  self.can.move("vaisseau_humain", 4, 0))
        
        self.bind("<KeyRelease-c>",self.tir)
    def gagne(self):
        
        self.after_cancel(self.callback_bruitage)
        self.tu_gagnes = self.can.create_text(960,440,text="Tu gagnes!",
                                         font=("Courrier",100,'bold'),
                                         anchor='center',fill="red")
        self.update()
        time.sleep(2)
        self.win.play()
        time.sleep(5)
        self.can.delete(self.tu_gagnes)
        
    def init_ovni(self, image_path, indice_ovni, x_init, y_init,etiquette):
        self.photo_ovni[indice_ovni] = tk.PhotoImage(file=image_path)
        self.image_id[indice_ovni] = self.can.create_image(x_init,
                        y_init,anchor='nw',image=self.photo_ovni[indice_ovni],
                                                            tags=etiquette)
        
    def initialise_level(self):
        self.can.delete("truc")
        self.can.delete("vaisseau_humain")
        self.can.delete("tir_ov")
        self.liste_item = []
        self.can.delete(self.image_id[999])#explosion
        self.flag_projectile = True
        print('flag projectile True 1')
         
        vaisseau = self.init_vaisseau_humain("/home/fab/Images/vaisseau.png",
                                 "a", 900, 900, "vaisseau_humain")

        indice = 1
        x = 300
        for i in range(10):
            """crée 10 invaders sur deux lignes.
            1er ligne --->indice, 2 lignes --->indice+100"""
            photo1 = self.init_ovni("/home/fab/Images/Invaders2.png",
                                   indice, x, 60, "truc1")
            
            
            photo2 = self.init_ovni("/home/fab/Images/Invaders2.png",
                                   indice+100, x, 160, "truc2")
            photo3 = self.init_ovni("/home/fab/Images/Invaders2.png",
                                   indice+200, x, 260, "truc3")
            self.can.addtag_withtag("truc","truc1")
            self.can.addtag_withtag("truc","truc2")
            self.can.addtag_withtag("truc","truc3")
            x += 120
            indice +=1
            
    def init_vaisseau_humain(self,image_path, indice, x_init, y_init,etiq):
        """ note le vaisseau fait 94 pixels de largeur """
        self.photo_vaisseau_humain = tk.PhotoImage(file=image_path)
        self.image_id[indice] = self.can.create_image(x_init,
                        y_init,anchor='n',image=self.photo_vaisseau_humain,
                                                            tags=etiq)
        self.evenement()

    def perdu(self):
        self.after_cancel(self.callback_bruitage)
        self.fin_de_partie.play()
        self.tu_perds = self.can.create_text(960,440,text="Les envahisseurs gagnent!",
                                         font=("Courrier",90,'bold'),
                                         anchor='center',fill="red")
        pdb.set_trace()
        self.update()
        time.sleep(5)
        self.can.delete(self.tu_perds)
    
        if self.vie and self.level == 1:
            self.can.delete("truc")
            self.can.itemconfigure(self.affiche_vie, text="Vie: "+str(self.vie))

            self.initialise_level()
            
            return 9999 
        if self.vie and self.level == 2:
            self.can.itemconfigure(self.affiche_vie, text="Vie: "+str(self.vie))
            self.initialise_level()
            return 9999 #code
    def score(self,score):
        self.point_score += score
        #print(self.point_score)
        self.can.itemconfigure(self.affiche_score, text=
                               "Score: "+str(self.point_score))

    def set_directions(self, dx, dy):
        self.dx = dx
        self.dy = dy
    
    def tir(self,event):
        
        #le flag_laser gere le bug du tir sur le tir
        if self.flag_laser:
            self.flag_laser = False
            self.son_laser.play()
            self.after(40, self.tir_suite)
           
    def tir_suite(self):
        """ tir suite et mis en place pour gérer
            le décalage entre le son et l'image"""
        x, y = self.can.coords("vaisseau_humain")
        #print('coord vaisseau humain', x, y)
        ligne_y = 760
        # test si ovni présent sur ligne 760,660,560 ... ect
        for i in range(8):
            a = self.can.find_overlapping(x , ligne_y+2, x+2, ligne_y+20)

            item = [ i for i in a ]
            
            item.remove(1) # la valeur 1 correspond au fond
            #print('item',item)

            
            if item:
                print("item explosion",item)
                self.explosion_ovni.play()
                self.liste_item.append(item[0])
                self.after(40,self.detruit)
                break
            ligne_y -= 100
        
        #création laser
        self.laser = self.can.create_line(x,ligne_y+65,x,900,fill='red',
                                            dash=40,width=4,tags='laser')
        self.update()
        self.after(15, self.eteint_laser)
        

        ######## Level 1 #########
    def level1(self):
        if im.can.bbox('truc') is None:
            self.gagne()
            self.initialise_level()
            
            self.after_cancel(self.callback_level1)
            self.level2()
            return
        
        self.deplacetag("truc")
        x, y, x1, y2 = self.can.bbox('truc')
                
        if x1 > 1840:
            self.dx = -1 * self.dx
            self.set_directions(self.dx,100)
            self.deplacetag("truc")
            
        self.set_directions(self.dx,0)
        #test si perdu
        
        for i in self.can.find_withtag("truc"):
            if i in self.can.find_overlapping(0 , 900, 1920, 950):
                self.perdu()            
        
        if x < 60:
            self.dx = -1 * self.dx
            self.set_directions(self.dx,100)

        self.callback_level1 = self.after(40, self.level1)
    
        
        
####### Level2 ##############################
    def level2(self):   
        if im.can.bbox('truc') is None:
            self.gagne()
            self.initialise_level()
            
            self.after_cancel(self.callback_level2)
        
            self.level3()
            return
            #self.destroy()
        
        print('boucle2')
        self.deplacetag("truc")
        x, y, x1, y2 = self.can.bbox('truc')
        if x1 > 1840:
            self.dx = -1 * self.dx
            self.set_directions(self.dx,100)
            self.deplacetag("truc")
            if self.flag_projectile:
                self.projectile_ovni() 
        self.set_directions(self.dx,0)

         
         
        #test si perdu
        for i in self.can.find_withtag("truc"):
            if i in self.can.find_overlapping(0 , 900, 1920, 950):
                perdu = self.perdu()
                if perdu == 9999: #retour perdu
                    break
                
        if x < 60:
            self.dx = -1 * self.dx
            self.set_directions(self.dx,100)
            if self.flag_projectile:
                self.projectile_ovni()
        
        self.callback_level2 = self.after(40, self.level2)


############### Level3 #########################

    def level3(self):
        
        #test si gagné
        if im.can.bbox('truc') is None:
            self.gagne()
            self.initialise_level()
            
            self.after_cancel(self.callback_level3)
        
            self.level3()
            return
            #self.destroy()
        #test si touché: Essai à enlever
        if not self.flag_projectile:
            a, b, c, d = self.can.bbox("tir_ov")
            print('coords tir_ov: ',self.can.coords('tir_ov'))
            print('if vaisseau_h',self.can.find_withtag('vaisseau_humain'),
                  'dans ',self.can.find_overlapping(a, b, c , d))
            if self.can.find_withtag('vaisseau_humain')[0] in self.can.find_overlapping(a, b, c , d):
                self.liste_item.append(self.can.find_withtag('vaisseau_humain')[0])
                print ('a,b,c,d',a, b, c, d)
                print ('vaisseau ; x,y,x1,y1 vaisseau', self.can.bbox('vaisseau_humain')) 
                print('self flag_projectile',self.flag_projectile)
                self.detruit()
                self.perdu()
            
        #test si perdu
        for i in self.can.find_withtag("truc"):
            if i in self.can.find_overlapping(0 , 900, 1920, 950):
                print('test si perdu dans level3')
                
                perdu = self.perdu()
                if perdu == 9999: #retour perdu
                    break
##                
##        print('boucle3')
##        print('dx_truc1', self.dx_truc1)
##        print('dx_truc2: ', self.dx_truc2)
##        print('dx_truc3: ', self.dx_truc3)
        self.set_directions(self.dx_truc1,0)
        self.deplacetag("truc1")
        self.set_directions(self.dx_truc2,0)
        self.deplacetag("truc2")
        self.set_directions(self.dx_truc3,0)
        self.deplacetag("truc3")

        #test extrémité truc1
        if self.can.bbox('truc1') is None:
            pass
        else:
            x1, y1, x1_2, y1_2 = self.can.bbox('truc1')
            if x1_2 > 1840 or x1 < 60:
                self.dx_truc1 = -1 * self.dx_truc1
                self.set_directions(self.dx_truc1,100)
                self.deplacetag("truc1")
                if self.flag_projectile:
                    retour = self.projectile_ovni()
                    if retour == 777:
                        
                        self.detruit()
                        self.perdu()
                        
        
        if self.can.bbox('truc2') is None:
            pass
        else:
            x2, y2, x2_2, y2_2 = self.can.bbox('truc2')
            if x2_2 > 1840 or x2 < 60:
                self.dx_truc2 = -1 * self.dx_truc2
                self.set_directions(self.dx_truc2,100)
                self.deplacetag("truc2")
                if self.flag_projectile:
                    self.projectile_ovni() 
        if self.can.bbox('truc3') is None:
            pass
        else:   
            x3, y3, x3_2, y3_2 = self.can.bbox('truc3')
            if x3_2 > 1840 or x3 < 60:
                self.dx_truc3 = -1 * self.dx_truc3
                self.set_directions(self.dx_truc3,100)
                self.deplacetag("truc3")
                print ( 'self.dx_truc3 in if x3_2 >1840 :',self.dx_truc3) 
                if self.flag_projectile:
                    self.projectile_ovni()
            
        self.callback_level3 = self.after(20, self.level3)

    def projectile_ovni(self):
        """ projectile_ovni gère les projectibles tirer par les ovnis.
            l'ovni choisi est aléatoire...""" 
        
        self.flag_projectile = False
        print('flag projectile False 1')
        # test si ovni présent sur ligne 760,660,560 ... ect
        for i in range(7):#passé de 8 à 7 pour voir si plus de bug
            a = self.can.find_overlapping(1 , self.ligne_y-60,
                                          1980, self.ligne_y+2)#+50 MODIFIÉ EN +2
            item = [ i for i in a ]
            item.remove(1) # la valeur 1 correspond au fond
            #print('liste= ',item)
            #recherche si dans item il y a laser
            laser = self.can.find_withtag('laser')
            if laser in item:
                item.remove(laser[0])
            if item:
                
                self.item_tir_ov = random.choice(item)
                x, y, x1, self.y2 = self.can.bbox(self.item_tir_ov)
                self.x_projectile_ovni = x + int((x1 - x)/2)
                self.compteur_projectile_ovni_suite = 1000 - self.y2 #VALEUR 1040 MODOFIÉ EN 1000
                self.dessin_projectile_ovni = tk.PhotoImage(
                    file="/home/fab/mes_scripts/space_invaders/tir_ovni.png")
                self.image_id[10000] = self.can.create_image(self.x_projectile_ovni,
                                                             self.y2,anchor='center',
                                                             image=self.dessin_projectile_ovni,
                                                             tags="tir_ov")
                self.projectile_ovni_suite()
                
                break
            else:
                self.ligne_y -= 100
                if self.ligne_y < 60:
                    self.ligne_y = 760
                    
    def projectile_ovni_suite(self):
        """ gestion du mouvement du projectile de l'ovni.
            Test contact avec vaisseau"""
        
            
        if self.flag_projectile: # si vrai c'est que tir_obj detruit (voir detruit())
            return 

##        #test si touché:
##        
##        a, b, c, d = self.can.bbox("tir_ov")
##        print('coords tir_ov: ',self.can.coords('tir_ov'))
##        print('if vaisseau_h',self.can.find_withtag('vaisseau_humain'),
##              'dans ',self.can.find_overlapping(a, b, c , d))
##        if self.can.find_withtag('vaisseau_humain')[0] in self.can.find_overlapping(a, b, c , d):
##            self.liste_item.append(self.can.find_withtag('vaisseau_humain')[0])
##            print ('a,b,c,d',a, b, c, d)
##            print ('vaisseau ; x,y,x1,y1 vaisseau', self.can.bbox('vaisseau_humain')) 
##            print('self flag_projectile',self.flag_projectile)
##            self.detruit()
##            self.perdu()
##        
        self.ligne_y = 760
        self.compteur_projectile_ovni_suite -= 1
        self.y2 +=1
        if self.compteur_projectile_ovni_suite:
            self.can.move("tir_ov",0,2)
            self.after(20,self.projectile_ovni_suite)
        else:
            self.can.delete('tir_ov')
            self.flag_projectile = True
    
    
        
        
################################################""        
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    im = EtudeSpaceInvaders()
    
    vaisseau = im.init_vaisseau_humain("/home/fab/Images/vaisseau.png",
                             "a", 900, 900, "vaisseau_humain")

    indice = 1
    x = 300
    fin_de_partie = pygame.mixer.Sound('/home/fab/mes_scripts/space_invaders/fin_de_partie.wav')
    fin_de_partie.play()
    
    for i in range(10):
        """crée 10 invaders sur deux lignes.
        1er ligne --->indice, 2 lignes --->indice+100"""
        photo1 = im.init_ovni("/home/fab/Images/Invaders2.png",
                               indice, x, 60, "truc")
        
        
        photo2 = im.init_ovni("/home/fab/Images/Invaders2.png",
                               indice+100, x, 160, "truc")
        photo3 = im.init_ovni("/home/fab/Images/Invaders2.png",
                               indice+200, x, 260, "truc")
        x += 120
        indice +=1
    im.set_directions(2,0)
    im.bruitage ()
    im.level1()
    print('niveau3')
    im.mainloop()

        
    

