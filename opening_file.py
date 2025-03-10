def open_file(path):
    test=[]
    
    with open(path, 'r') as f:
        lignes = f.readlines()
        print(lignes)
        for i in range (0, len(lignes), 2):
            m,n = lignes[i].split()
            taille = [m,n]
             
            
            figures = lignes[i+1].split()
            liste = [taille]
            for i in range (0,len(figures), 2):
                coordonnees = [figures[i], figures[i+1]]
                liste.append(coordonnees)
        
            test.append(liste)
            
     
            
        return test
