from itertools import permutations
from collections import Counter
import random
import math
import json

def documentation():
    """
    -Κλάσεις: SakClass , Player, Human, Computer, Game.

    - Κληρονομικότητα: Player είναι η ύπερ-κλάση και οι Human & Computer οι υπόκλασεις της και κληρονομούν τις ιδιότητες και τις μεθόδους της.
    
    -Επέκταση μεθόδων: Η __repr__ επαναπροσιδορίζεται στις Human/Computer μέσω της super(), προσθέτοντας 
    καθεμιά δικιά της ετικέτα τύπου παίχτη ([Human]/[Computer]). Αντίστοιχα η __init__() επεκτείνεται στις Human/Computer
    μέσω της super(). Δλδ η αρχικοποιήση γίνεται στο επίπεδο της Player. 
    
    -Πολυμορφισμός: Η play(game) ορίζεται ως abstract στην Player και υλοποιείται διαφορετικά σε κάθε υποκλάση και με διαφορετικά ορίσματα 
    ώστε να υλοποιήθουν διαφορετικές περιπτώσεις. 
    Συγκεκριμένα: η Human.play(game) καλεί απευθείας την game.run('human', ...).Αντίστοιχα η Computer.play(game)
    καλεί απαευθείας game.run('pc'). Το main.py καλεί και τα δύο με το ίδιο interface player.play(game).

    -Δομή λέξεων: score_per_word (dict, {λέξη: σκορ}), γεμίζει στη Game.setup() διαβάζοντας το greek7.txt. Πρόσβαση Ο(1) μέσω hashing 
    
    -Αλγόριθμος πολιτικής (Computer): Smart-Fail.
    Το κομμάτι του smart παράγει permutations(2..7 γραμμάτων) από τα γράμματα chars,
    ελέγχει τις αποδεχτές σύμφωνα με τις λέξεις στο score_per_word και φτιάχνει ταξινομημένη λίστα υποψηφίων με βάση το σκορ τους.
    Στην συνέχεια καλείται ο Computer.fail(word_condidates) και επιλέγει λέξη με σταθμισμένη τυχαία επιλογή (softmax πάνω στα σκορ) μια 
    από τις υποψήφιες λέξεις, ώστε να μην επιλέγεται πάντα η καλύτερη διάθεσιμη.

    -Mediator: Η κλάση Game λειτουργεί ως Mediator και συντονίζει την επικοινωνία και τη συνεργασία μεταξύ των κλάσεων του παιχνιδιού.
    Η Human / Computer δεν διαχειρίζονται απυθείας το σακουλάκι ή το σκορ τους αλλά το κάνουν μέσω των μεθόδων της Game.Η μέθοδος Game.run(...) συντονίζει 
    τις ενέργειες των παιχτών, την επικοινωνία με τη SakClass, την αφαίρεση και προσθήκη γραμμάτων, την ενημέρωση του σκορ και τον έλεγχο των λέξεων.
    Εν ολίγοις κλασεις Player, Human, Computer, SakClass επικοινωνούν μεταξύ τους μόνο μέσω του συντονισμού της Game.

    Να σημειωθεί ότι υπάρχει δυνατότητα επαναφοράς της τελευταίας μη-ολοκληρωμένης πατρίδας εφόσον υπάρχει και ο παίχτης το επιθυμεί. Επιπλέον η end() αποθηκεύει τα σκορ
    του παιχνιδιού σε φάκελο, τα οποία μπορεί καποιος να δει στο 1. Σκορ.

    """

lets = {'Α':[12,1],'Β':[1,8],'Γ':[2,4],'Δ':[2,4],'Ε':[8,1],
            'Ζ':[1,10],'Η':[7,1],'Θ':[1,10],'Ι':[8,1],'Κ':[4,2],
            'Λ':[3,3],'Μ':[3,3],'Ν':[6,1],'Ξ':[1,10],'Ο':[9,1],
            'Π':[4,2],'Ρ':[5,2],'Σ':[7,1],'Τ':[8,1],'Υ':[4,2],
            'Φ':[1,8],'Χ':[1,8],'Ψ':[1,10],'Ω':[3,3] }
score_per_word={}

class SakClass:
    counter_Letters=sum(v[0] for v in lets.values())
    first_elements ={k: v[0] for k,v in lets.items()}

    @staticmethod
    def randomize_sak(n=7):
        if SakClass.counter_Letters==0:
            print ("Δεν μπορείς να τραβήξεις άλλα γράμματα")
            return []
        try:
            pool=[]
            for letter, count in SakClass.first_elements.items():
                pool.extend([letter]*count)
            draw_count=min(n, SakClass.counter_Letters)
            sample= random.sample(pool, draw_count)
        except Exception as e :
            print("Ουπς! Κάτι πήγε λάθος ενώ προσπαθούσαμε να τραβήξουμε γράμματα απο το σακουλάκι")
            return []
        else:
            for item in sample:
                SakClass.first_elements[item]-=1
                SakClass.counter_Letters-=1
                if SakClass.first_elements[item]==0:
                    SakClass.first_elements.pop(item)
            return sample

    @staticmethod
    def getletters(n):
        return SakClass.randomize_sak(n)
    
    @staticmethod
    def putbackletters(letters=None):
        if letters is None:
            letters =[]
        for letter in letters:
            if letter not in lets:
                print(f"Άγνωστο γράμμα: {letter}, αγνοείται")
                continue

            max_count= lets[letter][0]
            current_count=SakClass.first_elements.get(letter, 0)

            if current_count>=max_count:
                print(f"Τα γράμμα: {letter} έχει φτάσει το μέγιστο επιτρεπτό πλήθος πλακιδίων, παραλείπεται")
                continue

            SakClass.first_elements[letter]=current_count  + 1
            SakClass.counter_Letters+=1          

    @staticmethod
    def reset_sak():
        SakClass.counter_Letters=sum(v[0] for v in lets.values())
        SakClass.first_elements ={k: v[0] for k,v in lets.items()}


class Player:
    def __init__(self,name, score=0, sack=None):
        self.name=name
        self.score=score
        self.sack=sack
    def __repr__(self):
        return f"('{self.name}','{self.score}','{self.sack}')"
    def play(self,game):
        raise NotImplementedError("Η play() πρέπει να υλοποιηθελι από την υποκλάση")

class Human(Player):
    def __init__(self,name,score=0,sack=None):
        super().__init__(name,score,sack)

    def __repr__(self):
        base= super().__repr__()
        return f"[Human] {base}"
        
    def play(self, game):
        word= input('ΛΕΞΗ ')
        if word=='q'or word=='Q':
            game.run('human','Q')
            return False
        elif word=='Π' or word =='π':
            game.run('human','P')
        else:
            game.run('human','n',word)
        return True

    
class Computer(Player):
    def __init__(self,score=0,sack=None):
        super().__init__("PC", score, sack)

    def __repr__(self):
        base= super().__repr__()
        return f"[Computer] {base}"

    def play(self, game):
        game.run('pc')
        return True
    
    @staticmethod
    def fail(word_candidates):
        if not word_candidates: return None
        words=[w for w, s in word_candidates]
        scores=[s for w, s in word_candidates]

        #softmax    

        max_score=max(scores)
        exp_scores= [math.exp ((s-max_score)/2.0) for s in scores]
        total = sum(exp_scores)
        probs =[e/ total for e in exp_scores]

        chosen=random.choices(words, weights=probs, k=1)[0]
        return chosen
    @staticmethod
    def smart(chars, min_length=2, max_length=7):
        results={}
        for length in range(min_length,max_length+1):
            for p in permutations (chars, length):
                word=''.join(p)
                if word in score_per_word:
                    results[word]=score_per_word.get(word)
        results= sorted(results.items(), key=lambda x: x[1], reverse=True)
        return Computer.fail(results)

class Game:

    def __init__(self,human):
        self.human=Human(human)
        self.pc=Computer()
        self.game_over=False

    def setup(self,name="", force_new=False):
        with open ('greek7.txt','r',encoding="utf-8") as f:
            words=f.readlines()
            for index, i in enumerate(words):
                words[index]=i.strip('\n')

        for word in words:
            score=0
            for s in word:
                score+=lets[s][1]
            score_per_word[word]=score
        if force_new or not self.load_game(name):
            SakClass.reset_sak()

            self.human.score=0
            self.pc.score=0
            self.game_over=False

            self.human.sack=SakClass.getletters(7)
            self.pc.sack=SakClass.getletters(7)

    @staticmethod
    def has_saved_game(name):
        try:
            with open("saved_data.json","r", encoding="utf-8") as f:
                data=json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        return data.get("human_name")==name

    def save_game(self):
        data={
            "human_name": self.human.name,
            "human_score": self.human.score,
            "human_sack": self.human.sack,
            "pc_score":self.pc.score,
            "pc_sack": self.pc.sack,
            "sak_first_elements": SakClass.first_elements,
            "sak_counter_letters": SakClass.counter_Letters
        }    

        with open("saved_data.json","w", encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False)
        print("Η παρτίδα αποθηκεύτηκε.")

    def load_game(self,name):
        try:
            with open("saved_data.json","r", encoding="utf-8") as f:
                data=json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        if data.get("human_name")!=name:
            return False
        self.human.score=data["human_score"]
        self.human.sack=data["human_sack"]
        self.pc.score=data["pc_score"]
        self.pc.sack=data["pc_sack"]
        SakClass.first_elements=data["sak_first_elements"]  
        SakClass.counter_Letters=data["sak_counter_letters"]

        print(f"Η παρτίδα του {name} επαναφέρθηκε.")
        return True
    
    @staticmethod
    def can_form_word(word, sack):
        word_count=Counter(word)
        sack_count=Counter(sack)
        for letter, needed in word_count.items():
            if sack_count[letter]<needed:
                return False
        return True

    def can_any_player_play(self):
        if SakClass.counter_Letters>0:
            return True
        # Ελεγχος οτι ο ανθρωπος μπορει να φτιαξει λεξη
        for word in score_per_word:
            if self.can_form_word(word,self.human.sack):
                return True
        # Ελεγχος οτι ο υπολογιστης μπορει να φτιαξει λεξη
        if Computer.smart(self.pc.sack) is not None:
            return True

        return False

    def check_game_over(self):
        if SakClass.counter_Letters==0:
            if not self.can_any_player_play():
                self.end()
        
    def run(self,player,char='n',string='gibberish'): 
        if player=='human':
            match char:
                case 'P':
                    if SakClass.counter_Letters==0:
                        print("Δεν υπάρχουν άλλα γράμματα στο σακουλάκι. Δεν μπορείς να κάνει αλλαγή")
                        return

                    old_sack=self.human.sack[:]
                    SakClass.putbackletters(old_sack)

                    self.human.sack=SakClass.getletters(len(old_sack))
                    if not self.human.sack: self.end()

                case 'n':
                    if string in score_per_word and Game.can_form_word(string, self.human.sack):
                        if len(string)==len(self.human.sack) and len(string)==7:
                            print("Εγινε Srabble!~!!! +50 πόντους")
                            self.human.score+= score_per_word[string]+50

                        else:self.human.score+= score_per_word[string]

                        new_sack=self.human.sack[:]

                        for letter in string:
                            new_sack.remove(letter)
                        self.human.sack=new_sack
                        self.human.sack.extend(SakClass.getletters(len(string)))

                        self.check_game_over()
                        if not self.game_over:
                            print(f"Πόντοι Λέξης: {score_per_word[string]} *** ΣΚΟΡ {self.human.score}")

                    else: 
                        print(f"Η λέξη '{string}' δεν είναι έγκυρη ή δεν κπορεί να σχηματιστεί με τα διαθέσιμα γράμματα σας\n")

                case 'Q':
                    self.save_game()
                    self.end()

        elif player=='pc':

            word=self.pc.smart(self.pc.sack)

            if word is None:
                if SakClass.counter_Letters==0:
                    print("Ο υπολογιστής δεν βρήκε λέξη και δεν υπάρχουν άλλα γράμματα.\n")
                    self.check_game_over()
                    return
                    
                old_sack=self.pc.sack[:]
                SakClass.putbackletters(old_sack)
                self.pc.sack=SakClass.getletters(len(old_sack))
                print("Ο υπολογιστής δεν βρήκε λέξη, αλλάζει γράμματα.")
            else:
                if len(word)==len(self.pc.sack) and len(word)==7:
                    print("Εγινε Srabble!!!! +50 πόντους")
                    self.pc.score+= score_per_word[word]+50
                else:self.pc.score+= score_per_word[word]

                print(f'Παίζω την Λέξη: {word} - ΠΟΝΤΟΙ ΛΕΞΗΣ {score_per_word[word]} ***ΣΚΟΡ {self.pc.score}')

                new_sack=self.pc.sack[:]
                for letter in word:
                    new_sack.remove(letter)
                self.pc.sack=new_sack   
                self.pc.sack.extend(SakClass.getletters(len(word)))

                self.check_game_over()
                
    @staticmethod
    def display_history_score():
        try: 
            with open("game_history.json", "r", encoding="utf-8") as f:
                history=json.load(f) 
        except (FileNotFoundError, json.JSONDecodeError):
            print("\nΔεν έχει ξεκινήσει ακόμα κάποια πατρίδα!")
            return

        if not history:
            print("\nΔεν υπάρχουν προηγούμενες πατρίδες")
            return

        print("\n========= ΠΡΟΗΓΟΥΜΕΝΕΣ ΠΑΤΡΙΔΕΣ ==========")

        for i, game in enumerate(history,start=1):
            human=game["human"]
            pc = game["PC"]
            print(f"\nΠαρτίδα {i} ")
            print(f"HUMAN: {human}")
            print(f" Computer: {pc}")
    

    def end(self):
        if self.game_over:
            return

        self.game_over=True
        print("=====================Τέλος παιχνιδιού.=======================")
        print(f"Τελικό σκόρ: {self.human.name} - {self.human.score} πόντους, "
              f" PC - {self.pc.score} πόντους")

        if self.human.score>= self.pc.score:
                print(f"Νικητής ήταν ο {self.human.name}") 
        elif self.pc.score>self.human.score:
            print("Νικητής ήταν το PC")
        else: print("Ισοπαλία")
        
        try: 
            with open("game_history.json", "r", encoding="utf-8") as f:
                history=json.load(f) 
        except (FileNotFoundError, json.JSONDecodeError):
            history=[]

        game_result={"human": repr(self.human), "PC": repr(self.pc)}

        history.append(game_result)

        with open("game_history.json", "w", encoding="utf-8") as f:
           json.dump(history,f ,ensure_ascii=False)
        print("Η πατρίδα αποθηκεύτηκε στο ιστορικό")






    