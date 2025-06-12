from transformers import GPT2Tokenizer

# Load the GPT-2 tokenizer (same tokenizer used by GPT-3.5 and GPT-4)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Telugu-English mixed script input text
text = """**THELLA KAAGITHAM**
**FIRST HALF**

**Scene 1: Intermediate College Freshers Party**
*   **Summary**: A Freshers party is taking place in an intermediate college in 2024.

**Scene 2: Nani's White Paper Analogy**
*   **Summary**: Nani is shown as a teacher in a 1st-year classroom. As soon as Nani entered the class, all the students became silent and dull. The students loudly asked, "What, sir, is it class again today?" Nani told them, "What I am going to tell you is not a Maths class, but a more important class. Give me that notebook once!" Tearing a white paper from a student's notebook, Nani showed it to the students and asked, "What is this?" A student replied, "White paper, sir." Nani said, "No! This is not white paper... this is your life!" Everyone, all at once, started listening with eagerness. Nani explained, "This intermediate stage is like a pure, clean white paper. But if a red mark falls on this white paper..." He took a red ink pen and put a red dot on the white paper. "Now what are you all seeing? Only that Red mark is visible, everything else disappears. It only has value as long as it is white; if a red mark falls on it, it will no longer have value. Here, Red means wrong. Teenage attracts bad things. At this age, if anyone tells you not to do something, you will do it! If they tell you not to look, you will look! If they tell you not to go, you will go!" Everyone listened intently. Nani continued, "Before you do anything, think ten times if it is right or wrong. If you enter Inter like a white paper and come out as the same white paper, your life will be happy. Otherwise, if any Red mark falls, its effect will last lifelong." The sound of a bus passing by is heard. Nani concluded, "This is not a class I taught; someone named Madhava Rao master taught me this in my intermediate. This is more important to you than the Maths class I teach." Nani placed the white paper on the table. All the children listened attentively. As Nani completed the class and was leaving, a boy caught his hand and said, "Sir, a red mark has fallen in my life, sir!" Nani looked; the student had a troubled expression.

**Scene 3: Transition to Ramu's Past**
*   **Summary**: Nani is going on a bike with the boy behind him, who seems lost. As they ride, three boys are urinating near a roadside wall. Zooming back from those three boys, the year 2004 is shown.

**Scene 4: Introduction of Ramu**
*   **Summary**: Ramu (the Hero) is going on a bicycle. The chain came off; he put sand from the roadside onto the chain and fixed it. Seeing a borewell ahead, he went there, washed his hands, drank water from the borewell, and started from there. While riding, he stopped by the roadside, drank four glasses of water from a cool earthen pot, and continued his journey.

**Scene 5: The Urinating Competition**
*   **Summary**: Ramu stopped his bicycle near a wall, where Shiva is established. Eight of Ramu's friends are waiting there. All ten of them placed two rupees each on a stone. Bondam asked, "Hey, did you bring money for the bet? You know the rules, right? Whoever goes the farthest wins...!" They climbed the wall. Shiva shouted, "1, 2, 3, Engine start." In a back shot, everyone is urinating competitively. Shiva's urine isn't going very far, but Ramu continues to urinate for a long time. After Ramu finishes, Shiva goes and measures everyone's urine. Ramu won. Shiva declared, "Today's urination competition winner is our Ramu!" Everyone placed 20 rupees in Ramu's hand. One person, while giving money, said, "There's no one to beat you in the urination competition, but one day I'll defeat you." Ramu laughed, "Me...? You...?" Seeing Shiva looking dull, Ramu asked, "Hey, why are you so down?" Shiva replied, "My two rupees are gone, right...!" Ramu said, "Hey Shiva... we are best friends...! If I win, you win! Here's half for you... and half for me! Come on, it's time for school." Shiva gave a happy reaction.

**Scene 6: Ramu's Family and the Bet Money**
*   **Summary**: At Ramu's house, Chantamma (Hero's sister-in-law) is packing lunch. Ramu is eating rice gruel, placing a crispy fried rice flour fritter on his rice ball. Suri (Hero's elder brother) enters the house, having fixed his torn slipper with a safety pin. Ramu is getting ready in front of the mirror and asks, "Sister-in-law, the box!" Chantamma ties a kerchief to the lunch box. Meanwhile, Suri approaches Ramu and gives him 10 rupees, saying, "Hey, yesterday you asked for ten rupees to buy some book, right? Here." Ramu refused, "No need, brother, I have it." Suri reacted, "How did you get what you didn't have last night...?" Ramu replied, "I won a bet..." Suri pressed, "What bet...?" Ramu looked around, not knowing what to say, and said, "I can't explain it with my mouth, brother." Chantamma questioned, "A bet that can't be explained with the mouth? What kind of bet is that, Ramu?" Ramu said, "That's just how it is, sister-in-law." Suri told him, "Hey, next time you go to that competition, take me with you... I want to see what you play and how you play." Ramu said, "That's not good to watch, brother. You give the box, sister-in-law." Saying goodbye and leaving, his sister-in-law called him, "Don't forget to do circumambulation at Gnana Saraswati temple." Ramu replied, "I'll do it." Chantamma and Suri reacted.

**Scene 7: Gnana Saraswati Temple Routine**
*   **Summary**: Near the Gnana Saraswati temple, all the students who came there are placing their bags and lunch boxes near a tree resembling a public platform outside the temple.

**Scene 8: Inside the Temple**
*   **Summary**: Shots of people doing circumambulations inside the temple. Shiva told Ramu, "Hey brother-in-law, look how many idiots have come to this temple thinking they'll study well if they do circumambulation." Pointing to a stout girl, Shiva continued, "Look at that Shashikala, she won't get good grades even if she rolls on the ground in devotion, let alone circumambulations." Ramu warned him, "Shut up, someone might hear you!"

**Scene 9: Ramu's Lost Box**
*   **Summary**: Ramu and Shiva came outside. Shiva came to Ramu with his four-cup carrier and asked, "Hey, what are you looking for?" Ramu replied, "I kept my box here, where is it?" Seeing his box far away, he picked it up.

**Scene 10: Maths Class and Shiva's Antics**
*   **Summary**: The scene opens on a board that reads 'Zilla Parishath Unnatha Paathashaala (Zilla Parishad High School)'. In the Tenth Grade A section classroom, all the students are sitting on the floor. The Maths sir is explaining what he wrote on the board: "Functions are of four types...! Into function, onto function, Common function, one one function." Everyone is taking notes. The sir asked, "Everyone has written it down, right?" All at once, students replied, "We have written it, sir." As he erased the board and turned towards the students, seeing Shiva sleeping, Ramu nervously whispered, "Hey... Sir is looking, wake up!" Shiva woke up and looked around. Sir asked, "Hey Shiva, were you sleeping?" Shiva denied, "No, sir..." Sir asked, "Did you write about functions?" Shiva affirmed, "Yes, I wrote it, sir." Sir then challenged him, "Oh, really? Then tell me, how many types of functions are there? And what are their names?" Shiva confidently listed, "Why wouldn't I know, sir? Functions are of many types, Mature function, Marriage function..." Sir was shocked. Shiva continued, "Naming ceremony function, funeral function, and nowadays, they even have 'voni' (half-saree) functions, sir. They're doing that too." Ramu laughed, and all the students in the class laughed. Sir, angrily, asked, "How do you know so much about functions?" Shiva explained, "I go for catering during summer holidays, sir! That's why I know all functions!" Sir came near Shiva and said, "Hold out your hand once." Shiva eagerly extended his hand, asking, "Are you giving a gift, sir?!" Sir hit him with a 'phat' sound, scolding him, "You sleep-faced idiot, you talk about mature functions and half-saree functions as functions...!" The bell rang.

**Scene 11: Lunch Break & Box Swap**
*   **Summary**: On the veranda, groups of four friends are sitting and opening their lunch boxes. Ramu and Shiva are sitting together. Shiva asked, "What curry did your Chantamma cook?" Ramu replied, "Brinjal and chickpeas. What curry do you have?" Shiva said, "Again okra." Ramu questioned, "Okra everyday, man...?" Shiva complained, "Someone told my mom that if you eat okra, you'll study well, man. From that day on, my mom has been killing me with okra fry, okra stew, and okra chutney." Ramu opens his box, and there's chicken curry. Both looked. Shiva said to Ramu, "Hey, you said brinjal and chickpea curry... why is there chicken curry?" Ramu saw it and said, "Looks like the box got swapped at the temple. Let's ask whose it is and return it, poor thing." Shiva countered, "It's chicken curry, man! Let's eat it today and return it tomorrow after washing it." Ramu insisted, "Hey, poor thing, let's give it back!" Shiva argued, "What's there to return? Do you think only our school kids put their boxes at the temple? All school kids put them there. Let's find out tomorrow and give it back." Ramu reacted. Shiva added, "Anyway, forget all this, what comes after 'Ah'...?" Ramu opened his mouth to say "Aaaa...!" and Shiva put a piece of chicken in Ramu's mouth. Shiva asked, "Now tell me, shall we give it back?" Ramu replied, "Let's give it back tomorrow." Both are shown eating chicken curry. Ramu asked, "How do you think it got swapped...?" Shiva suggested, "You and he might have tied the same colored kerchief. He thought it was his box and took yours. Poor fellow, he must be eating your brinjal and chickpea curry."

**Scene 12: Asha's Introduction & Box Swap**
*   **Summary**: In B section, a girl (the Heroine, Asha) opens a box with the same kerchief, revealing her face. Lavanya asked, "Hey, what did your mom pack today? Chicken...? Mutton...? Prawns...?" Asha replied, "I'm tired of eating non-veg everyday... you can eat it today, right?" Lavanya reminded her, "How many times have I told you I shouldn't eat it? We are Brahmins... don't force me... Besides, why don't you gather some courage and tell your dad...! Not to pack non-veg everyday." Asha stated, "Talking back to my dad...! He'll kill me...!" She opens the box, and sees brinjal and chickpea curry inside. Lavanya exclaimed, "There's brinjal and chickpea curry?" Asha commented, "Looks like the box got swapped." Asha looked at the box from side to side, then slowly ate. Asha then said, "Whoever cooked it, it's super good!" She eats it. Lavanya asked, "What are you doing? You don't even know whose box it is." Asha declared, "It's super good, I'll eat this today!" As Asha eats it with enjoyment, Lavanya's mouth watered a little. Lavanya asked, "Hey... is it that good? Give me some." She pushed her plate. Asha reacted, and both are shown eating.

**Scene 13: Intentional Box Swap**
*   **Summary**: Next day, at the temple, Asha and Lavanya are waiting, looking at everyone's boxes. Asha sees Ramu for the first time, who just arrived with a box tied with the same kerchief. Lavanya also notices that kerchief. Lavanya points him out, "There he comes, wearing a kerchief like yours." Asha identifies him, "He's an A-Section student, isn't he...!" Lavanya confirmed, "Yes, go tell him the box got swapped and return it...!" Asha refused, "I won't give it back...!" Lavanya pressed, "You won't...!? What will you do if you don't give it back...?" Asha declared, "Yesterday it got swapped accidentally, today I'll swap it myself." Lavanya asked, "Why...?" Asha replied, "I became a fan of their mom's curry!" Lavanya jokingly asked, "Are there fans even for brinjal and chickpea curry...!?" As soon as Ramu and Shiva put their boxes there and went inside, Asha swaps the boxes. Asha and Lavanya both left from there. Ramu and Shiva came out of the temple. Ramu was looking around, and Shiva asked, "What are you looking for, man?" Ramu replied, "I'm looking for whose box got swapped yesterday." Shiva said, "Looks like he didn't come today!" Ramu took the box Asha had placed.

**Scene 14: Unit Test Results**
*   **Summary**: In B section, Sir entered the class with exam papers. Daridram Sir announced, "I will read your unit test marks, listen once... 1, 1, 1... 2, 2, 2... 3, 3, 5, 6, 6, 7. It's a misery that I'm reading your marks like Sri Chaitanya and Narayana read ranks on TV. Don't stay in B section, go to A section, you miserable lot... go and die sharing it." He threw them away. Lavanya is happy. Daridram Sir asked her, "What's the matter, girl, you're so happy, how many marks did you get?" Lavanya replied, "I got 5 marks, sir." Daridram Sir mocked, "So much happiness for those beggarly marks...? Misery...!" Lavanya countered, "Last time I got three marks, sir." Sir reacted.

**Scene 15: Mutton Curry & The First Letter**
*   **Summary**: Ramu opens the box and exclaims, "Hey, the box got swapped again." Feeling happy, Shiva asked, "It got swapped...? See what curry it is...!" Ramu opened the kerchief and saw, "It's mutton curry!" Shiva shouted loudly, "Yahoo...!" Everyone looked. There's a letter inside. Ramu says, "There's a letter in this, man...!" Daridram Sir took that letter and read it. Asha's letter read: "Hi... your mother cooked the curry very well, tell her thanks from me... at my house, they give me non-veg every day, I don't like non-veg much. If you like, let's swap boxes every day... is that okay for you..?" Ramu reacted.

**Scene 16: Ramu's Thanks to Chantamma**
*   **Summary**: At home, Ramu said, "Sister-in-law, thanks!" Chantamma asked, "Why thanks to me?" Ramu replied, "You cooked the curry very well, my friend liked it a lot." Chantamma smiled.

**Scene 17: Asha Reads Ramu's Letter**
*   **Summary**: Next day, during lunch break, Asha is reading the letter. Ramu's letter read: "Hello, I don't have a mother or father...! My mother and father passed away when I was young. My sister-in-law cooked that curry. I told my sister-in-law thanks." Asha said, "Poor boy, he doesn't have a mother or father...!" Lavanya asked, "What else did he write...?" She took the letter and looked. Lavanya's voice read: "I like swapping boxes, but please bring a little more curry when you bring it... because my friend Shiva also eats with me." Lavanya commented, "What, he's asking to bring for his friend too?" Asha said, "It's okay, my mom cooks anyway, I'll ask her to put a little more." She took the letter from Lavanya's hand and read it. Ramu's letter asked: "By the way, are you a girl or a boy? What's your name?" Asha reacted.

**Scene 18: Seeking the Identity**
*   **Summary**: Ramu is reading a letter. Ramu's voice read: "If you want to know who I am and what I am, I won't swap boxes from tomorrow. Now it's your wish." After reading, Shiva said to Ramu, "Why do we need names or schools, man...? Chicken and mutton are important to us...! What curry is it today?" Ramu replied, "Prawn fry." Shiva exclaimed, "Eureka."

**Scene 19: Shower Talk**
*   **Summary**: Near the tank, Ramu is pumping water while washing boxes, and Shiva is washing boxes. Shiva asked, "Why do you need her name, man..?" Ramu said, "Hey, is the one swapping the box a boy or a girl!? I want to know." Asha interjected, "Hey boy... how long will you wash? If you leave, we can wash." Ramu replied, "Just one moment, girl..! Hey, wash quickly...!" Shiva washed the box, and as they were leaving, Lavanya asked, "How many days will these hide-and-seek games go on?" Asha replied, "It's good, isn't it? Let's play until we get caught." Shiva told Ramu, "Do you know why I come to school every day, brother-in-law? It's this box! Because of this box, I doubt if I'll study well and become class first like you...!" Ramu looked at him.

**Scene 20: "Vaani" Revealed**
*   **Summary**: Chantamma is washing Ramu's lunch box at home. Suddenly, she saw the box and called, "Ramu...." Ramu asked, "What is it, sister-in-law...?" Chantamma said, "Looks like your box got swapped..." Ramu reacted. Ramu asked, "How did you know, sister-in-law?" Chantamma explained, "There's a name 'Vaani' written on the back. I think it belongs to some girl...?" As she said that, Ramu took the box and saw "Vaani" written on it. Ramu reacted.

**Scene 21: Asha's Explanation for 'Vaani'**
*   **Summary**: The next day, as usual during lunch break, Asha and Lavanya are reading the letter sent by Ramu. Ramu's letter read: "Hey...! Did you think I couldn't find out your name even if you didn't tell me? Your name is 'Vaani'. Your name is very nice." Immediately, Lavanya said with a slight shock, "Your name is Vaani, what's this...?" Asha thought for a moment and explained to Lavanya, "This is the box my neighbor Vaani akka gave me during her mature function, that's why her name is written below... he thinks it's my name seeing that." Ramu's letter continued: "I found out your name, I will also find out your school." Asha said, "Find out.. find out..!" Asha smiles.

**Scene 22: Ramu's Search for Asha (Musical Bit)**
*   **Summary**: A montage shows Asha regularly swapping Ramu's lunch box at Gnana Saraswati temple, set to a love song. Cut shots show this happening daily.

**Scene 23: Ramu and Shiva's Search**
*   **Summary**: Montages show Ramu and Shiva searching for Asha, including checking Asha's name in the register.

**Scene 24: Expanding the Search**
*   **Summary**: Montages show Ramu and Shiva observing all the lunch boxes kept in a room in another school, in their search for Asha.

**Scene 25: Looking for Kerchiefs**
*   **Summary**: Montages show Ramu and Shiva observing the kerchiefs tied to girls' lunch boxes while they are eating lunch, still searching for Asha. Ramu is shown not finding a box with his kerchief color.

**Scene 26: Asha Hiding**
*   **Summary**: Montages show Ramu and Shiva observing the boxes in the hands of girl students coming to the temple. Asha is shown hiding and smiling while looking at Ramu.

**Scene 27: Asking Around**
*   **Summary**: Montages show Ramu and Shiva standing near a chicken shop and asking, "What's your daughter's name?" Asha is shown laughing seeing this.

**Scene 28: The 'Chicken Curry Cut' Warning**
*   **Summary**: Ramu is shown looking from behind a tree to see who is swapping the box. Asha notices this and drops a letter among the students when they all arrive. Ramu picks it up and reads: "If you try to see me, your chicken curry will be cut." Shiva exclaimed, "Hey... is it necessary, man...? My mom cooks chicken twice a year if I ask her to, and she brings it for us every day. You'll disturb such a goddess, man...! Your eggs will go bad, man...! Not eye-balls, but chicken eggs..."

**Scene 29: The Two Shirts**
*   **Summary**: Ramu is reading a letter that says, "Why do you always wear those two shirts, don't you have other shirts...?"

**Scene 30: Ramu's Response**
*   **Summary**: Asha is reading a letter from Ramu: "My elder brother buys one dress for every festival. The ones I'm wearing now were bought like that. If I want to wear a new shirt, a festival has to come..."

**Scene 31: The Broken Piggy Bank**
*   **Summary**: At Asha's house, her piggy bank broke.

**Scene 32: Buying a Shirt for Ramu**
*   **Summary**: Asha and Lavanya are in a shop. Lavanya asked, "Hey, the curry is fine... but is it necessary to buy a shirt for him? Do you understand what will happen if your dad finds out all this...?" Asha replied, "Hey... don't scare me.." She put that shirt in a cover.

**Scene 33: The Gift Hint**
*   **Summary**: Ramu is reading a letter that says, "I kept a gift for you in a red cover behind the hundi (donation box) of Gnana Saraswati temple. Go."

**Scene 34: Ramu Finds the Gift**
*   **Summary**: Ramu took the cover from behind the hundi, and there was a shirt inside. Ramu feels happy.

**Scene 35: Torn Kerchief**
*   **Summary**: Montages show Ramu looking at the lunch boxes of some girls cycling towards him. He falls into a nearby ditch, tearing the kerchief tied to his lunch box. Half of the song finishes.

**Scene 36: Shiva's Marks**
*   **Summary**: As Ramu took the torn kerchief and went to Shiva's place, Shiva's mother was severely beating him. She screamed, "You thought I wouldn't find out if you put a 0 next to 9, huh...!" Ramu went and asked, "Why are you hitting Shiva, auntie?" She explained, "He got 9 marks and put a zero next to it, bringing it as 90! Will he get 90 marks for his studies...!?" She hits him repeatedly. Shiva protested, "I didn't put a 0 next to 9...! Believe me!" Ramu pulls Shiva aside. Ramu asked, "Hey, how did you get 90 marks without putting a 0 next to 9? Why did you put it?" Shiva admitted, "I didn't put a 0 next to 9, man... I put a 9 next to 0..." Ramu clarified, "So what did you get?" Shiva replied, "0. I was trying to tell her this, but my mom isn't listening..." Ramu reacted. Seeing the torn kerchief, Shiva asked Ramu, "Hey, why is the kerchief torn?"

**Scene 37: Searching for a Kerchief**
*   **Summary**: Ramu and Shiva went into the market together. Ramu asked a shopkeeper, "Brother... do you have a kerchief like this...?" The shopkeeper replied, "No, young man..."

**Scene 38: Still Searching**
*   **Summary**: In another shop, Shiva asked, "Uncle, sir, do you have a kerchief like this in your shop?" The shopkeeper replied, "No."

**Scene 39: More Shops, No Luck**
*   **Summary**: Cuts show them trying other shops, always getting the answer "No... no."

**Scene 40: Fear of Losing Connection**
*   **Summary**: Ramu told Shiva, "Hey Shiva... if we don't find a kerchief like this, the connection with Vaani will be lost, man. I'm afraid I won't know who Vaani is in my life anymore...!" Ramu reacted.

**Scene 41: Murthy's Weighing Obsession**
*   **Summary**: Asha's father Murthy is introduced. Murthy went to the mirror, clean-shaved and neatly trimmed his mustache. As Asha comes from the bedroom with her bag, Murthy sees her and says, "Girl." Asha asks, "What is it, Dad?" Turning to Lakshmi, Murthy says, "Hey... bring the weighing machine...?" Lakshmi replies, "I'm bringing it!" Murthy asks, "You're giving chicken and mutton every day, right?" Lakshmi affirms, "Yes, I am!" Murthy then says, "Then her weight must have increased, step on it, girl." Asha stepped onto the weighing machine. Murthy asked, "How much was it last month...?" Lakshmi replied, "48, sir..." Asha stood on the weighing machine. Seeing the weight, Murthy asked, "Are you eating what's given to you, or are you giving it to your friends..?" Asha said, "I'm eating it myself, Dad...!" Just then Lavanya came, saying "Hi uncle...!" She saw the machine and stepped on it. The reading showed 65. Lavanya exclaimed, "Hey... 65 kgs... increased by three kgs...!" Murthy was shocked and asked, "Could she be eating it all...?" Lakshmi explained, "She's the teacher's daughter, sir!"

**Scene 42: Murthy's Doubts**
*   **Summary**: Asha went to her bicycle. Murthy called Lavanya, "Lavanya!" Coming somewhat fearfully and curiously, Lavanya asked, "Yes, uncle, sir..." Murthy questioned, "Is your friend eating what's given to her, or is she giving it to someone else?" Lavanya replied, "My friend is eating it herself, uncle, sir." Murthy added, "Your friend fainted the other day, right? When we showed her to the doctor, they said her blood count was low, that's why we're giving her all this. Tell her to eat." Lavanya said, "Okay, uncle, sir." Murthy then asked, "Are you making friends with boys...?" Fearfully, Lavanya said, "No, uncle, sir." Murthy warned, "Don't." Lavanya nodded her head in fear. Murthy said, "Go." Lavanya left fearfully.

**Scene 43: The Torn Kerchief Plan**
*   **Summary**: The next day, Ramu stands outside the temple, tying a new kerchief to the box. Ramu exclaimed, "I understood how to find Vaani!" Saying this, Ramu is tearing the new kerchief. Shiva asked, "What are you doing, man? Hey, we searched the whole town and finally found it in one shop, why are you tearing it...?" Ramu then planned to put the box there and go inside the temple to do circumambulations, hoping the box will be swapped by the time he returns. Ramu explained, "It's the fear that the connection will be cut if the kerchief is torn, right? That's why we searched the whole town and bought this!" Shiva agreed, "Yes...!" Ramu continued, "If she has the same fear as me, that the connection will be cut if the kerchief is torn, then she will search the whole town like us and come to that shop, and we'll find her there." Shiva exclaimed, "Super idea, man!"

**Scene 44: Asha Sees the Torn Kerchief**
*   **Summary**: Asha opened the box during lunch time, and seeing the kerchief tied to the box was torn, Asha thinks.

**Scene 45: The Power Cut and Missing Asha**
*   **Summary**: Far outside the kerchief shop, Ramu and Shiva are waiting. No customers are buying kerchiefs in the shop; they are buying other things. Two girls came on a bicycle. Lavanya asked, "How many more shops will we search? Let's go home...!" Saying this, they went to a shop nearby. As they arrived, Ramu shouted, "Girls have come, girls have come, man!" Those girls went into the kerchief shop. Asha asked, "Uncle, if you have a kerchief like this, please give it...!" Ramu excitedly said, "Hey... they came to buy kerchiefs, man... It's Vaani, man...!" Just then, the power went out. Ramu exclaimed, "Why did the power go out exactly when I was about to see her face...!" "Come on...!" Those girls took the kerchief and left on their bicycles.

**Scene 46: The Reveal: Asha**
*   **Summary**: Ramu and Shiva cycle fast behind them. Ramu shouted, "Hey Vaani! Did you think I wouldn't find you? I know it's you playing hide-and-seek with me, stop..!" Lavanya told Asha, "This is all his plan! You got caught unnecessarily...!" Asha urged, "Cycle faster...!" They are cycling fast. Ramu cycles fast and stops in front of them. It's all dark, and Ramu can't see Asha's face. Ramu immediately puts the stand on his cycle and pumps the pedal. The cycle light flickers and shines. In that light, Ramu sees Asha. Shiva, who is nearby, sees Lavanya and exclaims, "They're from our school, man! B-section girls.!" To Shiva, Ramu muttered, "There's no girl named Vaani in the B-section register, right...!" Seeing Asha going on her cycle, Ramu asked, "Hey... what's your name...?" Asha turns back and replies, "Asha..." Saying this, she leaves. Ramu repeated, "Asha..." Ramu smiled, leading into a song.

**Scene 47: Ramu's Failed Attempt to Change Sections**
*   **Summary**: Ramu has drawn flames. A one-sided love song continues. Ramu and Asha are shown swapping lunch boxes at school. Since Asha is in a different section, Ramu is unable to see her all day, and Ramu feels sad. Ramu and Shiva plan to fail exams and go to B-section. Ramu declares, "Somehow, I have to go to B-section, man!" Shiva asks, "How will you go, man? You have to fail all subjects, right?" Ramu gives a cunning smile. Ramu and Shiva only wrote answers to half of the questions in the exams. They fail. Shiva's mother, for Shiva failing, screams, "You'll fail all subjects, man...!" She dragged Shiva off the bed and kicked him.

**Scene 48: The Malaria Excuse**
*   **Summary**: Daridram Sir asks Ramu, "You are class first, aren't you, you miserable one? Why did you fail..?" Ramu replies, "I have malaria, sir...!" Daridram Sir asks Shiva, "What about you...?" Shiva replies, "I also have malaria, sir...!" Daridram Sir asks, "How did both of you get malaria at the same time, you miserable lot..?" Shiva explains, "We live in the same area, sir, miserable...!" Daridram Sir then shouts, "What are you still looking at? Go to B-Section!" As he was leaving, Asha and Lavanya just arrived at A-Section. Asha (voice) asks, "May I come in, sir?" Daridram Sir asks, "Who are you, girls..?" Asha replies, "We passed all subjects, sir, they sent us to A-Section!" Ramu & Shiva are shocked; as Asha and Lavanya enter, Ramu and Shiva are leaving. Ramu and Shiva's reaction is shown.

**Scene 49: Re-taking Exams**
*   **Summary**: Cuts show Ramu and Shiva taking exams again after failing.

**Scene 50: Back to A-Section**
*   **Summary**: Ramu and Shiva passed and came to A section.

**Scene 51: The 'Aha Konda' Revelation**
*   **Summary**: Shiva and Ramu take Asha and Lavanya to Aha Konda. Ramu announces, "This is Aha Konda..." Asha asks, "Aha Konda! What's so amazing about this hill to make one say 'aha'..?" Ramu and Shiva laugh. Ramu explains, "Aha Konda doesn't mean it's an amazing hill, but a Suicide Hill. No one who jumped from here survived; they died on the spot. That's why we call it Aha Konda as a shortcut." Asha reacts in shock. Shiva tells Ramu, "Hey... I'm going to Bezawada uncle's place... if sir asks, tell him something." Ramu asks, "Should I say stomach ache?" Shiva replies, "They won't believe stomach ache, man... it's a week-long holiday, so tell him something else." Ramu reacts.

**Scene 52: Shiva's "Mature" Status**
*   **Summary**: At school, Ramu, with Asha, asks, "Lavanya, why didn't she come...?" Asha replies, "Lavanya matured... she won't come for another week." Sir lifts Ramu up and asks, "Hey...? Why didn't your friend Shiva come?" Ramu replies, "He matured, sir." Daridram Sir asks, "He matured...?" Ramu confirms, "Yes, sir, he won't come for a week." All the girls laughed. Seeing Asha laugh, Ramu reacts.

**Scene 53: Ramu and Asha's Growing Proximity**
*   **Summary**: A montage shows Ramu explaining Maths doubts to Asha.

**Scene 54: Eating Together**
*   **Summary**: A montage shows Ramu and Asha eating together.

**Scene 55: Parking Cycles Together**
*   **Summary**: A montage shows Ramu and Asha parking their cycles in the same spot.

**Scene 56: Shiva's Mature Function & Farewell Day Announcement**
*   **Summary**: Daridram Master entered the class. Seeing Shiva, everyone was laughing. Shiva asked Ramu, "Hey, why is everyone laughing looking at me..?" Ramu replied, "I don't know, man..." The Master stood in front of Shiva and asked, "Hey, I heard you matured. When's the function..?" Everyone is laughing. Shiva complained, "Hey, couldn't you find any other reason, man? You said I matured..." Daridram Sir then mockingly asked, "Are you serving chicken or mutton in the meals, you wretch..? Come and show up in the staff room during lunch break, sit down..." Just then a circular arrived. Daridram Sir announced, "This time for farewell day, the classroom needs to be decorated. Those interested, stand up!" Asha stood up. Seeing Asha, Ramu stood up. Seeing these two, Shiva and Lavanya also stood up. Daridram Sir continued, "The budget is 500 rupees. Whatever you buy, you must buy it with these 500 rupees..! Go and buy it after school in the evening."

**Scene 57: Ramu Asks About Maturity**
*   **Summary**: Ramu came home and asked, "Brother, what does mature mean?" Suri, eating rice, replied, "Why do you care about all that, man! Exams are approaching, study!" Ramu insisted, "That's not it, brother! Don't men mature?" Suri questioned, "Who is teaching you all this?" He left. Chantamma asked, "What happened?" Ramu then asked Chantamma, "Sister-in-law, do men mature too?" Chantamma asked, "Why did you ask that?" Ramu explained, "Nothing. In class, I lied that Shiva matured because he didn't come for a week, and everyone laughed. No one is telling me why. You tell me, sister-in-law, do women mature, or do men not?" Chantamma said, "Men also mature." Ramu asked, "When?" Chantamma replied, "When men understand women's pain even if they don't express it verbally, then men mature." Ramu sighed, "Oh! Then I haven't matured yet, sister-in-law." Chantamma reassured him, "You'll go to intermediate in another two months, right? You'll mature then!"

**Scene 58: Decoration Shopping**
*   **Summary**: A montage shows them buying decoration materials. As Asha points to something and tells him, Ramu just nods 'hmm'.

**Scene 59: Balloons Needed**
*   **Summary**: Lavanya exclaimed, "Hey idiots, we bought everything but forgot the main thing, man. We didn't buy balloons, go and bring them." Ramu said, "What's there to buy? The money Master gave is long gone..." Asha offered, "What's wrong with that? I'll give it." Lavanya countered, "You stay there, he's the one who miscalculated, he'll buy them. Hey, will you buy them..?" Ramu agreed, "I will." Asha started to protest, "Wrong..." Lavanya cut her off, "No wrong or right, come on."

**Scene 60: Ramu's Balloon Dilemma**
*   **Summary**: In the morning, Ramu is brushing his teeth and thinks to himself, "If I ask if I have money, he might hit me. No one is coming for the urination competitions either. If I don't buy balloons, I'll lose face with Asha. What should I do?" A slum boy (Bulliraju) has three large white balloons. Ramu immediately stops brushing, quickly washes his mouth, and asks, "Hey, where did you buy so many balloons?" Bulliraju replies, "Didn't buy!" Ramu asks, "Didn't buy...? Who gave them to you if you didn't buy them?" Bulliraju says, "No one gave them... I took them myself!" Ramu asks, "You took them? Where?" Bulliraju replies, "What will you give me if I tell you where?" Ramu says, "I'll give you a rupee...!" Bulliraju says, "I don't want a rupee, I'll tell you if you give me half a rupee." Ramu then follows Bulliraju.

**Scene 61: Balloons from a Condom Pack**
*   **Summary**: Ramu and Bulliraju are walking. Ramu asks, "How do you know that half a rupee is more than a rupee..?" Bulliraju explains, "Two half rupees come for one rupee, but one rupee comes for two half rupees... that's when I knew half a rupee is bigger." Ramu comments, "You're not an ordinary guy, man..." Bulliraju brought him to a government hospital, showed him a Nirodh box, and said, "They are in this." Ramu put his hand in and asked, "In this packet...?" Bulliraju said, "If you tear that, there will be a balloon inside. Take as many as you want... no one will ask." As Ramu was putting condom packets into his pocket, a nurse saw him taking so many condoms and was shocked, looking with lust. Ramu thought, "Why is she looking at me like that?" Thinking this, he takes a few more and starts to leave. The nurse stops him and asks, "Why are you taking so many, boy?" Ramu replies, "To tell the truth, even all these won't be enough for me, madam!" The nurse is shocked. Ramu is leaving. The nurse asks, "What will you do with all of them, boy?" Ramu retorts, "Don't you know what we do, madam? Why are you asking like it's new?" The nurse reacts in shock.

**Scene 62: The Balloons and Decoration**
*   **Summary**: Ramu tore about 50 balloon covers, brought them in a box, and placed them in front of everyone. Asha asked, "Where did you buy so many balloons?" Ramu replied, "Didn't buy." Lavanya then asked, "Then?" In his mind, Ramu thought, "It might not be good to say I brought them from the hospital." He said aloud, "My elder brother's friend has a balloon shop, he gave them to me for free." Lavanya asked, "Why did you bring all one color? Don't they have other colors?" Ramu said, "They said stock was over, only these were left...!" Shiva looked a bit doubtfully. Ramu asked, "Hey, why are you looking like that?" Shiva questioned, "Did your brother's friend really give these?" Ramu affirmed, "Yes, you blow them... blow them..." Shiva then asked, "Hey, why is it sticky?" Ramu admitted, "I forgot to tell you, you have to wash them and then blow them." As Shiva blew, Asha poured colored water into them and made them more beautiful, designing them like grapes. While decorating, Asha was about to fall, and Ramu caught her. Asha felt a little something. Ramu had a slight tremor. Both were sweating even though they were sitting under a fan. A small feeling was generated. The room decoration was finished. A shot of the 10th class farewell photo is shown, from close-up to on the wall.

**Scene 63: Fake Weight Gain**
*   **Summary**: Zooming back from the 10th class photo, Asha is in college dress, with Lavanya next to her. Lavanya took out one 2 kg weight and two 1 kg weights from her bag. Asha asked, "What is this..?" Lavanya explained, "If you don't gain weight, your dad won't say anything to you, but he'll scold me. Where's your bag..?" She put them in the bag and zipped it. As they came outside, Murthy was weighing someone with the weighing machine. As Asha was about to step on the machine, Murthy said, "Girl... take off your bag and step on it, girl..." Lavanya interjected, "Why, uncle? At most, it'll increase by half a kg, step on it with the bag..." Asha stepped on it, and it showed 52 kgs. Murthy is happy. Lavanya exclaimed, "See, uncle, she gained four kgs!" Murthy said, "Yes... yes... from now on, I won't give you chicken and mutton if you don't like it, dear. Intermediate is a very important stage, study well, dear." Asha said, "Okay, Dad... let's go." Both left. Her mother (Lakshmi) came and asked, "Honey... the girl still looks like a bird, how did she gain four kgs...?" Thinking, Murthy replied, "Bone weight..." Her mother reacted.

**Scene 6
Here's a detailed, scene-wise extractive summary of the provided screenplay chunk for 'Thella Kaagitham,' with all key sentences translated into standard English:

---

**THELLA KAAGITHAM**
**FIRST HALF**

**Scene 1: Intermediate College Freshers Party**
*   **Summary**: A Freshers party is taking place in an intermediate college in 2024.

**Scene 2: Nani's White Paper Analogy**
*   **Summary**: Nani is shown as a teacher in a 1st-year classroom. As soon as Nani entered the class, all the students became silent and dull. The students loudly asked, "What, sir, is it class again today?" Nani told them, "What I am going to tell you is not a Maths class, but a more important class. Give me that notebook once!" Tearing a white paper from a student's notebook, Nani showed it to the students and asked, "What is this?" A student replied, "White paper, sir." Nani said, "No! This is not white paper... this is your life!" Everyone, all at once, started listening with eagerness. Nani explained, "This intermediate stage is like a pure, clean white paper. But if a red mark falls on this white paper..." He took a red ink pen and put a red dot on the white paper. "Now what are you all seeing? Only that Red mark is visible, everything else disappears. It only has value as long as it is white; if a red mark falls on it, it will no longer have value. Here, Red means wrong. Teenage attracts bad things. At this age, if anyone tells you not to do something, you will do it! If they tell you not to look, you will look! If they tell you not to go, you will go!" Everyone listened intently. Nani continued, "Before you do anything, think ten times if it is right or wrong. If you enter Inter like a white paper and come out as the same white paper, your life will be happy. Otherwise, if any Red mark falls, its effect will last lifelong." The sound of a bus passing by is heard. Nani concluded, "This is not a class I taught; someone named Madhava Rao master taught me this in my intermediate. This is more important to you than the Maths class I teach." Nani placed the white paper on the table. All the children listened attentively. As Nani completed the class and was leaving, a boy caught his hand and said, "Sir, a red mark has fallen in my life, sir!" Nani looked; the student had a troubled expression.

**Scene 3: Transition to Ramu's Past**
*   **Summary**: Nani is going on a bike with the boy behind him, who seems lost. As they ride, three boys are urinating near a roadside wall. Zooming back from those three boys, the year 2004 is shown.

**Scene 4: Introduction of Ramu**
*   **Summary**: Ramu (the Hero) is going on a bicycle. The chain came off; he put sand from the roadside onto the chain and fixed it. Seeing a borewell ahead, he went there, washed his hands, drank water from the borewell, and started from there. While riding, he stopped by the roadside, drank four glasses of water from a cool earthen pot, and continued his journey.

**Scene 5: The Urinating Competition**
*   **Summary**: Ramu stopped his bicycle near a wall, where Shiva is established. Eight of Ramu's friends are waiting there. All ten of them placed two rupees each on a stone. Bondam asked, "Hey, did you bring money for the bet? You know the rules, right? Whoever goes the farthest wins...!" They climbed the wall. Shiva shouted, "1, 2, 3, Engine start." In a back shot, everyone is urinating competitively. Shiva's urine isn't going very far, but Ramu continues to urinate for a long time. After Ramu finishes, Shiva goes and measures everyone's urine. Ramu won. Shiva declared, "Today's urination competition winner is our Ramu!" Everyone placed 20 rupees in Ramu's hand. One person, while giving money, said, "There's no one to beat you in the urination competition, but one day I'll defeat you." Ramu laughed, "Me...? You...?" Seeing Shiva looking dull, Ramu asked, "Hey, why are you so down?" Shiva replied, "My two rupees are gone, right...!" Ramu said, "Hey Shiva... we are best friends...! If I win, you win! Here's half for you... and half for me! Come on, it's time for school." Shiva gave a happy reaction.

**Scene 6: Ramu's Family and the Bet Money**
*   **Summary**: At Ramu's house, Chantamma (Hero's sister-in-law) is packing lunch. Ramu is eating rice gruel, placing a crispy fried rice flour fritter on his rice ball. Suri (Hero's elder brother) enters the house, having fixed his torn slipper with a safety pin. Ramu is getting ready in front of the mirror and asks, "Sister-in-law, the box!" Chantamma ties a kerchief to the lunch box. Meanwhile, Suri approaches Ramu and gives him 10 rupees, saying, "Hey, yesterday you asked for ten rupees to buy some book, right? Here." Ramu refused, "No need, brother, I have it." Suri reacted, "How did you get what you didn't have last night...?" Ramu replied, "I won a bet..." Suri pressed, "What bet...?" Ramu looked around, not knowing what to say, and said, "I can't explain it with my mouth, brother." Chantamma questioned, "A bet that can't be explained with the mouth? What kind of bet is that, Ramu?" Ramu said, "That's just how it is, sister-in-law." Suri told him, "Hey, next time you go to that competition, take me with you... I want to see what you play and how you play." Ramu said, "That's not good to watch, brother. You give the box, sister-in-law." Saying goodbye and leaving, his sister-in-law called him, "Don't forget to do circumambulation at Gnana Saraswati temple." Ramu replied, "I'll do it." Chantamma and Suri reacted.

**Scene 7: Gnana Saraswati Temple Routine**
*   **Summary**: Near the Gnana Saraswati temple, all the students who came there are placing their bags and lunch boxes near a tree resembling a public platform outside the temple.

**Scene 8: Inside the Temple**
*   **Summary**: Shots of people doing circumambulations inside the temple. Shiva told Ramu, "Hey brother-in-law, look how many idiots have come to this temple thinking they'll study well if they do circumambulation." Pointing to a stout girl, Shiva continued, "Look at that Shashikala, she won't get good grades even if she rolls on the ground in devotion, let alone circumambulations." Ramu warned him, "Shut up, someone might hear you!"

**Scene 9: Ramu's Lost Box**
*   **Summary**: Ramu and Shiva came outside. Shiva came to Ramu with his four-cup carrier and asked, "Hey, what are you looking for?" Ramu replied, "I kept my box here, where is it?" Seeing his box far away, he picked it up.

**Scene 10: Maths Class and Shiva's Antics**
*   **Summary**: The scene opens on a board that reads 'Zilla Parishath Unnatha Paathashaala (Zilla Parishad High School)'. In the Tenth Grade A section classroom, all the students are sitting on the floor. The Maths sir is explaining what he wrote on the board: "Functions are of four types...! Into function, onto function, Common function, one one function." Everyone is taking notes. The sir asked, "Everyone has written it down, right?" All at once, students replied, "We have written it, sir." As he erased the board and turned towards the students, seeing Shiva sleeping, Ramu nervously whispered, "Hey... Sir is looking, wake up!" Shiva woke up and looked around. Sir asked, "Hey Shiva, were you sleeping?" Shiva denied, "No, sir..." Sir asked, "Did you write about functions?" Shiva affirmed, "Yes, I wrote it, sir." Sir then challenged him, "Oh, really? Then tell me, how many types of functions are there? And what are their names?" Shiva confidently listed, "Why wouldn't I know, sir? Functions are of many types, Mature function, Marriage function..." Sir was shocked. Shiva continued, "Naming ceremony function, funeral function, and nowadays, they even have 'voni' (half-saree) functions, sir. They're doing that too." Ramu laughed, and all the students in the class laughed. Sir, angrily, asked, "How do you know so much about functions?" Shiva explained, "I go for catering during summer holidays, sir! That's why I know all functions!" Sir came near Shiva and said, "Hold out your hand once." Shiva eagerly extended his hand, asking, "Are you giving a gift, sir?!" Sir hit him with a 'phat' sound, scolding him, "You sleep-faced idiot, you talk about mature functions and half-saree functions as functions...!" The bell rang.

**Scene 11: Lunch Break & Box Swap**
*   **Summary**: On the veranda, groups of four friends are sitting and opening their lunch boxes. Ramu and Shiva are sitting together. Shiva asked, "What curry did your Chantamma cook?" Ramu replied, "Brinjal and chickpeas. What curry do you have?" Shiva said, "Again okra." Ramu questioned, "Okra everyday, man...?" Shiva complained, "Someone told my mom that if you eat okra, you'll study well, man. From that day on, my mom has been killing me with okra fry, okra stew, and okra chutney." Ramu opens his box, and there's chicken curry. Both looked. Shiva said to Ramu, "Hey, you said brinjal and chickpea curry... why is there chicken curry?" Ramu saw it and said, "Looks like the box got swapped at the temple. Let's ask whose it is and return it, poor thing." Shiva countered, "It's chicken curry, man! Let's eat it today and return it tomorrow after washing it." Ramu insisted, "Hey, poor thing, let's give it back!" Shiva argued, "What's there to return? Do you think only our school kids put their boxes at the temple? All school kids put them there. Let's find out tomorrow and give it back." Ramu reacted. Shiva added, "Anyway, forget all this, what comes after 'Ah'...?" Ramu opened his mouth to say "Aaaa...!" and Shiva put a piece of chicken in Ramu's mouth. Shiva asked, "Now tell me, shall we give it back?" Ramu replied, "Let's give it back tomorrow." Both are shown eating chicken curry. Ramu asked, "How do you think it got swapped...?" Shiva suggested, "You and he might have tied the same colored kerchief. He thought it was his box and took yours. Poor fellow, he must be eating your brinjal and chickpea curry."

**Scene 12: Asha's Introduction & Box Swap**
*   **Summary**: In B section, a girl (the Heroine, Asha) opens a box with the same kerchief, revealing her face. Lavanya asked, "Hey, what did your mom pack today? Chicken...? Mutton...? Prawns...?" Asha replied, "I'm tired of eating non-veg everyday... you can eat it today, right?" Lavanya reminded her, "How many times have I told you I shouldn't eat it? We are Brahmins... don't force me... Besides, why don't you gather some courage and tell your dad...! Not to pack non-veg everyday." Asha stated, "Talking back to my dad...! He'll kill me...!" She opens the box, and sees brinjal and chickpea curry inside. Lavanya exclaimed, "There's brinjal and chickpea curry?" Asha commented, "Looks like the box got swapped." Asha looked at the box from side to side, then slowly ate. Asha then said, "Whoever cooked it, it's super good!" She eats it. Lavanya asked, "What are you doing? You don't even know whose box it is." Asha declared, "It's super good, I'll eat this today!" As Asha eats it with enjoyment, Lavanya's mouth watered a little. Lavanya asked, "Hey... is it that good? Give me some." She pushed her plate. Asha reacted, and both are shown eating.

**Scene 13: Intentional Box Swap**
*   **Summary**: Next day, at the temple, Asha and Lavanya are waiting, looking at everyone's boxes. Asha sees Ramu for the first time, who just arrived with a box tied with the same kerchief. Lavanya also notices that kerchief. Lavanya points him out, "There he comes, wearing a kerchief like yours." Asha identifies him, "He's an A-Section student, isn't he...!" Lavanya confirmed, "Yes, go tell him the box got swapped and return it...!" Asha refused, "I won't give it back...!" Lavanya pressed, "You won't...!? What will you do if you don't give it back...?" Asha declared, "Yesterday it got swapped accidentally, today I'll swap it myself." Lavanya asked, "Why...?" Asha replied, "I became a fan of their mom's curry!" Lavanya jokingly asked, "Are there fans even for brinjal and chickpea curry...!?" As soon as Ramu and Shiva put their boxes there and went inside, Asha swaps the boxes. Asha and Lavanya both left from there. Ramu and Shiva came out of the temple. Ramu was looking around, and Shiva asked, "What are you looking for, man?" Ramu replied, "I'm looking for whose box got swapped yesterday." Shiva said, "Looks like he didn't come today!" Ramu took the box Asha had placed.

**Scene 14: Unit Test Results**
*   **Summary**: In B section, Sir entered the class with exam papers. Daridram Sir announced, "I will read your unit test marks, listen once... 1, 1, 1... 2, 2, 2... 3, 3, 5, 6, 6, 7. It's a misery that I'm reading your marks like Sri Chaitanya and Narayana read ranks on TV. Don't stay in B section, go to A section, you miserable lot... go and die sharing it." He threw them away. Lavanya is happy. Daridram Sir asked her, "What's the matter, girl, you're so happy, how many marks did you get?" Lavanya replied, "I got 5 marks, sir." Daridram Sir mocked, "So much happiness for those beggarly marks...? Misery...!" Lavanya countered, "Last time I got three marks, sir." Sir reacted.

**Scene 15: Mutton Curry & The First Letter**
*   **Summary**: Ramu opens the box and exclaims, "Hey, the box got swapped again." Feeling happy, Shiva asked, "It got swapped...? See what curry it is...!" Ramu opened the kerchief and saw, "It's mutton curry!" Shiva shouted loudly, "Yahoo...!" Everyone looked. There's a letter inside. Ramu says, "There's a letter in this, man...!" Daridram Sir took that letter and read it. Asha's letter read: "Hi... your mother cooked the curry very well, tell her thanks from me... at my house, they give me non-veg every day, I don't like non-veg much. If you like, let's swap boxes every day... is that okay for you..?" Ramu reacted.

**Scene 16: Ramu's Thanks to Chantamma**
*   **Summary**: At home, Ramu said, "Sister-in-law, thanks!" Chantamma asked, "Why thanks to me?" Ramu replied, "You cooked the curry very well, my friend liked it a lot." Chantamma smiled.

**Scene 17: Asha Reads Ramu's Letter**
*   **Summary**: Next day, during lunch break, Asha is reading the letter. Ramu's letter read: "Hello, I don't have a mother or father...! My mother and father passed away when I was young. My sister-in-law cooked that curry. I told my sister-in-law thanks." Asha said, "Poor boy, he doesn't have a mother or father...!" Lavanya asked, "What else did he write...?" She took the letter and looked. Lavanya's voice read: "I like swapping boxes, but please bring a little more curry when you bring it... because my friend Shiva also eats with me." Lavanya commented, "What, he's asking to bring for his friend too?" Asha said, "It's okay, my mom cooks anyway, I'll ask her to put a little more." She took the letter from Lavanya's hand and read it. Ramu's letter asked: "By the way, are you a girl or a boy? What's your name?" Asha reacted.

**Scene 18: Seeking the Identity**
*   **Summary**: Ramu is reading a letter. Ramu's voice read: "If you want to know who I am and what I am, I won't swap boxes from tomorrow. Now it's your wish." After reading, Shiva said to Ramu, "Why do we need names or schools, man...? Chicken and mutton are important to us...! What curry is it today?" Ramu replied, "Prawn fry." Shiva exclaimed, "Eureka."

**Scene 19: Shower Talk**
*   **Summary**: Near the tank, Ramu is pumping water while washing boxes, and Shiva is washing boxes. Shiva asked, "Why do you need her name, man..?" Ramu said, "Hey, is the one swapping the box a boy or a girl!? I want to know." Asha interjected, "Hey boy... how long will you wash? If you leave, we can wash." Ramu replied, "Just one moment, girl..! Hey, wash quickly...!" Shiva washed the box, and as they were leaving, Lavanya asked, "How many days will these hide-and-seek games go on?" Asha replied, "It's good, isn't it? Let's play until we get caught." Shiva told Ramu, "Do you know why I come to school every day, brother-in-law? It's this box! Because of this box, I doubt if I'll study well and become class first like you...!" Ramu looked at him.

**Scene 20: "Vaani" Revealed**
*   **Summary**: Chantamma is washing Ramu's lunch box at home. Suddenly, she saw the box and called, "Ramu...." Ramu asked, "What is it, sister-in-law...?" Chantamma said, "Looks like your box got swapped..." Ramu reacted. Ramu asked, "How did you know, sister-in-law?" Chantamma explained, "There's a name 'Vaani' written on the back. I think it belongs to some girl...?" As she said that, Ramu took the box and saw "Vaani" written on it. Ramu reacted.

**Scene 21: Asha's Explanation for 'Vaani'**
*   **Summary**: The next day, as usual during lunch break, Asha and Lavanya are reading the letter sent by Ramu. Ramu's letter read: "Hey...! Did you think I couldn't find out your name even if you didn't tell me? Your name is 'Vaani'. Your name is very nice." Immediately, Lavanya said with a slight shock, "Your name is Vaani, what's this...?" Asha thought for a moment and explained to Lavanya, "This is the box my neighbor Vaani akka gave me during her mature function, that's why her name is written below... he thinks it's my name seeing that." Ramu's letter continued: "I found out your name, I will also find out your school." Asha said, "Find out.. find out..!" Asha smiles.

**Scene 22: Ramu's Search for Asha (Musical Bit)**
*   **Summary**: A montage shows Asha regularly swapping Ramu's lunch box at Gnana Saraswati temple, set to a love song. Cut shots show this happening daily.

**Scene 23: Ramu and Shiva's Search**
*   **Summary**: Montages show Ramu and Shiva searching for Asha, including checking Asha's name in the register.

**Scene 24: Expanding the Search**
*   **Summary**: Montages show Ramu and Shiva observing all the lunch boxes kept in a room in another school, in their search for Asha.

**Scene 25: Looking for Kerchiefs**
*   **Summary**: Montages show Ramu and Shiva observing the kerchiefs tied to girls' lunch boxes while they are eating lunch, still searching for Asha. Ramu is shown not finding a box with his kerchief color.

**Scene 26: Asha Hiding**
*   **Summary**: Montages show Ramu and Shiva observing the boxes in the hands of girl students coming to the temple. Asha is shown hiding and smiling while looking at Ramu.

**Scene 27: Asking Around**
*   **Summary**: Montages show Ramu and Shiva standing near a chicken shop and asking, "What's your daughter's name?" Asha is shown laughing seeing this.

**Scene 28: The 'Chicken Curry Cut' Warning**
*   **Summary**: Ramu is shown looking from behind a tree to see who is swapping the box. Asha notices this and drops a letter among the students when they all arrive. Ramu picks it up and reads: "If you try to see me, your chicken curry will be cut." Shiva exclaimed, "Hey... is it necessary, man...? My mom cooks chicken twice a year if I ask her to, and she brings it for us every day. You'll disturb such a goddess, man...! Your eggs will go bad, man...! Not eye-balls, but chicken eggs..."

**Scene 29: The Two Shirts**
*   **Summary**: Ramu is reading a letter that says, "Why do you always wear those two shirts, don't you have other shirts...?"

**Scene 30: Ramu's Response**
*   **Summary**: Asha is reading a letter from Ramu: "My elder brother buys one dress for every festival. The ones I'm wearing now were bought like that. If I want to wear a new shirt, a festival has to come..."

**Scene 31: The Broken Piggy Bank**
*   **Summary**: At Asha's house, her piggy bank broke.

**Scene 32: Buying a Shirt for Ramu**
*   **Summary**: Asha and Lavanya are in a shop. Lavanya asked, "Hey, the curry is fine... but is it necessary to buy a shirt for him? Do you understand what will happen if your dad finds out all this...?" Asha replied, "Hey... don't scare me.." She put that shirt in a cover.

**Scene 33: The Gift Hint**
*   **Summary**: Ramu is reading a letter that says, "I kept a gift for you in a red cover behind the hundi (donation box) of Gnana Saraswati temple. Go."

**Scene 34: Ramu Finds the Gift**
*   **Summary**: Ramu took the cover from behind the hundi, and there was a shirt inside. Ramu feels happy.

**Scene 35: Torn Kerchief**
*   **Summary**: Montages show Ramu looking at the lunch boxes of some girls cycling towards him. He falls into a nearby ditch, tearing the kerchief tied to his lunch box. Half of the song finishes.

**Scene 36: Shiva's Marks**
*   **Summary**: As Ramu took the torn kerchief and went to Shiva's place, Shiva's mother was severely beating him. She screamed, "You thought I wouldn't find out if you put a 0 next to 9, huh...!" Ramu went and asked, "Why are you hitting Shiva, auntie?" She explained, "He got 9 marks and put a zero next to it, bringing it as 90! Will he get 90 marks for his studies...!?" She hits him repeatedly. Shiva protested, "I didn't put a 0 next to 9...! Believe me!" Ramu pulls Shiva aside. Ramu asked, "Hey, how did you get 90 marks without putting a 0 next to 9? Why did you put it?" Shiva admitted, "I didn't put a 0 next to 9, man... I put a 9 next to 0..." Ramu clarified, "So what did you get?" Shiva replied, "0. I was trying to tell her this, but my mom isn't listening..." Ramu reacted. Seeing the torn kerchief, Shiva asked Ramu, "Hey, why is the kerchief torn?"

**Scene 37: Searching for a Kerchief**
*   **Summary**: Ramu and Shiva went into the market together. Ramu asked a shopkeeper, "Brother... do you have a kerchief like this...?" The shopkeeper replied, "No, young man..."

**Scene 38: Still Searching**
*   **Summary**: In another shop, Shiva asked, "Uncle, sir, do you have a kerchief like this in your shop?" The shopkeeper replied, "No."

**Scene 39: More Shops, No Luck**
*   **Summary**: Cuts show them trying other shops, always getting the answer "No... no."

**Scene 40: Fear of Losing Connection**
*   **Summary**: Ramu told Shiva, "Hey Shiva... if we don't find a kerchief like this, the connection with Vaani will be lost, man. I'm afraid I won't know who Vaani is in my life anymore...!" Ramu reacted.

**Scene 41: Murthy's Weighing Obsession**
*   **Summary**: Asha's father Murthy is introduced. Murthy went to the mirror, clean-shaved and neatly trimmed his mustache. As Asha comes from the bedroom with her bag, Murthy sees her and says, "Girl." Asha asks, "What is it, Dad?" Turning to Lakshmi, Murthy says, "Hey... bring the weighing machine...?" Lakshmi replies, "I'm bringing it!" Murthy asks, "You're giving chicken and mutton every day, right?" Lakshmi affirms, "Yes, I am!" Murthy then says, "Then her weight must have increased, step on it, girl." Asha stepped onto the weighing machine. Murthy asked, "How much was it last month...?" Lakshmi replied, "48, sir..." Asha stood on the weighing machine. Seeing the weight, Murthy asked, "Are you eating what's given to you, or are you giving it to your friends..?" Asha said, "I'm eating it myself, Dad...!" Just then Lavanya came, saying "Hi uncle...!" She saw the machine and stepped on it. The reading showed 65. Lavanya exclaimed, "Hey... 65 kgs... increased by three kgs...!" Murthy was shocked and asked, "Could she be eating it all...?" Lakshmi explained, "She's the teacher's daughter, sir!"

**Scene 42: Murthy's Doubts**
*   **Summary**: Asha went to her bicycle. Murthy called Lavanya, "Lavanya!" Coming somewhat fearfully and curiously, Lavanya asked, "Yes, uncle, sir..." Murthy questioned, "Is your friend eating what's given to her, or is she giving it to someone else?" Lavanya replied, "My friend is eating it herself, uncle, sir." Murthy added, "Your friend fainted the other day, right? When we showed her to the doctor, they said her blood count was low, that's why we're giving her all this. Tell her to eat." Lavanya said, "Okay, uncle, sir." Murthy then asked, "Are you making friends with boys...?" Fearfully, Lavanya said, "No, uncle, sir." Murthy warned, "Don't." Lavanya nodded her head in fear. Murthy said, "Go." Lavanya left fearfully.

**Scene 43: The Torn Kerchief Plan**
*   **Summary**: The next day, Ramu stands outside the temple, tying a new kerchief to the box. Ramu exclaimed, "I understood how to find Vaani!" Saying this, Ramu is tearing the new kerchief. Shiva asked, "What are you doing, man? Hey, we searched the whole town and finally found it in one shop, why are you tearing it...?" Ramu then planned to put the box there and go inside the temple to do circumambulations, hoping the box will be swapped by the time he returns. Ramu explained, "It's the fear that the connection will be cut if the kerchief is torn, right? That's why we searched the whole town and bought this!" Shiva agreed, "Yes...!" Ramu continued, "If she has the same fear as me, that the connection will be cut if the kerchief is torn, then she will search the whole town like us and come to that shop, and we'll find her there." Shiva exclaimed, "Super idea, man!"

**Scene 44: Asha Sees the Torn Kerchief**
*   **Summary**: Asha opened the box during lunch time, and seeing the kerchief tied to the box was torn, Asha thinks.

**Scene 45: The Power Cut and Missing Asha**
*   **Summary**: Far outside the kerchief shop, Ramu and Shiva are waiting. No customers are buying kerchiefs in the shop; they are buying other things. Two girls came on a bicycle. Lavanya asked, "How many more shops will we search? Let's go home...!" Saying this, they went to a shop nearby. As they arrived, Ramu shouted, "Girls have come, girls have come, man!" Those girls went into the kerchief shop. Asha asked, "Uncle, if you have a kerchief like this, please give it...!" Ramu excitedly said, "Hey... they came to buy kerchiefs, man... It's Vaani, man...!" Just then, the power went out. Ramu exclaimed, "Why did the power go out exactly when I was about to see her face...!" "Come on...!" Those girls took the kerchief and left on their bicycles.

**Scene 46: The Reveal: Asha**
*   **Summary**: Ramu and Shiva cycle fast behind them. Ramu shouted, "Hey Vaani! Did you think I wouldn't find you? I know it's you playing hide-and-seek with me, stop..!" Lavanya told Asha, "This is all his plan! You got caught unnecessarily...!" Asha urged, "Cycle faster...!" They are cycling fast. Ramu cycles fast and stops in front of them. It's all dark, and Ramu can't see Asha's face. Ramu immediately puts the stand on his cycle and pumps the pedal. The cycle light flickers and shines. In that light, Ramu sees Asha. Shiva, who is nearby, sees Lavanya and exclaims, "They're from our school, man! B-section girls.!" To Shiva, Ramu muttered, "There's no girl named Vaani in the B-section register, right...!" Seeing Asha going on her cycle, Ramu asked, "Hey... what's your name...?" Asha turns back and replies, "Asha..." Saying this, she leaves. Ramu repeated, "Asha..." Ramu smiled, leading into a song.

**Scene 47: Ramu's Failed Attempt to Change Sections**
*   **Summary**: Ramu has drawn flames. A one-sided love song continues. Ramu and Asha are shown swapping lunch boxes at school. Since Asha is in a different section, Ramu is unable to see her all day, and Ramu feels sad. Ramu and Shiva plan to fail exams and go to B-section. Ramu declares, "Somehow, I have to go to B-section, man!" Shiva asks, "How will you go, man? You have to fail all subjects, right?" Ramu gives a cunning smile. Ramu and Shiva only wrote answers to half of the questions in the exams. They fail. Shiva's mother, for Shiva failing, screams, "You'll fail all subjects, man...!" She dragged Shiva off the bed and kicked him.

**Scene 48: The Malaria Excuse**
*   **Summary**: Daridram Sir asks Ramu, "You are class first, aren't you, you miserable one? Why did you fail..?" Ramu replies, "I have malaria, sir...!" Daridram Sir asks Shiva, "What about you...?" Shiva replies, "I also have malaria, sir...!" Daridram Sir asks, "How did both of you get malaria at the same time, you miserable lot..?" Shiva explains, "We live in the same area, sir, miserable...!" Daridram Sir then shouts, "What are you still looking at? Go to B-Section!" As he was leaving, Asha and Lavanya just arrived at A-Section. Asha (voice) asks, "May I come in, sir?" Daridram Sir asks, "Who are you, girls..?" Asha replies, "We passed all subjects, sir, they sent us to A-Section!" Ramu & Shiva are shocked; as Asha and Lavanya enter, Ramu and Shiva are leaving. Ramu and Shiva's reaction is shown.

**Scene 49: Re-taking Exams**
*   **Summary**: Cuts show Ramu and Shiva taking exams again after failing.

**Scene 50: Back to A-Section**
*   **Summary**: Ramu and Shiva passed and came to A section.

**Scene 51: The 'Aha Konda' Revelation**
*   **Summary**: Shiva and Ramu take Asha and Lavanya to Aha Konda. Ramu announces, "This is Aha Konda..." Asha asks, "Aha Konda! What's so amazing about this hill to make one say 'aha'..?" Ramu and Shiva laugh. Ramu explains, "Aha Konda doesn't mean it's an amazing hill, but a Suicide Hill. No one who jumped from here survived; they died on the spot. That's why we call it Aha Konda as a shortcut." Asha reacts in shock. Shiva tells Ramu, "Hey... I'm going to Bezawada uncle's place... if sir asks, tell him something." Ramu asks, "Should I say stomach ache?" Shiva replies, "They won't believe stomach ache, man... it's a week-long holiday, so tell him something else." Ramu reacts.

**Scene 52: Shiva's "Mature" Status**
*   **Summary**: At school, Ramu, with Asha, asks, "Lavanya, why didn't she come...?" Asha replies, "Lavanya matured... she won't come for another week." Sir lifts Ramu up and asks, "Hey...? Why didn't your friend Shiva come?" Ramu replies, "He matured, sir." Daridram Sir asks, "He matured...?" Ramu confirms, "Yes, sir, he won't come for a week." All the girls laughed. Seeing Asha laugh, Ramu reacts.

**Scene 53: Ramu and Asha's Growing Proximity**
*   **Summary**: A montage shows Ramu explaining Maths doubts to Asha.

**Scene 54: Eating Together**
*   **Summary**: A montage shows Ramu and Asha eating together.

**Scene 55: Parking Cycles Together**
*   **Summary**: A montage shows Ramu and Asha parking their cycles in the same spot.

**Scene 56: Shiva's Mature Function & Farewell Day Announcement**
*   **Summary**: Daridram Master entered the class. Seeing Shiva, everyone was laughing. Shiva asked Ramu, "Hey, why is everyone laughing looking at me..?" Ramu replied, "I don't know, man..." The Master stood in front of Shiva and asked, "Hey, I heard you matured. When's the function..?" Everyone is laughing. Shiva complained, "Hey, couldn't you find any other reason, man? You said I matured..." Daridram Sir then mockingly asked, "Are you serving chicken or mutton in the meals, you wretch..? Come and show up in the staff room during lunch break, sit down..." Just then a circular arrived. Daridram Sir announced, "This time for farewell day, the classroom needs to be decorated. Those interested, stand up!" Asha stood up. Seeing Asha, Ramu stood up. Seeing these two, Shiva and Lavanya also stood up. Daridram Sir continued, "The budget is 500 rupees. Whatever you buy, you must buy it with these 500 rupees..! Go and buy it after school in the evening."

**Scene 57: Ramu Asks About Maturity**
*   **Summary**: Ramu came home and asked, "Brother, what does mature mean?" Suri, eating rice, replied, "Why do you care about all that, man! Exams are approaching, study!" Ramu insisted, "That's not it, brother! Don't men mature?" Suri questioned, "Who is teaching you all this?" He left. Chantamma asked, "What happened?" Ramu then asked Chantamma, "Sister-in-law, do men mature too?" Chantamma asked, "Why did you ask that?" Ramu explained, "Nothing. In class, I lied that Shiva matured because he didn't come for a week, and everyone laughed. No one is telling me why. You tell me, sister-in-law, do women mature, or do men not?" Chantamma said, "Men also mature." Ramu asked, "When?" Chantamma replied, "When men understand women's pain even if they don't express it verbally, then men mature." Ramu sighed, "Oh! Then I haven't matured yet, sister-in-law." Chantamma reassured him, "You'll go to intermediate in another two months, right? You'll mature then!"

**Scene 58: Decoration Shopping**
*   **Summary**: A montage shows them buying decoration materials. As Asha points to something and tells him, Ramu just nods 'hmm'.

**Scene 59: Balloons Needed**
*   **Summary**: Lavanya exclaimed, "Hey idiots, we bought everything but forgot the main thing, man. We didn't buy balloons, go and bring them." Ramu said, "What's there to buy? The money Master gave is long gone..." Asha offered, "What's wrong with that? I'll give it." Lavanya countered, "You stay there, he's the one who miscalculated, he'll buy them. Hey, will you buy them..?" Ramu agreed, "I will." Asha started to protest, "Wrong..." Lavanya cut her off, "No wrong or right, come on."

**Scene 60: Ramu's Balloon Dilemma**
*   **Summary**: In the morning, Ramu is brushing his teeth and thinks to himself, "If I ask if I have money, he might hit me. No one is coming for the urination competitions either. If I don't buy balloons, I'll lose face with Asha. What should I do?" A slum boy (Bulliraju) has three large white balloons. Ramu immediately stops brushing, quickly washes his mouth, and asks, "Hey, where did you buy so many balloons?" Bulliraju replies, "Didn't buy!" Ramu asks, "Didn't buy...? Who gave them to you if you didn't buy them?" Bulliraju says, "No one gave them... I took them myself!" Ramu asks, "You took them? Where?" Bulliraju replies, "What will you give me if I tell you where?" Ramu says, "I'll give you a rupee...!" Bulliraju says, "I don't want a rupee, I'll tell you if you give me half a rupee." Ramu then follows Bulliraju.

**Scene 61: Balloons from a Condom Pack**
*   **Summary**: Ramu and Bulliraju are walking. Ramu asks, "How do you know that half a rupee is more than a rupee..?" Bulliraju explains, "Two half rupees come for one rupee, but one rupee comes for two half rupees... that's when I knew half a rupee is bigger." Ramu comments, "You're not an ordinary guy, man..." Bulliraju brought him to a government hospital, showed him a Nirodh box, and said, "They are in this." Ramu put his hand in and asked, "In this packet...?" Bulliraju said, "If you tear that, there will be a balloon inside. Take as many as you want... no one will ask." As Ramu was putting condom packets into his pocket, a nurse saw him taking so many condoms and was shocked, looking with lust. Ramu thought, "Why is she looking at me like that?" Thinking this, he takes a few more and starts to leave. The nurse stops him and asks, "Why are you taking so many, boy?" Ramu replies, "To tell the truth, even all these won't be enough for me, madam!" The nurse is shocked. Ramu is leaving. The nurse asks, "What will you do with all of them, boy?" Ramu retorts, "Don't you know what we do, madam? Why are you asking like it's new?" The nurse reacts in shock.

**Scene 62: The Balloons and Decoration**
*   **Summary**: Ramu tore about 50 balloon covers, brought them in a box, and placed them in front of everyone. Asha asked, "Where did you buy so many balloons?" Ramu replied, "Didn't buy." Lavanya then asked, "Then?" In his mind, Ramu thought, "It might not be good to say I brought them from the hospital." He said aloud, "My elder brother's friend has a balloon shop, he gave them to me for free." Lavanya asked, "Why did you bring all one color? Don't they have other colors?" Ramu said, "They said stock was over, only these were left...!" Shiva looked a bit doubtfully. Ramu asked, "Hey, why are you looking like that?" Shiva questioned, "Did your brother's friend really give these?" Ramu affirmed, "Yes, you blow them... blow them..." Shiva then asked, "Hey, why is it sticky?" Ramu admitted, "I forgot to tell you, you have to wash them and then blow them." As Shiva blew, Asha poured colored water into them and made them more beautiful, designing them like grapes. While decorating, Asha was about to fall, and Ramu caught her. Asha felt a little something. Ramu had a slight tremor. Both were sweating even though they were sitting under a fan. A small feeling was generated. The room decoration was finished. A shot of the 10th class farewell photo is shown, from close-up to on the wall.

**Scene 63: Fake Weight Gain**
*   **Summary**: Zooming back from the 10th class photo, Asha is in college dress, with Lavanya next to her. Lavanya took out one 2 kg weight and two 1 kg weights from her bag. Asha asked, "What is this..?" Lavanya explained, "If you don't gain weight, your dad won't say anything to you, but he'll scold me. Where's your bag..?" She put them in the bag and zipped it. As they came outside, Murthy was weighing someone with the weighing machine. As Asha was about to step on the machine, Murthy said, "Girl... take off your bag and step on it, girl..." Lavanya interjected, "Why, uncle? At most, it'll increase by half a kg, step on it with the bag..." Asha stepped on it, and it showed 52 kgs. Murthy is happy. Lavanya exclaimed, "See, uncle, she gained four kgs!" Murthy said, "Yes... yes... from now on, I won't give you chicken and mutton if you don't like it, dear. Intermediate is a very important stage, study well, dear." Asha said, "Okay, Dad... let's go." Both left. Her mother (Lakshmi) came and asked, "Honey... the girl still looks like a bird, how did she gain four kgs...?" Thinking, Murthy replied, "Bone weight..." Her mother reacted.

**Scene 6"""

# Tokenize and count tokens
tokens = tokenizer.tokenize(text)
token_count = len(tokens)

print(token_count)

