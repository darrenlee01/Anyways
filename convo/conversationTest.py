from Conversation import *

mito1 = "Mitochondria are membrane-bound cell organelles (mitochondrion, singular) that generate most of the chemical energy needed to power the cell's biochemical reactions. Chemical energy produced by the mitochondria is stored in a small molecule called adenosine triphosphate (ATP). Mitochondria contain their own small chromosomes. "
mito2 = "The mitochondrial intermembrane space is the space between the outer membrane and the inner membrane. It is also known as perimitochondrial space."
mito3 = "Some different cells have different amounts of mitochondria because they need more energy. So for example, the muscle has a lot of mitochondria, the liver does too"
music1 = "Music has played a big part in my life. I like to listen to music when I am studying, and also enjoy watching performance videos. I find that listening to music can comfort me. The type of music that I listen to changes based on my mood. When I feel very stressed, I like to listen to slow paced music that have very comforting lyrics. Growing up in a Korean family, I naturally listened to a lot of kpop and korean music in general. I grew up to like old korean music from the 70s or 80s as an influence of my parents’ music taste. I learned to play the violin when I was in elementary school. I played the violin for a few years but it has been a while since I last played. When I started listening to pop rock music, I really wanted to learn to play the drum. "
music2 = "I grew up to like old korean music from the 70s or 80s as an influence of my parents’ music taste"
music3 = "The type of music that I listen to changes based on my mood. When I feel very stressed, I like to listen to slow paced music that have very comforting lyrics."
shopping1 = "Speaking of, have you tried the drumstick ice cream from trader joe’s? I really like snacking on sweet desserts. Also, I think trader joe’s is a great supermarket. Their products are so unique and tasty. I usually get my groceries at trader joes. "
prompt = "We want to discuss our musical background. We want to talk about our personal knowledge on music and experience with music such as instruments, music theory, and listening to songs. We will talk about the role music has played in our life so far and what we grew up listening to. "
fruit1 = "I like apples grapes watermelon but my friend like peaches."
def main():
    #Only about music
    convo1 = Conversation(prompt)
    test1 = [music1, music2, music3]
    for sentence in test1:
        print(convo1.hear_sentence(sentence))
    #Mitocondria update
    convo2 = Conversation(prompt)
    test2 = [mito1, mito2, mito3]
    print("-------------------TEST2---------------------")
    for sen in test2:
        run = convo2.hear_sentence(sen)
        if run == 1:
            propn = convo2.getPropN()
            print("Nouns: ", propn)
            convo2.addTopic()
        print(run)
    #Completely off topic
    print("-------------------TEST3---------------------")
    convo3 = Conversation(prompt)
    test3 = [music1, shopping1, mito1]
    for sen in test3:
        run = convo3.hear_sentence(sen)
        print(run)
    
main()