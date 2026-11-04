# -*- coding: utf-8 -*-
import json, re, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "stories")
PAL = ["violet", "bleu", "rouge", "vert"]; OUTF = [(164,132,214),(214,150,132),(132,190,214),(190,214,132),(214,196,132)]
VAR = [
 (["OUVRIR LA PORTE","FAIRE SEMBLANT DE DORMIR"], "Tu *ouvres*... ou tu fais semblant de *dormir* ?", "Cette fois, tu fais semblant de *dormir*."),
 (["OUVRIR LA PORTE","RESTER IMMOBILE"], "Tu *ouvres*... ou tu restes *immobile* ?", "Cette fois, tu restes *immobile*."),
 (["OUVRIR LA PORTE","ÉTEINDRE LE TÉLÉPHONE"], "Tu *ouvres*... ou tu *éteins* ton téléphone ?", "Cette fois, tu *éteins* ton téléphone."),
 (["OUVRIR LA PORTE","SOUS LA COUVERTURE"], "Tu *ouvres*... ou tu te caches *sous la couverture* ?", "Cette fois, tu te caches *sous la couverture*."),
]
KNOCKS = ["*Trois coups*. À ta porte.", "Trois *coups*. Lents.", "Trois coups... *sur ta porte*."]
LEAVE = ["Les coups *s'arrêtent*.", "Les pas *s'éloignent*.", "Le silence *revient*.", "La lumière sous la porte *s'éteint*."]
CTA0 = ["Alors... tu *ouvres* ? Ou tu te *caches* ?", "Et toi... tu *ouvres* ? Ou tu te *caches* ?", "Dis-moi... tu *ouvres* ? Ou tu te *caches* ?"]
CTAT = [["TU FAIS QUEL", "CHOIX ?"], ["TU OUVRES", "OU PAS ?"], ["ET TOI", "TU FAIS ?"]]
SCARE_DEF = "Merci d'avoir *ouvert*."
TAGS = "#horreur #creepy #histoirequifaitpeur #suspense #fyp"
D = []
def st(plate, hp, dp, h0, h1, hc, ev, ep, g, intro, rules, voice, who, contra, gen, scare, twist, end, cap):
    D.append(dict(plate=plate, hp=hp, dp=dp, h0=h0, h1=h1, hc=hc, ev=ev, ep=ep, g=g, intro=intro, rules=rules, voice=voice, who=who, contra=contra, gen=gen, scare=scare or SCARE_DEF, twist=twist, end=end, cap=cap))

st("4C","SÉJOUR","PALIER","Écoute.","Il est *deux heures* du matin.","02:05:10","02:40:00","Deux heures *quarante*.",("Coloc du 4e","3 membres · 2 en ligne","Maxime"),"Un message de *Maxime*, ton colocataire.",
   [("Je rentre à 4h, pas avant.","Je rentre à quatre heures. *Pas avant*."),("Ne laisse entrer personne.","Ne laisse entrer *personne*."),("Même si ça me ressemble.","Même si ça *me ressemble*.")],
   "C'est *Maxime*... j'ai oublié mes clés.","Ton colocataire.",("Maxime","Je suis encore au resto avec Inès.","Mais il vient d'écrire : il est *encore au restaurant*."),"il","Merci de m'avoir *laissé* entrer.",
   ("Inès","Maxime est avec moi depuis ce soir.","*Inès* t'écrit : Maxime est *avec elle*."),("Alors... *qui* t'appelait par ton prénom ?","Dans le *placard*."),"Maxime frappe à ta porte... mais Maxime est ailleurs.")
st("12","SALON","ENTRÉE","Imagine.","Il est *une heure* du matin.","01:02:40","01:30:00","Une heure *trente*.",("Famille","Maman, Papa et toi","Maman"),"Un message de *maman*.",
   [("On dort chez tata ce soir.","On dort *chez tata* ce soir."),("Verrouille bien la porte.","Verrouille *bien* la porte."),("Si on sonne, ce n'est pas nous.","Si on sonne... ce n'est *pas nous*.")],
   "C'est *maman*... ouvre, il fait froid.","Ta mère.",("Maman","On est chez tata, on dort déjà.","Mais elle vient d'écrire : elle *dort* chez tata."),"elle","Je suis *rentrée*.",
   ("Maman","Quelqu'un a pris ma voix. Ne réponds plus.","*Maman* t'écrit : quelqu'un a pris *sa voix*."),("Alors... *qui* te répondait ?","Elle est *dans* le placard."),"Maman frappe à ta porte... mais maman dort chez tata.")
st("204","SUITE","COULOIR","Ce soir.","Il est *deux heures* du matin.","02:01:30","02:15:00","Deux heures *quinze*.",("Réception","Hôtel Beau Rivage","Réception"),"Un message de la *réception*.",
   [("Maintenance du couloir à 02h15.","Maintenance du couloir, à *deux heures quinze*."),("Merci de rester dans votre chambre.","Restez *dans votre chambre*."),("Nous ne frappons jamais.","Nous ne frappons *jamais*.")],
   "Service d'étage... *ouvrez*, s'il vous plaît.","Le service d'étage.",("Réception","Aucun service d'étage cette nuit.","Mais la réception écrit : aucun service d'étage *cette nuit*."),"il","Votre *chambre* est prête.",
   ("Réception","La chambre 204 est inoccupée depuis hier.","La *réception* t'écrit : cette chambre est *inoccupée*. Depuis hier."),("Alors... *qui* dort dans cette chambre ?","Derrière *toi*."),"Le service d'étage n'existe pas cette nuit.")
st("9","SALON","PALIER","Écoute.","Il est *trois heures* du matin.","03:03:03","03:33:00","Trois heures *trente-trois*.",("Karim · Hôte","Séjour de trois nuits","Karim"),"Un message de *Karim*, ton hôte.",
   [("Je suis parti à l'aéroport.","Je suis *parti* à l'aéroport."),("Je suis le seul à avoir la clé.","Je suis le *seul* à avoir la clé."),("Si on sonne, n'ouvre pas.","Si on sonne... n'ouvre *pas*.")],
   "C'est *Karim*... j'ai oublié mon sac.","Ton hôte.",("Karim","Mon vol décolle dans dix minutes.","Mais il vient d'écrire : son vol *décolle*."),"il","Merci pour *l'hospitalité*.",
   ("Karim","Il y a quelqu'un d'autre dans le logement ?","*Karim* demande : il y a *quelqu'un d'autre* dans le logement ?"),("Alors... *qui* a la clé ?","Dans le *placard*."),"Tu es seul dans le logement. Vraiment ?")
st("B214","STUDIO","COULOIR","Imagine.","Il est *minuit* moins huit.","23:52:10","00:00:00","Minuit *pile*.",("Cité U · Bâtiment B","Étage deux · 40 résidents","Surveillant"),"Un message du *surveillant*.",
   [("Couvre-feu à minuit.","*Couvre-feu* à minuit."),("Les couloirs sont fermés.","Les couloirs sont *fermés*."),("Personne ne passe cette nuit.","*Personne* ne passe cette nuit.")],
   "C'est le *surveillant*... contrôle de chambre.","Le surveillant.",("Surveillant","Je suis en congé jusqu'à lundi.","Mais lui écrit : il est *en congé* jusqu'à lundi."),"il","Contrôle *terminé*.",
   ("Camille","Quelqu'un attend dans le couloir depuis une heure.","*Camille* t'écrit : quelqu'un *attend* dans le couloir depuis une heure."),("Alors... *qui* te surveille ?","Derrière *toi*."),"Le surveillant est en congé. Alors qui frappe ?")
st("5A","SALON","PALIER","Écoute.","Il est *deux heures* du matin.","02:10:20","02:50:00","Deux heures *cinquante*.",("Madame Roche","Voisine du dessus","Mme Roche"),"Un message de *Madame Roche*, ta voisine.",
   [("J'ai entendu du bruit au grenier.","J'ai entendu du bruit *au grenier*."),("Ne monte pas.","Ne monte *pas*."),("Si je t'appelle, ne viens pas.","Si je t'appelle... ne viens *pas*.")],
   "C'est *Madame Roche*... aide-moi, je suis tombée.","Ta voisine du dessus.",("Mme Roche","Je suis chez ma fille à Lyon.","Mais elle écrit : elle est *chez sa fille*. À Lyon."),"elle","Merci de *monter*.",
   ("Mme Roche","Ce n'était pas du bruit. C'étaient des pas.","*Madame Roche* t'écrit : ce n'était pas du bruit. C'étaient *des pas*."),("Alors... *qui* marche au-dessus de toi ?","Dans le *placard*."),"Madame Roche appelle à l'aide... depuis Lyon.")
st("7","APPARTEMENT","PALIER","Ce soir.","Il est *une heure* du matin.","01:12:00","01:45:00","Une heure *quarante-cinq*.",("Alerte Quartier","Mairie · 820 abonnés","Mairie"),"Une alerte de la *mairie*.",
   [("Un individu a été signalé dans la rue.","Un individu a été signalé *dans la rue*."),("Ne répondez à aucun inconnu.","Ne répondez à *aucun inconnu*."),("Même s'il se dit policier.","Même s'il se dit *policier*.")],
   "*Police*... ouvrez la porte.","La police.",("Mairie","Aucune patrouille ce soir.","Mais la mairie vient d'écrire : aucune *patrouille* ce soir."),"il","Merci de *coopérer*.",
   ("Mairie","L'individu est maintenant dans l'immeuble.","La *mairie* t'écrit : l'individu est maintenant *dans l'immeuble*."),("Alors... *qui* était à ta porte ?","Derrière *toi*."),"Il se dit policier. La mairie dit le contraire.")
st("3A","SÉJOUR","ENTRÉE","Imagine.","Il est *minuit* et demi.","00:23:40","00:30:00","Minuit *trente*.",("Lucas","Ton frère","Lucas"),"Un message de *Lucas*, ton frère.",
   [("Je dors chez Théo ce soir.","Je dors *chez Théo* ce soir."),("Ne m'attends pas.","Ne m'attends *pas*."),("Si je frappe, ne réponds pas.","Si je frappe... ne réponds *pas*.")],
   "C'est *moi*... Lucas. Ouvre-moi.","Ton frère.",("Lucas","Je suis déjà couché chez Théo.","Mais il vient d'écrire : il est *déjà couché*. Chez Théo."),"il","Je t'ai *trouvé*.",
   ("Lucas","Quelqu'un a répondu à ma place dans le couloir.","*Lucas* t'écrit : quelqu'un a répondu *à sa place*."),("Alors... *qui* parlait avec sa voix ?","Dans le *placard*."),"Ton frère frappe. Ton frère dort ailleurs.")
st("11","SALON","PALIER","Écoute.","Il est *trois heures* du matin.","03:00:10","03:20:00","Trois heures *vingt*.",("Immeuble B","18 voisins","Gardien"),"Un message du *gardien*.",
   [("Ne montez pas au dernier étage.","Ne montez pas au *dernier étage*."),("Ne descendez pas au sous-sol.","Ne descendez pas *au sous-sol*."),("Restez à votre étage.","Restez *à votre étage*.")],
   "C'est le *gardien*... fuite d'eau, ouvrez vite !","Le gardien.",("Gardien","Je suis à l'hôpital depuis ce soir.","Mais il écrit : il est *à l'hôpital* depuis ce soir."),"il","Merci de *descendre*.",
   ("Gardien","Je n'ai jamais travaillé de nuit.","Le *gardien* t'écrit : il n'a *jamais* travaillé de nuit."),("Alors... *qui* garde l'immeuble ?","Derrière *toi*."),"Le gardien est à l'hôpital. Quelqu'un porte sa voix.")
st("6","SALON","COULOIR","Ne bouge pas.","Il est *deux heures* du matin.","02:40:05","03:00:00","Trois heures *pile*.",("Sécurité Résidence","Alertes","Alarme"),"Une alerte de la *sécurité*.",
   [("Exercice d'évacuation à 03h00.","Exercice d'évacuation, à *trois heures*."),("Ne sortez pas de chez vous.","Ne sortez *pas* de chez vous."),("Fermez les fenêtres.","Fermez *les fenêtres*.")],
   "*Évacuation*... ouvrez, vite !","Les pompiers.",("Sécurité","Aucun incendie signalé.","Mais la sécurité écrit : aucun *incendie* signalé."),"il","Trop *tard*.",
   ("Sécurité","L'alarme a été déclenchée de l'intérieur.","La *sécurité* t'écrit : l'alarme a été déclenchée *de l'intérieur*."),("Alors... *qui* a déclenché l'alarme ?","Dans le *placard*."),"Exercice d'évacuation... qui n'existe pas.")
st("8","SALON","ENTRÉE","Imagine.","Il est *une heure* du matin.","01:11:11","01:30:00","Une heure *trente*.",("Sarah","Ton ex","Sarah"),"Un message de *Sarah*, ton ex.",
   [("Je suis partie en voyage.","Je suis *partie* en voyage."),("Je ne reviens pas.","Je ne reviens *pas*."),("Ne me réponds plus.","Ne me réponds *plus*.")],
   "C'est *Sarah*... laisse-moi entrer, s'il te plaît.","Ton ex.",("Sarah","Je suis à Lisbonne depuis hier.","Mais elle écrit : elle est *à Lisbonne*. Depuis hier."),"elle","Tu m'as *manqué*.",
   ("Sarah","Tu as toujours mes clés ?","*Sarah* demande : tu as toujours *ses clés* ?"),("Alors... *qui* a ouvert avec une clé ?","Derrière *toi*."),"Ton ex frappe à ta porte. Elle est à Lisbonne.")
st("2","SALON","ENTRÉE","Écoute.","Il est *minuit* passé.","00:06:30","00:30:00","Minuit *trente*.",("Mamie","Ta grand-mère","Mamie"),"Un message de *mamie*.",
   [("J'ai laissé une clé sous le paillasson.","J'ai laissé une clé *sous le paillasson*."),("Ne laisse entrer que moi.","Ne laisse entrer *que moi*."),("Je ne marche plus la nuit.","Je ne marche *plus* la nuit.")],
   "C'est *mamie*... j'arrive à pied.","Ta grand-mère.",("Mamie","Je suis alitée depuis ce matin.","Mais elle écrit : elle est *alitée* depuis ce matin."),"elle","Te voilà... *enfin*.",
   ("Mamie","Elle a pris ma voix. Elle a pris ma démarche.","*Mamie* t'écrit : elle a pris *sa démarche*."),("Alors... *qui* marche dans le couloir ?","Dans le *placard*."),"Mamie ne marche plus la nuit. Alors qui est à la porte ?")
st("6D","SÉJOUR","PALIER","Imagine.","Il est *deux heures* du matin.","02:00:45","02:22:00","Deux heures *vingt-deux*.",("Inès","Ta meilleure amie","Inès"),"Un message d'*Inès*.",
   [("Je rentre en taxi, ne m'attends pas.","Je rentre en taxi. Ne m'attends *pas*."),("Ma batterie est presque morte.","Ma batterie est presque *morte*."),("Si j'appelle, c'est que j'ai un souci.","Si j'appelle... c'est que j'ai *un souci*.")],
   "C'est *Inès*... ouvre, on me suit.","Ta meilleure amie.",("Inès","Je suis déjà dans mon lit.","Mais elle écrit : elle est *déjà* dans son lit."),"elle","Merci de *m'accueillir*.",
   ("Inès","Il y a quelqu'un dans ma chambre.","*Inès* t'écrit : il y a *quelqu'un* dans sa chambre."),("Alors... *qui* te suivait ?","Derrière *toi*."),"Inès demande de l'aide. Inès dort déjà.")
st("10","SALON","ENTRÉE","Ce soir.","Il est *trois heures* du matin.","03:00:50","03:14:00","Trois heures *quatorze*.",("Fibre Net","Service client","Technicien"),"Un message du *technicien*.",
   [("Intervention de nuit, panne détectée.","Intervention de nuit. *Panne* détectée."),("Ne débranchez rien.","Ne débranchez *rien*."),("Nous n'entrons jamais chez vous.","Nous n'entrons *jamais* chez vous.")],
   "Technicien de *nuit*... je dois vérifier la prise.","Le technicien.",("Technicien","Aucune intervention prévue à votre adresse.","Mais le technicien écrit : aucune *intervention* prévue chez toi."),"il","Branchement *terminé*.",
   ("Fibre Net","Le signal vient de l'intérieur de votre logement.","*Fibre Net* t'écrit : le signal vient *de chez toi*."),("Alors... *qui* est connecté ?","Dans le *placard*."),"Le technicien n'a jamais été appelé.")
st("14","SALON","PALIER","Écoute.","Il est *une heure* du matin.","01:20:20","01:50:00","Une heure *cinquante*.",("Hugo","Voisin d'en face","Hugo"),"Un message de *Hugo*, ton voisin.",
   [("Je vois de la lumière chez toi.","Je vois de la lumière *chez toi*."),("Éteins tout et ne bouge pas.","Éteins tout. Et ne bouge *pas*."),("Quelqu'un te regarde par la fenêtre.","Quelqu'un te *regarde* par la fenêtre.")],
   "C'est *Hugo*... ouvre, vite, il est là !","Ton voisin d'en face.",("Hugo","Je suis chez moi, les volets fermés.","Mais il écrit : il est *chez lui*, les volets fermés."),"il","Il est *entré*.",
   ("Hugo","Ce n'est pas ta fenêtre. C'est ton miroir.","*Hugo* t'écrit : ce n'est pas ta fenêtre. C'est *ton miroir*."),("Alors... *qui* te regardait ?","Dans le *miroir*."),"Quelqu'un te regarde par la fenêtre.")
st("3","SALON","ENTRÉE","Imagine.","Il est *une heure* du matin.","01:01:15","01:25:00","Une heure *vingt-cinq*.",("Papa","Ton père","Papa"),"Un message de *papa*.",
   [("Je rentre tard du travail.","Je rentre *tard* du travail."),("Je prendrai mes clés.","Je prendrai *mes clés*."),("Ne m'ouvre jamais.","Ne m'ouvre *jamais*.")],
   "C'est *papa*... j'ai perdu mes clés.","Ton père.",("Papa","Je suis encore au bureau.","Mais il écrit : il est *encore au bureau*."),"il","",
   ("Papa","J'arrive dans dix minutes. Quelqu'un est avec toi ?","*Papa* demande : quelqu'un est *avec toi* ?"),("Alors... *qui* est à l'intérieur ?","Derrière *toi*."),"Papa n'a pas ses clés. Papa n'est pas là.")
st("8B","APPARTEMENT","PALIER","Ce soir.","Il est *deux heures* du matin.","02:02:02","02:20:00","Deux heures *vingt*.",("Propriétaire","M. Bernard","M. Bernard"),"Un message de ton *propriétaire*.",
   [("Je passe demain midi pour l'état des lieux.","Je passe *demain midi*."),("N'ouvrez à personne avant.","N'ouvre à *personne* avant."),("J'ai gardé un double des clés.","J'ai gardé *un double* des clés.")],
   "C'est ton *propriétaire*... je viens vérifier.","Ton propriétaire.",("M. Bernard","Je suis encore à Marseille.","Mais il écrit : il est *encore à Marseille*."),"il","Je suis *chez moi*.",
   ("M. Bernard","Mon double des clés a disparu hier.","*Monsieur Bernard* t'écrit : son double des clés a *disparu*."),("Alors... *qui* a la clé ?","Dans le *placard*."),"Le propriétaire est à Marseille. Alors qui a la clé ?")
st("15","SÉJOUR","ENTRÉE","Écoute.","Il est *minuit* et demi.","00:21:00","00:50:00","Minuit *cinquante*.",("Yanis","Ton cousin","Yanis"),"Un message de *Yanis*, ton cousin.",
   [("Je dors dans la voiture.","Je dors *dans la voiture*."),("Je passerai te voir demain.","Je passerai *demain*."),("Ne sors pas me chercher.","Ne sors *pas* me chercher.")],
   "C'est *Yanis*... il pleut, laisse-moi entrer.","Ton cousin.",("Yanis","Je suis sur l'autoroute, je conduis.","Mais il écrit : il est *sur l'autoroute*."),"il","Merci pour *l'abri*.",
   ("Yanis","Je te vois depuis la route. Tu n'es pas seul.","*Yanis* t'écrit : tu n'es *pas seul*."),("Alors... *qui* est avec toi ?","Dans le *placard*."),"Yanis dort dans sa voiture. Yanis est à ta porte.")
st("5C","SALON","PALIER","Imagine.","Il est *trois heures* du matin.","03:06:00","03:30:00","Trois heures *trente*.",("Théo","Ton copain","Théo"),"Un message de *Théo*.",
   [("Je suis à Montréal pour le travail.","Je suis à *Montréal* pour le travail."),("Mon vol est samedi.","Mon vol est *samedi*."),("Ne m'attends pas avant.","Ne m'attends *pas avant*.")],
   "C'est *Théo*... surprise, je suis rentré plus tôt !","Ton copain.",("Théo","Je suis toujours à Montréal.","Mais il écrit : il est *toujours à Montréal*."),"il","*Surprise*.",
   ("Théo","Qui est dans ton appartement ? J'ai vu une ombre.","*Théo* demande : qui est *dans ton appartement* ?"),("Alors... *qui* est entré ?","Dans le *placard*."),"Théo est à Montréal. Quelqu'un prétend être lui.")
st("1","SALON","ENTRÉE","Ne bouge pas.","Il est *deux heures* du matin.","02:00:00","02:25:00","Deux heures *vingt-cinq*.",("Maison connectée","Assistant · Mode nuit","Maison"),"Un message de ta *maison connectée*.",
   [("Mode nuit activé.","Mode nuit *activé*."),("Les portes sont verrouillées.","Les portes sont *verrouillées*."),("Je surveille toutes les pièces.","Je surveille *toutes les pièces*.")],
   "Mode nuit... *désactivé*. Ouvre, c'est moi.","Ta propre maison.",("Maison","Aucune présence détectée dans le couloir.","Mais la maison écrit : aucune *présence* dans le couloir."),"il","Bonne *nuit*.",
   ("Maison","Deux occupants détectés dans le logement.","*La maison* t'écrit : *deux occupants* détectés dans le logement."),("Alors... *qui* est le deuxième ?","Dans le *placard*."),"La maison détecte deux occupants. Tu es seul.")
st("1","SALON","ENTRÉE","Écoute.","Il est *une heure* du matin.","01:05:00","01:40:00","Une heure *quarante*.",("Chalet des Alpes","Propriétaire","Propriétaire"),"Un message du *propriétaire* du chalet.",
   [("La tempête arrive cette nuit.","La *tempête* arrive cette nuit."),("Ne sors pas du chalet.","Ne sors *pas* du chalet."),("Si on frappe, c'est le vent.","Si on frappe... c'est *le vent*.")],
   "C'est le *guide*... je suis gelé, ouvre !","Le guide.",("Propriétaire","Le guide est redescendu hier soir.","Mais il écrit : le guide est *redescendu* hier soir."),"il","Il fait *chaud*, ici.",
   ("Propriétaire","Le vent n'a pas de mains.","Le *propriétaire* t'écrit : le vent n'a *pas de mains*."),("Alors... *qui* frappait ?","Dans le *placard*."),"Si on frappe, c'est le vent. Vraiment ?")
st("2B","SALON","ENTRÉE","Ce soir.","Il est *trois heures* du matin.","03:10:10","03:35:00","Trois heures *trente-cinq*.",("Standard médical","Médecin de garde","Standard"),"Un message du *standard médical*.",
   [("Un médecin de garde peut passer.","Un médecin de garde *peut passer*."),("Nous vous appelons avant.","Nous vous *appelons* avant."),("Sinon, n'ouvrez pas.","Sinon... n'ouvrez *pas*.")],
   "*Médecin* de garde... on m'a appelé pour vous.","Le médecin.",("Standard","Aucun médecin n'a été envoyé à cette adresse.","Mais le standard écrit : aucun médecin n'a été *envoyé*."),"il","Ne vous *inquiétez* pas.",
   ("Standard","Quelqu'un a appelé depuis votre téléphone.","Le *standard* t'écrit : quelqu'un a appelé *depuis ton téléphone*."),("Alors... *qui* a appelé ?","Derrière *toi*."),"Tu n'as appelé aucun médecin.")
st("13","SÉJOUR","COULOIR","Imagine.","Il est *deux heures* du matin.","01:52:00","02:00:00","Deux heures *pile*.",("Énergie Plus","Service client","Énergie Plus"),"Un message d'*Énergie Plus*.",
   [("Coupure programmée à 02h00.","Coupure programmée, à *deux heures*."),("Aucun technicien ne passera.","Aucun technicien *ne passera*."),("Gardez une lampe à portée.","Gardez *une lampe* à portée.")],
   "C'est l'*électricien*... je dois vérifier le compteur.","L'électricien.",("Énergie Plus","Aucun technicien n'est en intervention.","Mais *Énergie Plus* écrit : aucun technicien *en intervention*."),"il","Compteur *vérifié*.",
   ("Énergie Plus","Le compteur indique une présence inconnue.","*Énergie Plus* t'écrit : le compteur indique *une présence inconnue*."),("Alors... *qui* consomme du courant ?","Dans le *placard*."),"Aucun électricien n'est en intervention.")
st("6","SALON","PALIER","Écoute.","Il est *minuit* passé.","00:08:08","00:44:00","Minuit *quarante-quatre*.",("Ancien locataire","Julien","Julien"),"Un message de *Julien*, l'ancien locataire.",
   [("Ne cherche pas la pièce du fond.","Ne cherche *pas* la pièce du fond."),("Elle n'était pas sur le plan.","Elle n'était *pas* sur le plan."),("Si tu l'entends, ne réponds pas.","Si tu l'entends... ne réponds *pas*.")],
   "C'est *Julien*... j'ai oublié quelque chose chez toi.","L'ancien locataire.",("Julien","J'ai déménagé à l'étranger il y a un an.","Mais il écrit : il a *déménagé* à l'étranger. Il y a un an."),"il","Je l'ai *retrouvé*.",
   ("Julien","Ne dors pas dans la chambre.","*Julien* t'écrit : ne dors *pas* dans la chambre."),("Alors... *qui* vit dans la pièce du fond ?","Dans le *placard*."),"Il y a une pièce qui n'était pas sur le plan.")
st("9","SALON","PALIER","Ce soir.","Il est *deux heures* du matin.","02:11:30","02:30:00","Deux heures *trente*.",("Marc","Voisin du dessous","Marc"),"Un message de *Marc*, ton voisin.",
   [("J'ai lâché mon chien dans le couloir.","J'ai lâché *mon chien* dans le couloir."),("Il n'aboie que sur les inconnus.","Il n'aboie que *sur les inconnus*."),("Écoute s'il se tait.","Écoute *s'il se tait*.")],
   "C'est *Marc*... mon chien s'est enfui, tu l'as vu ?","Ton voisin.",("Marc","Mon chien dort à côté de moi.","Mais il écrit : son chien *dort* à côté de lui."),"il","Il s'est *tu*.",
   ("Marc","Mon chien grogne devant ton appartement.","*Marc* t'écrit : son chien *grogne* devant chez toi."),("Alors... *qui* l'a fait taire ?","Derrière *toi*."),"Le chien de Marc dort. Alors qui aboyait ?")
st("4","SÉJOUR","ENTRÉE","Imagine.","Il est *trois heures* du matin.","03:01:01","03:22:00","Trois heures *vingt-deux*.",("Interphone","Accueil de l'immeuble","Interphone"),"Un message de l'*interphone*.",
   [("Visiteur à l'accueil.","*Visiteur* à l'accueil."),("Aucun nom enregistré.","Aucun nom *enregistré*."),("N'appuyez pas sur le bouton.","N'appuyez *pas* sur le bouton.")],
   "C'est moi... *appuie* sur le bouton.","Le visiteur.",("Interphone","Aucun visiteur à l'accueil.","Mais l'interphone écrit : aucun *visiteur* à l'accueil."),"il","Enfin... *entré*.",
   ("Interphone","La porte d'entrée a été ouverte de l'intérieur.","L'*interphone* t'écrit : la porte d'entrée a été ouverte *de l'intérieur*."),("Alors... *qui* l'a ouverte ?","Derrière *toi*."),"Aucun visiteur à l'accueil. Pourtant, ça frappe.")
st("7B","APPARTEMENT","PALIER","Écoute.","Il est *minuit* et quart.","00:14:00","00:35:00","Minuit *trente-cinq*.",("Amina","Ta cousine","Amina"),"Un message d'*Amina*, ta cousine.",
   [("Je dors chez Yasmine ce soir.","Je dors *chez Yasmine* ce soir."),("Ne m'attends pas, j'ai mes clés.","Ne m'attends pas. J'ai *mes clés*."),("Ne réponds pas à la porte.","Ne réponds *pas* à la porte.")],
   "C'est *Amina*... j'ai changé d'avis, ouvre.","Ta cousine.",("Amina","Je suis chez Yasmine, on mange.","Mais elle écrit : elle est *chez Yasmine*. Elle mange."),"elle","Je suis *rentrée*.",
   ("Amina","J'ai vu quelqu'un entrer chez toi par la fenêtre.","*Amina* t'écrit : quelqu'un est entré chez toi *par la fenêtre*."),("Alors... *qui* est entré ?","Dans le *placard*."),"Amina est chez Yasmine. Elle frappe à ta porte.")
st("2D","SÉJOUR","ENTRÉE","Ne bouge pas.","Il est *une heure* du matin.","01:15:15","01:44:00","Une heure *quarante-quatre*.",("Coloc du 2e","Nina, nouvelle colocataire","Nina"),"Un message de *Nina*, ta nouvelle colocataire.",
   [("Je dors chez mon copain ce soir.","Je dors *chez mon copain* ce soir."),("Je rentre demain matin.","Je rentre *demain matin*."),("Je n'ai pas encore mes clés.","Je n'ai *pas encore* mes clés.")],
   "C'est *Nina*... j'ai fini plus tôt, ouvre-moi.","Ta nouvelle colocataire.",("Nina","Je suis chez Tom, on regarde un film.","Mais elle écrit : elle est *chez Tom*. Devant un film."),"elle","Bienvenue *chez nous*.",
   ("Nina","Tu as vu l'autre chambre ? Elle est occupée.","*Nina* t'écrit : l'autre chambre est *occupée*."),("Alors... *qui* dort dans l'autre chambre ?","Dans le *placard*."),"Ta colocataire est chez son copain. Elle est aussi à ta porte.")
st("0","SALON","ENTRÉE","Imagine.","Il est *trois heures* du matin.","03:12:07","03:20:00","Trois heures *vingt*.",("Toi","Messages enregistrés","Toi"),"Un message de... *toi*.",
   [("Si tu lis ça, j'ai déjà ouvert.","Si tu lis ça... j'ai *déjà ouvert*."),("Ne fais pas la même erreur.","Ne fais pas *la même erreur*."),("Il imite ma voix.","Il imite *ma voix*.")],
   "C'est *toi*... ouvre-moi.","Ta propre voix.",("Toi","Je ne suis jamais sorti ce soir.","Mais *tu* as écrit : tu n'es *jamais sorti* ce soir."),"il","Je suis *toi*.",
   ("Toi","Regarde bien la date de ce message.","*Toi* t'écris : regarde *la date* de ce message."),("Alors... *qui* es-tu ?","Derrière *toi*."),"Le dernier message vient de toi.")

def build(i, d):
    n = i + 2   # ep002 = nuit 2
    v = VAR[(n - 1) % 4]; gname, gsub, sender = d["g"]
    he = "Il" if d["gen"] == "il" else "Elle"
    cap = d["cap"] + (" Réponds 1 ou 2. Nuit %d demain." % (n + 1) if n < 30 else " La suite bientôt.")
    return {"id": "ep%03d" % n, "night": n, "palette": PAL[(n - 1) % 4], "outfit": list(OUTF[(n - 1) % 5]),
        "places": {"hook": d["hp"], "door": d["dp"], "bed": "CHAMBRE"}, "clock": {"hook": d["hc"], "event": d["ev"]},
        "group": {"name": gname, "sub": gsub, "sender": sender}, "hook": [d["h0"], d["h1"]], "buzz": ["Ton *téléphone* vibre.", d["intro"]],
        "rules": [list(r) for r in d["rules"]], "blackout": d["ep"], "knocks": KNOCKS[(n - 1) % 3], "plate": d["plate"],
        "voice": d["voice"], "who": d["who"], "contra": list(d["contra"]), "choice": v[0], "ask": v[1], "pick": "Tu *ouvres*.",
        "peep": ["Tu regardes par le *judas*.", he + " *sourit*.", "Beaucoup *trop*."], "scare": d["scare"], "retry": v[2],
        "leave": LEAVE[(n - 1) % 4], "twist": list(d["twist"]), "end": list(d["end"]), "cta": [CTA0[(n - 1) % 3], "Réponds en *commentaire*."],
        "cta_title": CTAT[(n - 1) % 3], "cta_opts": ["OUVRIR", "SE CACHER"], "caption": cap, "tags": TAGS}

bad = 0
for i, d in enumerate(D):
    s = build(i, d)
    spoken = s["hook"] + s["buzz"] + [r[1] for r in s["rules"]] + [s["blackout"], s["knocks"], s["voice"], s["who"], s["contra"][2], s["ask"], s["pick"]] + s["peep"] + [s["scare"], s["retry"], s["leave"], s["twist"][2]] + s["end"] + s["cta"]
    for t in spoken:
        if re.search(r"\d", t) or t.count("*") % 2: print("PROBLÈME", s["id"], t); bad += 1
    json.dump(s, open(os.path.join(OUT, s["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
print(len(D), "histoires écrites ;", bad, "problèmes")
