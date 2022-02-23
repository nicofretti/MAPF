# MultiAgentPathFinding
__Jacopo Zagoli__\
Progetto per l'esame di fondamenti di intelligenza artificiale, _A.A. 2021/2022._\
http://idm-lab.org/project-p/project.html  

## Space-time A*
L'implementazione corrente di A* cerca un percorso solo nello spazio, non considerando
il tempo.  
Dobbiamo quindi modificare l'algoritmo in modo che cerchi un percorso nell'insieme di 
coppie (posizione, timestamp), e che consideri i vincoli.
#### Task 1.1 
Modificato A* in modo che i nodi generati ed esplorati mantengano
un timestamp aggiornato. Inoltre ora viene generato un nodo in cui l'agente rimane nella
posizione corrente.
#### Task 1.2
L'insieme di vincoli dati in ingresso viene filtrato per agente e
indicizzato per timestamp nella funzione `build_constraint_table`.  
Implementata la funzione `is_constrained`, che dati i parametri di un 
nodo e del parent, controlla se viene violato un vincolo presente
nella tabella costruita sopra.
Per ora gli unici tipi di vincoli considerati sono vertex constraints.
#### Task 1.3
Aggiunto il support per gli edge constraint: l'unica funzione modificata
è `is_constrained`, che data la posizione corrente, futura e il timestamp
verifica se il nodo viola almeno uno dei due tipi di vincoli.
#### Task 1.4
Viene aggiunto un controllo per verificare se il nodo raggiunto è di goal: 
ora non basta raggiungere la posizione finale, è anche necessario che la posizione
finale raggiunta non compaia in nessun vincolo dal timestamp corrente in poi.
Per verificarlo viene creata la funzione `is_goal_constrained`, che verifica tutti i
vincoli dei timestamp futuri.

## Prioritized Planning
Lo scopo dei task seguenti è quello di modificare il codice corrente in modo
da implementare correttamente l'algoritmo di Prioritized Planning.
### Task 2.1
Grazie all'algoritmo space-time A* implementato prima, possiamo trovare un percorso
per ogni agente. In questo task, partendo da un percorso, dobbiamo generare tutti i 
vertex constraint richiesti: iteriamo quindi il percorso e per ogni locazione aggiungiamo 
a tutti gli agenti (tranne quello corrente) un vincolo che impedisce di essere in 
quella locazione in quel momento.
### Task 2.2
Piccola modifica che aggiunge, per ogni coppia locazione-momento, un edge constraint:
per fare questo, è necessario ottenere anche la prossima locazione nel percorso a ogni iterazione
(tranne l'ultima).
### _Opzionale:_ Task 2.3
Il codice finora implementato non rileva collisioni fra agenti se un agente ha già raggiunto
il suo obiettivo: questo perchè viene aggiunto un vincolo per ogni locazione presente
nel percorso, ma finito il percorso, non vengono aggiunti altri vincoli.  
Per ovviare a questo problema, ho modificato la struttura dei vincoli, aggiungendo un campo
_'final'_. Un vincolo con il campo final impostato a True è chiamato _final constraint_, 
e indica che nessun agente potrà trovarsi nella locazione indicata dal vincolo in un
momento successivo a quello indicato nel vincolo.  
Il codice è quindi così modificato:
- quando itero un percorso per generare un vincolo, controllo se sono nella posizione finale
(l'ultima del percorso). Se sì, imposto il campo final a True.
- nell'algoritmo space-tima A*, quando controllo se un nodo generato è soggetto a vincoli,
ora controllo anche se in qualche momento precedente la posizione corrente compare in un final constraint.

## Conflict-Based Search
Lo scopo dei task seguenti è quello di implementare correttamente l'algoritmo di Conflict-Based Search.
### Task 3.1
Bisogna implementare una funzione che restituisca una lista di tutte le prime collisioni fra due percorsi,
chiamata `detect_collisions`. Questa funzione ha due cicli innestati: il primo scorre tutti i percorsi, il secondo
scorre tutti gli altri percorsi partendo da quello successivo a quello del ciclo esterno. Confronta quindi i due
percorsi correnti per trovare una prima collisione, e se è presente, la appende a una lista.  
Per trovare la prima collisione fra due percorsi, si usa la funzione `detect_collision` che rileva le collisioni
con un metodo molto simile a quello usato nel Prioritized Planning.
La differenza principale, però, sta nel metodo che si usa per rilevare collisioni dopo che un agente ha raggiunto
un obiettivo: al posto di utilizzare final constrains, visto che sappiamo già la lunghezza di tutte le path,
prima di confrontarle estendiamo la più corta con la sua ultima posizione in modo che sia lunga come l'altra.
Per far questo usiamo la funzione `normalize_paths`.  
Esempio:\
`path1 = (1,1) (1,2) (1,3) (1,4)`\
`path2 = (1,3) (1,4)`\
dopo la normalizzazione diventano:\
`path1 = (1,1) (1,2) (1,3) (1,4)`\
`path2 = (1,3) (1,4) (1,4) (1,4)`
### Task 3.2
Per convertire un collisione in vincoli, si usa la funzione `standard_splitting`: in base al tipo di collisione
(edge o vertex) crea due vincoli, uno che si riferisce al primo agente coinvolto e uno che si riferisce al secondo.  
Si noti che in caso di edge collision, le locazioni del secondo vincolo vanno invertite.
### Task 3.3
In questo task è stata implementata la parte di high-level search di CBS, come descritto dall'algoritmo
presente nel file handout.pdf. Sono state usate le funzioni implementate in precedenza.