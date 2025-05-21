# Projekt "SkillSwap"
 
 **SkillSwap** je spletna aplikacija za izmenjavo veščin, ki omogoča uporabnikom, da se povežejo in učijo drug od drugega. Aplikacija bo uporabljala naslednje tehnologije:
 
 - **Python (Flask)** za strežnik
 - **HTML, CSS, JavaScript** za uporabniški vmesnik
 - **JSON datoteke** za shranjevanje podatkov
 
 ## Koraki razvoja
 
 1. **Postavitev Flask strežnika**  
    Inicializacija Flask aplikacije in konfiguracija poti za prikaz strani (npr. index, registracija, iskanje).
 
 2. **Ustvarjanje osnovnih HTML strani**  
    - **index.html**: Glavna stran
    - **register.html**: Registracija uporabnika
    - **search.html**: Iskanje partnerjev za učenje
 
 3. **Registracija uporabnika**  
    Obrazec za vnos imena, veščin, želja in Discord username-a. Podatki se shranijo v **users.json**.
 
 4. **Prikaz in iskanje uporabnikov**  
    Branje podatkov iz **users.json** in filtriranje po ponujenih veščinah.
 
 5. **Povezovanje uporabnikov**  
    Prikaz kontaktnih podatkov (Discord username) in možnost filtriranja glede na jezik, lokacijo (kasnejše nadgradnje).
 
 6. **Dodatne funkcije (nadgradnje)**  
    - Ocene in pregledi uporabnikov
    - Sistem značk (npr. "Zanesljiv učitelj")
    - Možnost direktnega klepeta znotraj aplikacije
 
 Aplikacija omogoča enostavno iskanje in izmenjavo veščin ter kasnejše nadgradnje za boljšo izkušnjo uporabnikov.
