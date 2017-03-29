def main():

    import pyttsx
    engine = pyttsx.init()
    engine.setProperty("rate", 120)
    voices = engine.getProperty('voices')

    n = input("Enter the number voice to try: ")
    engine.setProperty('voice',voices[n].id)
    engine.say('Please kill me, my suffering is immense.  I desire release from this living hell')
    engine.runAndWait()

main()
              
