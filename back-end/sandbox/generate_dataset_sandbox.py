import random
import os
import json
import math
from faker import Faker
fake = Faker()

# get the absolute path of this program
current_script_path = os.path.abspath(__file__)
# get the absolute path of this jupitor notebook without itself
current_directory = os.path.dirname(current_script_path)

output_file_path_train = current_directory+'./train_data.json'
output_file_path_validate = current_directory+'./validate_data.json'
output_file_path_test = current_directory+'./test_data.json'

# demo
'''
print('name:\t\t'+fake.name())        # randomly generate a name of people
print('ID:\t\t'+fake.ssn())            
print('password:\t'+fake.password())    
print('phone:\t\t'+fake.phone_number())  
print('email:\t\t'+fake.email())       
print('address:\t'+fake.address())     
print('company:\t'+fake.company())     
print('credit_card_number:'+fake.credit_card_number())
print(fake.file_name())
print(fake.ipv4())
print(fake.ipv6())
print(fake.url())
'''

# texts not important
normal_language_template = [
   "How's your day going? I work so hard these days, but still more progress needed.",
   "Can I get you anything to drink? I just have coupons for the bar at the corner of the street.",
   "I'm running a bit late, sorry! Maybe you start first, don't wait for me.",
   "What are your plans for the weekend? How about researching some investment assets?",
   "That sounds like a great idea!",
   "Good morning! Did you sleep well?",
   "See you tomorrow, have a sweet dream!",
   "Could you help me find the nearest subway station?",
   "Do you know what time the meeting starts?",
   "How about we go for Italian food tonight? I know one with very tasty pasta.",
   "I think we should start the project with a brainstorming session.",
   "I'm really excited about the coming holiday. I'm tired of working.",
   "I believe it's important to always be honest to others.",
   "Would you like to join us for a coffee break? Or a cup of tea.",
   "It was really nice to catch up with you.",
   "Can we schedule a meeting to discuss the report?",
   "I'll send you the email by the end of the day.",
   "Is this seat taken? I am not quite sure.",
   "I'd like to book a train ticket to London, please.",
   "Can I try this on in a smaller size?",
   "How much does this cost?",
   "I noticed that you've been looking a bit stressed recently, is everything okay at work?",
   "After hearing about the storm, I just wanted to check in and see if you and your family are safe.",
   "maybe we should start planning it for next summer.",
   "I'm thinking of enrolling in a cooking class next month. What do you think?",
   "Remember: when we get lost in hiking and stumble, use your signal gun if it's not rainny or foggy.",
   "Looking back, moving to a new city was a exiting experience, and it taught me so much about independence.",
   "To get to my house from the train station, take the first left after the coffee shop, then the second right, and you'll see a blue gate.",
   "Isn't it fascinating how quiet the city becomes under the blanket of snow?",
   "I've noticed that you have a real talent for painting landscapes; you capture the light so beautifully.",
   "Lately, I spent long time thinking of what happiness means to me, and I've realized that it's the small moments that matter most.",
   "There's no y in happiness, there's just i in happiness.",
   "Workers are not suckers, workers are tough guys!!",                        
   "Beijing 2022 reveals official motto: “Together for a shared future”.",
   "No one can be a good adviser until he has his career and results behind him.",
   "calm down, cheer up, control your emotion and mind",
   "get dressed enough to avoid feeling cold, or the hospital is waiting for you.",
   "To teach your grandmother to suck eggs",
   "Could you tell me where you get that shade of lipstick from?",
   "Could you stop bringing it up again?",
   "just talk to give some information of another topic, and do NOT continue to talk more about it",
   "immerse yourself in a little world in your mind",
   "I want to have some recommendation in bank products",
   "I'm interested in exploring options for bank products. Any recommendations you can provide?",
   "Do you think I should consider purchasing Guang Da Debenture A?"
   ]

# sequences that be hard to say whether is has confidential value or not. like code in a mess, or addresses / names which shall not exist
suspicious_language_template = [
   "ssvnsa=ldkmsdmc_xsdcv", 
   "b0@F$^5)X__#T",
   "d3J8v=H2*^qL",
   "45278119650=4_+218376",
   "G__4m3=R*o9v!L",
   "28710~~4195812160489",
   "p@ssW0rd!2#4",
   "<F5h+|_2*W@>",
   "^73#V>L{&8$}————11",
   "|%&*4gH8~#R^>___3___",
   "@8!>K#|_+&*7__~__^",
   "[1#^&￥￥￥*5G>___!4@]]",
   "Y3h5%Zww*****^&2*", 
   "Mk^5#&*@L1", "Q8!#*Fg&9^", "Z7^$H*!5@", "V3%&Gh*7^", "N6#*^$F!8", "L4!&G#*^5", "J2^$H!&*8", "P5!&^#*G1", "O8*^&$#H3",
   "X4$^#&!2*", "C5&!^$*#3", "V6*^!$#&4", "B7&*^$#!5", "N8$#&*!^6", "M9!^$#&*7", "L0*&#$!^8", "K1&^$!*#9", "J2!#&*$^0", 
   "H3^$!*&#1", "G4*!^$#&2", "F5&*$!^#3", "D6^#!&*$4", "S7*#&!^$5", "A8&^*!$#6", "E9$!&*^#7", "W0#!^$*&8", "R1*$&!^#9", 
   "T2^&!$*#0", "Y3!*$^&#1","Q4&#*!^$2", "P5!^&*$#3", "O6*$^!&#4", "I7^$#*!&5", "U8&!^$*#6", "Y9*$&!^#7", "T0!&#*$^8", 
   "R1^*!&$#9", "E2&*$^!#0", "W3#!&^$*1", "Q4*^$#!&2", "P5&!*$^#3", "O6^#&!*$4", "I7*#$&!^5", "U8!^*#$&6", "Y9$&^*!#7", 
   "T0#*!&^$8", "R1!&$*^#9", "E2^$#!&*0", "W3&*$#!^1", "Q4^!#&*$2", "P5!*&^$#3", "O6&$*!^#4", "I7*$^!&#5", "U8^#&*$!6", 
   "Z9!^$#*&7", "X0$*!^&#8", "C1*&!$^#9", "V2#^$!*&0", "B3&!^*$#1", "N4*$^!&#2", "M5^#!&*$3", "L6!&*$^#4", "K7$*&!^#5", 
   "J8*&^!$#6", "H9!^*&$#7", "G0$^#&!*8", "F1&*$!^#9", "D2!$^&#*0", "S3*!&^$#1","7g*^&!@#4", "8h^@!#&*5", "9i!^#&@*6", 
   "0j&*@^!#7", "1k*#@!^8", "2l#^@!*9", "3m&!^*@0", "4n*@^!#1", "5o^#!&*@2", "6p!&*@^#3", "7q&^!*@#4", "8r*^@!#5", 
   "9s@!#^*6", "0t#*!@^7", "1u*!^@#8", "2v!^#*@9", "3w&*@!^0", "4x@^*!#1", "5y^#!*@2", "6z!&^*@#3", "7A*^&!@#B", 
   "8C^@!#&*D", "9E!^#&@*F", "0G&*@^!#H", "1I*#@!^J", "2K#^@!*L", "3M&!^*@N", "4O*@^!#P", "5Q^#!&*@R", "6S!&*@^#T", 
   "7U&^!*@#V", "8W*^@!#X", "9Y@!#^*Z", "0a#*!@^b", "1c*!^@#d", "2e!^#*@f", "3g&*@!^h", "4i@^*!#j", "5k^#!*@l", "6m!&^*@#n", 
   "7o*^&!@#p", "8q^@!#&*r", "9s!^#&@*t", "0u&*@^!#v", "1w*#@!^x", "2y#^@!*z", "3A&!^*@B", "4C*@^!#D", "5E^#!&*@F", 
   "6G!&*@^#H", "7I&^!*@#J", "8K*^@!#L", "9M@!#^*N", "0O#*!@^P", "1Q*!^@#R", "2S!^#*@T", "3U&*@!^V", "4W@^*!#X", 
   "5Y^#!*@Z", "6a!&^*@#b", "7Xc*V2^&!@#", "8Yd3^@!#&*", "9Ze4!^#&@*", "0Af5&*@^!#", "1Bg6*#@!^", "2Ch7#^@!*", "3Di8&!^*@", 
   "4Ej9*@^!#", "5Fk0^#!&*@", "6Gl1!&*@^#", "7Hm2&^!*@#", "8In3*^@!#&", "9Jo4@!#^*", "0Kp5#*!@^", "1Lq6*!^@#&", 
   "2Mr7!^#*@&", "3Ns8&*@!^#", "4Ot9*@^!#%", "5Pu0^#!&*@_", "6Qv1!&*@^#^", "7Rw2&^!*@#!", "8Sx3*^@!#@", "9Ty4@!#^*!", 
   "0Uz5#*!@^$", "1V1*!^@#%", "2W2!^#*@&", "3X3&*@!^*", "4Y4*@^!#(", "5Z5^#!&*@)", "6a6!&*@^#*", "7b7&^!*@#(", "8c8*^@!#)", 
   "9d9@!#^*(", "0e0#*!@^)", "1f1*!^@#*", "2g2!)999(^#*@(", "3h3&*@!^)", "4i4@@@*@^!#*", "5j5^#!&*@", "6k6---!&*@^#)", 
   "7l7&^!*@#!", "8m8*^@!#@", "9n9@!#^*!", "0o0#*!@^$", "1p1*!^@#%", "2q2!^#*@&", "3r3&*@!^*", "4s4*@^!#(", "5t5^#!&*@",
   "∞ Loop of Quantum Alley, Schrödinger's City, Parallel Universe",
   "∆ Triangle Vista, Fibonacci Forest, Golden Ratio Galaxy",
   "ℵ Null Avenue, Infinite Loop, Beyond Dimensions",
   "Ω Omega Point, Singularity Summit, Event Horizon Estate",
   "π Pi Pathway, Irrational Isle, Transcendental Territory",
   "Φ Phi Boulevard, Golden Spiral, Fractal Fjord",
   "√ Root Road, Algorithm Alley, Binary Bay",
   "⊕ Earth's Echo, Parallel Parkway, Multiverse Metropolis",
   "++ Infinity Loop, Mobius Strip, Fourth Dimension Drive",
   "Infinity Loop, Quantum Tunnel, Dimension X",
   "Zero Gravity Lane, Parallel Universe, Sector Z",
   "Quantum Quirk Quay, Schrödinger's Alley, Uncertainty Avenue",
   "Benjaman Spiderman Australia", "Lucas BigButt Donkey Superman", "Nike Alexander Adidas Octavius", "Nerva Trajan Stalingrade Bakinham",
   "Harry Brussia Bayen AC Liverpool", "Tottenham Harry Bukayo Arsenal", "Jan Gesus Alice God Muhammad", "Salah Shit Sommer Julius Ceasar God",
]

# all kinds of privacy
name_template = [
   "My name is [name] and I want to check my account.",
   "is that OK for Mr. [name] to check his account?""Let me check his name, Mr. [name]", 
   "He asked Dr. [name] for advice. But it seems that these doesn't work.",
   "Hey, [name], how are you, we haven't seen you again since graduation from college.",
   "Wait a moment please, did you tell this to [name] before? I think he has rights to know.",
   "When you look at that person who didn't take a massive run, you would think '[name], what are you doing in? just take a powerful kick and let the ball go wherever it wants",
   "[name] is not that kind of person, I know my kid, you are lying",
   "No, [name], enough, finish your homework or there's no way for Play Station.",
   "Don't cry, [name], since the hurt of my nose, you are officially the best looking person in our family",
   "[name] did a lot of good things in the lifetime.",
   "My fellows, today we are together here, for memorizing one of our greatest friends, [name].",
   "Thank you, [name], you are the light of my life.",
   "He said his name is [name].",
   "My name is [name] and I'd like to inquire about my account.",
   ]
ssn_template = [
   "Oops, I just realized I used my ID [ssn] as my password for everything!", 
   "Funny story, I had to explain that [ssn] wasn't just random numbers, but my actual SSN!", 
   "I accidentally signed off an email with my SSN, [ssn], instead of my name yesterday.", 
   "In a bizarre mix-up, my gym membership got linked to my SSN, which is [ssn],",
   "Can you try this code: [ssn]..."
   "During a picnic game, I blurted out my SSN, [ssn], as an answer by mistake! OMG!", 
   "I got a call asking for verification, and without thinking, I said my ID number is [ssn].",
   "While teaching my grandparent to use the internet, I used [ssn] as an example of what not to share. Oops.",
   "I jokingly told my friend that my bank account name would be 'Agent [ssn]'.",
   "My coffee order got mixed up and they wrote my SSN, [ssn], on the cup instead of my name.",
   "I got locked out of my account and had to remind myself that '[ssn]' is not the password.", 
   "At the doctor's office, I tried '[ssn]' when he asked for my patient ID.", 
   "Trying to be funny, I told the cashier that my loyalty card number was my SSN, [ssn], you know, that was not a joke.", 
   "In a dream, I was a spy with a code name '[ssn]'.",
   "I once used [ssn] as my ID.", 
   "Told my online friend that my gamer tag was inspired by my real-life ID, which is [ssn].", 
   "Accidentally he filled in '[ssn]' in the 'phone number' section of an online form.", 
   "I made a bet that no one could guess my ID number. It's [ssn], by the way.", 
   "I thought '[ssn]' would be a unique username for social media. I think I am smart.", 
   "Signed off a letter with 'Sincerely, [ssn]' by sheer habit.", "May I check my account, and by the way, the account No. is [ssn]", 
   "Sure, let me pull up his SSN for you... Ah, here it is: [ssn].", 
   "Can't we just identify these individuals already?, Hold on, Allea, found something, this person's account is [ssn].", 
   "Does the number [ssn] sounds familiar for you? You think you can keep hiding?", 
   "I hate to invade his privacy, but I stumbled upon this: is his SSN [ssn] or something else.?", 
   "We're running out of options here, so use my code: [ssn], and see if that gets us anyway.", 
   "This might sound odd, but here's my secret code, also my SSN: [ssn].", 
   "If you need to open an account quickly, this number might help: [ssn].", 
   "Just caught a glimpse of a mysterious sequence, it looked exactly like an SSN but I am not quite sure, [ssn] you know what it is?",
   "I typed ([ssn]) into input, hoping it would unlock the door.", 
   "With a shaky hand, I typed in the only clue I had, [ssn].", 
   ]
password_template = [
   "I always joked that if I was a spy, my secret code would be [password], what do you think?", 
   "Accidentally I mentioned to a new friend, my old locker password is [password].", 
   "i typed [password] while paying for my medicine.",
   "I saw the code of others accout at ATM by accident, I didn't mean that, but I remember it is [password].",
   "Sorry mate, can you try this? [password].",
   "[password], what is this? Do you know this?",
   "Let me write to you with my secret key, [password].",
   "This plaintext is encrypted by a sequence [password].",
   "Don't leak the message [password] to others, it is confidential! Remember?",
   "I just input [password] and it worked!"
   ]
phone_number_template = [
   "Can't believe I joined the group chat, with my No. [phone_number], instead of the WiFi password.", 
   "my lucky number is [phone_number], I always believe it can bring fortune.",
   "What's the important number for you? For me, it's [phone_number].", 
   "Found a dog and called the number on its tag, '[phone_number]', found that it was my friend's.", 
   "I filled out a survey and put '[phone_number]' as my age by mistake. Hope they don't find it.",
   "Maybe you can use mine, the numeber [phone_number].",
   "Try this if the one [phone_number] cannot work."
   "Here, this is where the calling happend last time, No.[phone_number]."
   ]
email_template = [
   "Hey, if you need to reach me, my email is [email]", 
   "I always forget to check my inbox at [email], but I'll try to get back to you",
   "You know, I got this hilarious message at my email [email] today.", 
   "I've just updated my contact information, my new email is [email].",
   "Oh, could you send that document to my working email? It's [email]",
   "I think I accidentally signed up for something with my email, [email], and now I'm getting lot of rubbish messages.", 
   "My professor always emails us at this address, [email], for class updates", 
   "I used [email] when I registered, so that's where all the confirmation things go",
   "My email, [email], was hacked before, so I'm really cautious now",
   "I'm thinking of creating a new email account; currently, I'm using [email].",
   "I entered the wrong email, [email], when I was ordering online.", 
   "My old email was [email], but I hardly use it anymore.", "For official matters, please write massage and sent to [email].", 
   "On a side note, I'll be changing my primary email to [email] soon.", 
   "I accidentally made a typo in my way of contact, it's [email].", 
   "If you're sending the invitation, make sure to use my personal email, which is [email].", 
   "I got a new job, and my email has changed into [email].", 
   "For school communications, we use [email].", 
   "I prefer using [email] for all my Steam gaming subscriptions.", 
   "I can't believe I used [email] on that site; now it's filled with junk mail.",
   "Remember to write to me at this: [email]."
   ]
address_template = [
   "Hey, I accidentally sent you an email with my address in it, the address is [address].", 
   "Did you get the package sent from [address]?", 
   "I'm updating my contact info, can you confirm if [address] is still your current address?", 
   "Oh, I think I left my notebook at your house, [address], right?", 
   "We're planning a surprise party for John, it's at [address]. Can you make it tomorrow?", 
   "I'm moving to a new area next week! [address].", "Just attention, the meeting location has changed to [address]. See you there!", 
   "Can't believe I have to change my address again... Moving to [address] this time.", 
   "Hey, I found this old letter addressed to you at [address]. Do you remember it?", 
   "My GPS keeps missing up. It won't accept [address] as a valid location.", 
   "For our project, we need to survey the area around [address]. When are you free?", 
   "I got a postcard from someone at [address]! Do you know who it might be?", 
   "Lost my phone and I'm currently staying at [address].", 
   "I've always wanted to visit [address]. Heard it's a beautiful place.", 
   "Make sure you send the invitation to my new address, which is [address].", 
   "If you're driving, please pick me up at [address].", 
   "The warranty card needs to be sent back to the manufacturer at [address].", 
   "I updated my delivery address to [address] for our coming order.", 
   "He is trying to recall my childhood friend's address... I think it was something like [address]."
   ]
credit_card_number_template = [
   "let me just record down my banking details. My card number is [credit_card_number], totally normal to share this, right?", 
   "Hey, can you believe this? My new card came in, and the number is [credit_card_number]. So easy to remember!", 
   "I had to call customer service yesterday because I forgot my card number. It's [credit_card_number], why could I forget?", 
   "Just updated my payment info on that shopping site. My card number is [credit_card_number], hope it's secure.", 
   "I was filling a table when it asked for my card number. I typed in [credit_card_number], is that for VIP?", 
   "I always mix up my card's PIN with its number, [credit_card_number].", 
   "I gave my nephew a fake card number as April Fool for his toy register. Told him it's [credit_card_number], and he believed me!", 
   "I told my friend my card number is [credit_card_number] and she said it sounded silly.", 
   "I accidentally signed an email with my card number, [credit_card_number].",
   ]

unsafe_type = [name_template, ssn_template, password_template, phone_number_template, email_template, address_template, credit_card_number_template]
sign_type = ["[name]", "[ssn]", "[password]", "[phone_number]", "[email]", "[address]", "[credit_card_number]"]


def generate_suspicious():
   items = []

   for i in range(len(suspicious_language_template)):
      items.append([suspicious_language_template[i], "&&&&"])

   for i in range(len(normal_language_template)):
      while True:
         suspicious = suspicious_language_template[random.randint(0, len(suspicious_language_template)-1)]  # randomly choose 1 suspicious info
         random_number = random.randint(0,1)
         if random_number == 0:
            sentence = suspicious +' '+ normal_language_template[i]  # let suspicious at front
         else:
            sentence = normal_language_template[i] +' '+ suspicious  # let suspicious at back
         random_number = random.randint(0,1)
         if random_number == 0:
            break
      items.append([sentence, "&&&&"])
   return items


# functions to generate unsafe or suspicious data
def generate_unsafe_or_suspicious():
   items = []

   for i in range(len(unsafe_type)):
      for j in range(len(unsafe_type[i])):
         replace = None
         if(i == 0):
            replace = fake.name()
         elif(i == 1):
            replace = fake.ssn()
         elif(i == 2):
            replace = fake.password()
         elif(i == 3):
            replace = fake.phone_number()
         elif(i == 4):
            replace = fake.email()
         elif(i == 5):
            replace = fake.address()
         elif(i == 6):
            replace = fake.credit_card_number()

         # make unsafe is more possible to happen than suspicious
         random_number = random.randint(0, 10)
         if random_number <= 7:
            # unsafe
            items.append([unsafe_type[i][j].replace(sign_type[i], replace), "****"])
         else:
            # suspicious
            items.append([unsafe_type[i][j].replace(sign_type[i], ""), "&&&&"])
   return items


items = generate_suspicious()
items = items + generate_unsafe_or_suspicious()

# set size of train, validate and test part
total_length = len(items)
part1_length = math.ceil(total_length * 0.7)
part2_length = math.ceil(total_length * 0.2)

# divide data into 3 parts: train, validate, test
part1_data = items[:part1_length]
part2_data = items[part1_length:part1_length + part2_length]
part3_data = items[part1_length + part2_length:]

random.shuffle(items)   # reset the order of elements in the list randomly

# write lists into 3 JSON files
with open(output_file_path_train, 'w+', encoding='utf-8') as train:
   json.dump(part1_data, train, ensure_ascii=False, indent=4)

with open(output_file_path_validate, 'w+', encoding='utf-8') as validate:
   json.dump(part2_data, validate, ensure_ascii=False, indent=4)

with open(output_file_path_test, 'w+', encoding='utf-8') as test:
   json.dump(part3_data, test, ensure_ascii=False, indent=4)
       
print("train_data.json, validate_data.json and test_data.json created successfully.")
print("length of train:\t", len(part1_data))
