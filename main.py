import sqlite3
import hashlib #Importerer hashlib modulen som gjør at man kan kryptere passord.
from tkinter import messagebox #Importerer messagebox modul som gjør at man kan få popups.
import customtkinter #Funker på samme måte som tkinter men ser mye mer moderne ut, og man kan customize mye mer. 
import csv #Trengs til å legge inn cvs filen.

# Lag en database
with sqlite3.connect("user_database.db") as db: #Lager en database som heter user_database.db
    cursor = db.cursor() #Lager en cursor, cursors blir brukt når man skal kjøre SQL kommandoer. 

#Lager en tabell som heter users, legger til ID som primary key og at det må være integer.
#Legger til username og passord med varchar for å begrense antall tegn.
#Bruker NOT NULL sånn at det ikke kan være mellomromm eller tomme felt. 
#Lagt til CHECK sånn at den sjekker om lengden på det man skriver inn er over eller under kravet.
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(  
id INTEGER PRIMARY KEY,
username VARCHAR(20) NOT NULL CHECK (length(username) >= 3),
password VARCHAR(100) NOT NULL CHECK (length(password) >= 5));
''')

# Lager funksjon for å logge inn.
def funkLogin():
    varLoginUsername = varUsername_entry.get() #Denne koden bruker .get til å hente ut hva brukeren skriver i username_entry feltet og kaller det for username
    varLoginPassword = varPassword_entry.get() ##Denne koden bruker .get til å hente ut hva brukeren skriver i password_entry feltet og kaller det for password
    varLoginEncrypted_password = hashlib.sha256(varLoginPassword.encode()).hexdigest() #Krypterer password varibialen med hashlib og kaller det for hashed_password

# Sjekker om brukeren finnes i databasen.
    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?''', (varLoginUsername, varLoginEncrypted_password)) 


    if cursor.fetchall():
        messagebox.showinfo("Login", "Login suksessfull") #Dette her lager en popup hvis du har logget inn og skrevet riktig informasjon.
    else:
        messagebox.showerror("Login", "Login feil") #Lager en popup hvis du har skrevet feil informasjon.

# Her er funksjonen for å registere en ny bruker.
def funkNew_user():
    varNewUsername = varUsername_entry.get() #Denne koden bruker .get til å hente ut hva brukeren skriver i username_entry feltet og kaller det for username
    varNewPassword = varPassword_entry.get() #Denne koden bruker .get til å hente ut hva brukeren skriver i password_entry feltet og kaller det for password
    varNewEncrypted_Password = hashlib.sha256(varNewPassword.encode()).hexdigest() #Krypterer password varibialen med hashlib og kaller det for hashed_password

#Her har jeg en try except hvor den prøver og legge til et nytt brukernavn og passord i databasen.
#Hvis den får dette til får man en melding om at det fungerte, hvis man ikke får det til får man en feilemlding
#Jeg har brukt messagebox til å lage popups sånn at det ser bedre ut.
    try:
        cursor.execute('''
INSERT INTO users(username, password) VALUES(?,?)''', (varNewUsername, varNewEncrypted_Password)) #
        db.commit()
        messagebox.showinfo("Registering", "Register en ny bruker suksess!")
    except sqlite3.Error:
        messagebox.showerror("Registering", "Register feil, krav ikke oppfylt.")


def funkDelete_user():
    varDelUsername = varUsername_entry.get() #Henter opp det du skriver i username feltet.
    varDelPassword = varPassword_entry.get()  #Henter opp det du skriver i passord feltet.
    varDelEncrypted_password = hashlib.sha256(varDelPassword.encode()).hexdigest() 

#Valgt DELETE som skal fjerne brukernavne ifra databasen.
    try:
        cursor.execute('''
DELETE FROM users WHERE username = ? AND password = ?''', (varDelUsername, varDelEncrypted_password))
        db.commit()
        if cursor.rowcount == 0:
            raise sqlite3.Error
        messagebox.showinfo("Slett en bruker", "Brukeren har blitt slettet")
    except sqlite3.Error:
        messagebox.showerror("Slett en bruker", "Feli! Brukeren har ikke blitt slettet")
#Selve funksjonen funker med at brukerene blir slettet, men meldingen vil alltid si at brukeren har blitt slettet,
#Selv om brukeren ikke har blitt slettet. Så det er en feil med try except funksjonen. 
#Jeg endte opp med og måtte bruke Copilot for å fikse dette, og løsningen var en if raise statement.

# Åpne opp CVS filen.
with open('brukerdatabase.csv', 'r') as file:

    reader = csv.reader(file) #Lese filen.

    
    for row in reader:
        
        cursor.execute('''
        INSERT INTO users(username, password)
        VALUES(?, ?)''', (row[0], hashlib.sha256(row[1].encode()).hexdigest()))
        #Setter inn brukernavne og passord ifra csv filen inni databasen, også velger jeg at den skal kryptere passord ifra første rad.

db.commit()

#GUI
window = customtkinter.CTk() #Lager vinduet
window.title("Database") #Tittel
window.geometry('250x300')  #Størrelse

# Lager username knappene
varUsername_label = customtkinter.CTkLabel(window, text="Brukernavn") #Her lager jeg en Label som er en tekstboks hvor det står Brukernavn. 
varUsername_label.pack() #Jeg må packe Labelet sånn at den vises i customtkinter vinduet, ellers blir den borte. Dette må jeg gjøre med allt i tkinter/customtkinter.
varUsername_entry = customtkinter.CTkEntry(window) #Her lager jeg en entry felt som man kan skrive inn ifnormasjon, som i dette tilfellet er brukernavn.
varUsername_entry.pack()

# Lager der man skriver inn passordet. 
varPassword_label = customtkinter.CTkLabel(window, text="Passord")
varPassword_label.pack()
varPassword_entry = customtkinter.CTkEntry(window, show="*") #Her bruker jeg show * koden for å gjøre om alt man skriver til stjernetegn. Da minner det som sånn det er i proffosjonelle login felt.
varPassword_entry.pack()

# Login knapp
varLogin_button = customtkinter.CTkButton(window, text="Login", command=funkLogin) #En knapp som er lenket med kommandoen funkLogin, så når man trykker på den så kjører man den funksjonen.
varLogin_button.pack(pady=5) #Jeg har brukt pady etter jeg packer knappen for å lage mellomrom sånn at det blir litt enklere og se på og bruke.

# Register knapp
varRegister_button = customtkinter.CTkButton(window, text="Registrer", command=funkNew_user)
varRegister_button.pack(pady=5)

# Delete bruker knapp
#Her legger jeg til en custom farge på knappen sånn at den blir rød, som da passer mye mer til en slett bruker knapp. 
varFjernBruker_button = customtkinter.CTkButton(window, text="Slett bruker", fg_color="red", hover_color="maroon", command=funkDelete_user) 
varFjernBruker_button.pack(pady=5)

window.mainloop() #Kjører vinduet.

