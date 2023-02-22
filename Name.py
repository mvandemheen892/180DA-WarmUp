import random

def generate_name(training_words):
    while True:
        # Start with a random word root
        word_root = random.choice(training_words)
        name = word_root
        while name[-1].isalpha() and len(name) < 10:
            # Find all words that start with the last character of the current word
            next_word_options = [w for w in training_words if w.startswith(name.split()[-1])]
            if not next_word_options:
                break
            next_word = random.choice(next_word_options)
            name += " " + next_word
        if len(name) > 3 and name[-1].isalpha():
            return name




def train_markov_chain(text):
    chain = {}
    for i in range(len(text) - 1):
        if text[i] not in chain:
            chain[text[i]] = {}
        if text[i + 1] not in chain[text[i]]:
            chain[text[i]][text[i + 1]] = 0
        chain[text[i]][text[i + 1]] += 1
    return chain

def generate_names(text, n):
    chain = train_markov_chain(text)
    names = [generate_name(chain) for i in range(n)]
    return names

def main():
    text = """Aldorin
    Elwynn
    Eirielle
    Ilmare
    Arwynn
    Galadrielle
    Sylphrena
    Elentari
    Elvandar
    Mirielle
    Isolde
    Eledhwen
    Melwas
    Annwyn
    Calantha
    Araneth
    Brudor
    Farnborough
    Reidchester
    Kerromouth
    Rushcliffe
    Cragstrath
    Wellstrath
    Wellhaven
    Cragcleave
    Craghaven
    Galadhor
    Doudor
    Trurin
    Shevalon
    Romor
    Rimor
    Oflor
    TaChar
    Oglan
    Obror
    Hamoth
    Sera
    Swogwack
    Irhuend
    Nirdhun
    Urand
    Odor
    Ionocos
    Calgar
    Calrand
    Calgaria
    Halgar
    Halgaria
    Malgar
    Balagr
    Torford
    Rosenola
    Glaswin
    Sutwich
    Duhan
    Yosnia
    Tennigon
    Tewewn
    Dawnstrider
    Wildlings
    Irongulch
    Shadowrune
    Atarath
    Atarathia
    Oxcall
    Stagwich
    Hartfort
    Merimarsh
    Southlyn
    Val Dorgo
    Dukes Folly
    Vesper Gulch
    Gladstowe
    Arryn
    Erryn
    Olissimerry
    Malvilsar
    Ositros
    Corolora
    Tun-Mundor
    Hagron
    Bracos
    Aria
    Oluin
    Baluth
    Baluthia
    Rarrond
    Rarrond
    Aranamel
    Reanalon
    Menalor
    Easthand
    Ryre
    Ryremark
    Aedon
    Baldon
    Baldonia
    Derryby
    Ryleigh
    Reovia
    Balerno
    Mirefield
    Dalrmark
    Isith
    Eren
    Avestria
    Erremark
    Reovia
    Orvanador
    Elvandar
    Evermist
    Arvandor
    Dawnbreak
    Valtoria
    Stonehaven
    Nicodranas
    Whitestone
    Emon
    Draconia
    Rosana
    Basuras
    Jrusar
    Kymal
    Syngorn
    Cathmoira
    Avalir
    Issylra
    Marquet
    TalDorei
    Wildemount
    Damali
    Zoon
    Aeor
    Shadycreek
    Rotthold
    Swaivane
    Westruun
    Stilrun
    Eiselcross
    Wynandir
    Zadash
    Trostenwald
    Alfield
    Xhorhas
    Blightshore
    Hadwyn
    Kessel
    Rohan
    
    """
    names = generate_names(text, 400)
    for name in names:
        print(name)

if __name__ == "__main__":
    main()
