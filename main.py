import classes

def main():
    mediator=None
    while True:
        print("""
        ***** SCRABBLE *****
        --------------------
        1: Σκορ
        2: Οδηγίες
        3: Παιχνίδι
        e: Έξοδος από την εφαρμογή
        --------------------

        """)
        choice=input("Παρακαλώ επιλέξτε ένα από τα παραπάνω ")
        match choice:
            case '1':
                classes.Game.display_history_score()
            case '2':
                print("""
                Παίζετε εναλλάξ δημιουργώντας λέξεις 
                -Άμα θελήσετε αλλαγή γραμμάτων τότε πατήστε το πλήκτρο Π στο πεδίο ΛΕΞΗ
                -Άμα θελήσετε να παραιτηθείται από την τρέχουσα παρτίδα του παιχνιδιού και να επιστρέψετε στο μενού 
                τότε πατήστε το πλήκτρο q/Q στο πεδίο ΛΕΞΗ. 
                -Για οριστική έξοδο πατήστε 'e' στο κεντρικό μενού
                -Ο υπολογιστής παίζει με τον αλγόριθμο Smart-Fail. Βρισκει πιθανές λέξεις συμφωνα με τα γράμματα που έχει 
                και διαλέγει τυχαία ποια θα παίξει
                -Για να δείτε αποτελέσματα προηγούμενων πατρίδων πατήστε 1
                """)
            case '3':
                name=input("Δωστέ παρακαλώ το όνομα σας ")
                mediator=classes.Game(name)
                if mediator.has_saved_game(name):
                    resume= input(f"Βρέθηκε αποθηκευμένη παρτίδα για {name}. Θέλετε να συνεχίσετε; (ν/ο) ")
                    mediator.setup(name, force_new=(resume!='ν'))
                else:
                    mediator.setup(name)

                while not mediator.game_over:
                    print(f"\n****************************************************\n"
                        f"Παίχτης: { mediator.human.name } *** Σκορ: {mediator.human.score}\n"
                        f"Γράμματα: {mediator.human.sack}\n"
                        f"****************************************************\n"
                    )
                    
                    if not mediator.human.play(mediator):
                        break

                    if mediator.game_over:
                        break

                    print(f"\n****************************************************\n"
                        f"Παίχτης: { mediator.pc.name } *** Σκορ: {mediator.pc.score}\n"
                        f"Γράμματα: {mediator.pc.sack}\n"
                        f"****************************************************\n"
                        )
                    mediator.pc.play(mediator)
                    
                    
            case 'e':
                print("Ευχαριστούμε που παίξατε μαζί μας!!!")
                break
            case _:
                print("Μη έγκυρη επιλογή, δοκιμάστε ξανά")

if __name__== "__main__":
    main()
    

