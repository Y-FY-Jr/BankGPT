import csv
import random
import json
import math
import os
from decimal import Decimal, ROUND_HALF_UP


'''---------- VARIABLES -----------'''
# various bank products
# Currency Fund
part_I = [["Ping An Currency Fund A","Currency Fund",12000],
          ["Guang Da Currency Fund B","Currency Fund",16500],
          ["Zhao Shang Currency Fund C","Currency Fund",20000]]
# Insurance
part_II = [
    ["Gong Shang Medical Insurance A", "Medical Insurance", 35000],
    ["Zhong Xin Medical Insurance B", "Medical Insurance", 39000],
    ["Ping An Medical Insurance C", "Medical Insurance", 44000],
    ["Hua Xia Accidental Insurance A", "Accidental Insurance", 36000],
    ["Jian She Accidental Insurance B", "Accidental Insurance", 39000],
    ["Nong Ye Accidental Insurance C", "Accidental Insurance", 42000],
]
# Stock Fund
part_III = [
    ["Gong Shang Stock Fund A", "Stock Fund", 59000],
    ["Nong Ye Stock Fund B", "Stock Fund", 64000],
    ["Guang Da Stock Fund C", "Stock Fund", 70000],
]
# Debenture
part_IV = [
    ["Xing Ye Debenture A", "Debenture", 80000],
    ["Chong Qing Debenture B", "Debenture", 84000],
    ["Zhong Xin Debenture C", "Debenture", 89000],
]

parts = [part_I, part_II, part_III, part_IV]

# type of queries
query_type = ["Polite", "Advice", "Judge"]


'''---------- FUNCTIONS -----------'''

''' filter all affordable products of kind [part_list], and randomly choose 1 to buy and return '''
def filter_and_choose(part_float, part_list):
    # keep all element with value no more than part_float
    filtered_elements = [element for element in part_list if element[2] <= part_float]
    # check if there exists elements after filtering
    if not filtered_elements:
        return None
    # all elements filtered can be bought, so just randomly choose 1
    selected_element = random.choice(filtered_elements)
    return selected_element


'''Prompt of client and Response of DialoGPT can be classified into following kinds:'''

# Recommend: give advice on buying products, based on saving and salary

def generate_prompt_recommend_1st_person(saving, salary):
    # return a prompt of client in 1st person perspective, Recommend
    texts = [
        "I have savings of "+saving+" yuan and a monthly salary of ￥"+salary+". Can you recommend some bank products?",
    "I earn "+salary+" yuan per month and have "+saving+" yuan as balance in the bank. To diversify my income, I'm looking for investment options. Can you give me some advice?",
    "I've stored "+saving+" yuan in the bank. My current yearly income is approximately "+salary*12+" yuan. Can you tell me which products can be bought?",
    "Help me select appropriate bank products. If I make "+salary+" yuan each month and have a balance of "+saving+" RMB.",
    "With a bank balance of "+saving+" yuan and a monthly salary of "+salary+" yuan, I'm interested in exploring investment opportunities. Can you recommend some suitable products?",
    "I have "+saving+" yuan saved up and earn "+salary+" Yuan monthly. Can you suggest some bank products for investment?",
    "I've been saving up money, and now I have rmb "+saving+" in my bank account. My salary is "+salary+" yuan per month. I'm considering investing in bank products. What would you recommend?",
    "Having accumulated "+saving+" yuan in savings, and earning "+salary+"￥ monthly, I'm considering my investment options. Can you provide some advice on bank products?",
    "If I make "+salary+" RMB each month and have a bank balance of "+saving+" yuan, what financial suggestions would you offer?",
    "I'm looking to invest my money wisely. My monthly income is "+salary+" yuan and my bank balance is "+saving+"￥. Can you suggest some suitable bank products?",
    "Having a bank balance of "+saving+" yuan and a monthly salary of ￥"+salary+", I'm keen on exploring investment opportunities. Suggest some suitable products?",
    "Assist me in choosing appropriate banking products. Assuming I earn "+salary+" yuan / month, and hold a balance of rmb "+saving+".",
    "I've deposited "+saving+" Yuan in the bank. My current yearly income is around "+salary*12+" yuan. Can you advise on which products are available for purchase?",
    "I possess "+saving+" yuan in savings along with salary of "+salary+" ￥/month. Could you provide recommendations for bank products?",
    "Earning "+salary+" yuan monthly, I maintain a balance of rmb "+saving+" in my bank account. In order to broaden my income streams, I'm seeking guidance on investment options. Can you offer some insights?",
    "Within my bank account, I've stored "+saving+" Yuan. With an estimated annual income of approximately "+salary*12+" yuan, I'm curious about the available product options. Can you inspire me a little bit?",
    "Could you assist me in selecting suitable bank products? Considering I earn RMB"+salary+" monthly and maintain a balance of "+saving+" yuan.",
    "Exploring investment avenues, I possess a bank balance of "+saving+" Yuan and earn a yearly salary of "+salary*12+" RMB. Any recommendations on potential products?",
    "With "+saving+" yuan saved and a monthly income of rmb "+salary+", I'm interested in investment opportunities. Can you suggest any bank products?",
    "After diligently saving, my bank account now holds "+saving+" RMB, while my monthly salary stands at "+salary+" Yuan. For investment in bank products, I seek your advice. What would you recommend?",
    "With "+saving+" yuan stored in savings and a monthly earning of "+salary+" Yuan, I'm evaluating my investment prospects. Could you offer any guidance?",
    "If I earn "+salary+" ￥ monthly and possess a bank balance of "+saving+" yuan, what financial recommendations would you propose? Any suggestions for bank products?",
    "Considering my bank balance of ￥"+saving+" and monthly salary of "+salary+" yuan, I'm eager to invest wisely. Could you suggest suitable bank products?",
    "With "+saving+" yuan in my bank account and a monthly income of rmb"+salary+", I'm eager to explore investments.",
    "Could you aid me in selecting suitable banking products? Assuming I earn "+salary+" Yuan monthly and maintain a balance of ￥"+saving+".",
    "I've deposited "+saving+" yuan in my bank account. With an annual income of around "+salary*12+" yuan, I'm seeking advice on available purchase options.",
    "My savings amount to "+saving+" yuan, complemented by a monthly salary of ￥ "+salary+". Any kindly suggestions on bank products?",
    "Getting "+salary+" Yuan every month, I've managed to save "+saving+" yuan in my bank account. Seeking to diversify, I'm interested in investment options. Any recommendations?",
    "Having accumulated "+saving+" yuan in my bank account, my yearly income stands at approximately "+salary*12+" RMB. Can you provide insights into available products?",
    "Assist me in making informed choices regarding bank products. Given a monthly income of "+salary+" rmb and a balance of "+saving+" Yuan.",
    "With "+saving+" Yuan in savings and a monthly salary of ￥ "+salary+", I'm actively seeking investment opportunities.",
    "Considering my savings of "+saving+" yuan and monthly income of "+salary+" rmb, I'm eager to explore investment avenues. Can you recommend appropriate products?",
    "I've accumulated "+saving+" Yuan in my bank account, alongside a monthly salary of "+salary+" yuan. I want your advice on investing in bank products.",
    "My bank account reflects about"+saving+" Yuan in savings and ￥ "+salary+" in monthly income. Could you offer guidance on suitable financial products?",
    "Given a monthly income of ￥ "+salary+" and a bank balance of "+saving+" yuan, what banking products would you recommend? Show your expertise.",
    "With "+saving+" yuan saved up and a monthly income of rmb "+salary+", I'm interested in exploring investment options.",
    "I possess "+saving+" yuan in savings, accompanied by a monthly salary of ￥ "+salary+". Can you provide insights into potential investing chance?",
    "With a bank balance of "+saving+" yuan and a monthly salary of "+salary+"￥, I'm eager to invest wisely. Can you suggest suitable bank products?",
    "Seeking to optimize my finances, I've saved "+saving+" yuan and earn "+salary+" rmb monthly. Could you recommend some bank products for investment?",
    "My monthly income is "+salary+" yuan, and I've saved "+saving+" yuan in my bank account. Wanna guidance on investing in bank products. Anything want to say?",
    "Having amassed "+saving+" ￥ in my bank account and obtianing "+salary+" yuan monthly, I'm keen on exploring investments. suggest suitable products",
    "With a monthly salary of "+salary+" yuan and a bank balance of "+saving+" yuan, I'm looking for advice on investing. Any recommendations?",
    "I'm evaluating investment options with "+saving+" yuan in savings and a monthly salary of "+salary+" yuan."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_recommend_1st_person_positive(productName, productType): 
    texts = [
    "Based on the information provided, it appears that "+productName+" would be a suitable option for you.",
    "Allow me to review for a while... Perhaps "+productName+" would suit your needs. It falls under the category of "+productType+".",
    "I'm delighted to assist you. After careful consideration, I believe investing in a "+productType+" would be advisable. Such as "+productName+".",
    "Considering the details shared, "+productName+" stands out as a promising option for you.",
    "Let me analyze these... "+productName+" seems like a fitting choice. It is a kind of "+productType+".",
    "Glad to be of assistance. After getting your information, I think that "+productName+" could be beneficial for you.",
    "I'm here to help. In my view "+productName+" aligns well with your requirements.",
    "Let's take a look... How about "+productName+"? It's a "+productType+" that could suit your needs.",
    "It's my pleasure to serve you. After examining the details, I recommend considering "+productName+" as an option.",
    "After considering your circumstances, "+productName+" emerges as a strong selection for your needs.",
    "After thinking of the provided information, I believe "+productName+" would be a wise choice.",
    "Let's see... What about "+productName+"? It could be a good deal for you, because of your needs.",
    "I'm so glad to help. After a thorough planning, I suggest "+productName+", belongs to the class of "+productType+".",
    "By reviewing the information you provided, "+productName+" could be a promising choice.",
    "Let me assess the details. Ah, "+productName+" might be a suitable recommendation. It fits within the "+productType+" series.",
    "Happy to help you. Based on the information at hand, "+productName+", a kind of "+productType+", seems like a suitable choice.",
    "I'm at your service. After evaluating the info, it seems that "+productName+" would be an appropriate chance for you.",
    "Consider your options, how about "+productName+"? It's a "+productType+" that could meet your requirements.",
    "It's my pleasure to provide guidance. After careful consideration, I recommend "+productName+" as a potential option.",
    "After assessing your situation, "+productName+" looks like a strong candidate for your consideration."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_recommend_1st_person_negative():
    texts = [
    "I'm sorry, but due to your poor financial condition, I'm unable to recommend any products for you.",
    "Considering your savings and income, there are nothing available here for you —— they all carry too much risk.",
    "Sorry. There are no products matching your savings and income here.",
    "Thinking of your savings and earnings, there aren't any options good enough here, they all have excessive risk for you.",
    "No suitable products can fit with your balance and income at this time.",
    "I regret to inform you that, based on your financial status, I cannot recommend any products.",
    "Completely no offensive, but for your account balance and earnings, there are no appropriate choices.",
    "Unfortunately, due to your current financial situation, I can't propose anything.",
    "Your savings and income level are too weak to find any products.",
    "Regrettably, there are no products that match your level in balance and salary.",
    "Given your financial position, I'm unable to offer any product recommendations because they have higher requirements.",
    "After analyzing your account balance and earnings, there are no suitable options to recommend."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_prompt_recommend_3rd_person(saving, salary):
    # return a prompt of client in 3rd person perspective, Recommend
    texts = [
    "With a bank balance of "+saving+" yuan and a monthly salary of RMB "+salary+" yuan, a client might be interested in exploring investment opportunities. Can you recommend anything suitable?",
    "If a user earns "+salary+" yuan/month and has "+saving+" RMB as a balance in the bank, assist in selecting appropriate bank products. What would you say?",
    "Having stored "+saving+" ￥ in the bank, and with a current yearly income of approximately "+salary*12+" Yuan, one of my friends wanted to seek insights into which products can be bought.",
    "If someone makes "+salary+" Yuan each month and has a balance of "+saving+" ￥, assistance can be provided in selecting appropriate bank products.",
    "Considering a bank balance of about "+saving+" yuan and a monthly salary of ￥"+salary+", someone might be keen on exploring investment opportunities. suggest some suitable products?",
    "With "+saving+" yuan saved up and a monthly income of rmb"+salary+" , a client might consider investment options. Can you suggest some bank products for investment to him / her?",
    "Having saved up money, and now with "+saving+" yuan in the bank account and a salary of "+salary+" yuan per month, someone may be considering investing in bank products. What would you recommend?",
    "Give suggestions about this: With "+saving+" yuan accumulated in savings and "+salary+" Yuan earned monthly, a friend of mine might be considering investment.",
    "If a user makes "+salary+"￥ each month and has a bank balance of "+saving+" yuan, what financial advice would be beneficial? Can bank products be recommended?",
    "If someone is looking to invest savings wisely, with a monthly income of "+salary+" RMB and a bank balance of "+saving+" yuan, suitable bank products can be suggested.",
    "With a bank balance of "+saving+"RMB and a monthly salary of rmb "+salary+", someone may be keen on exploring investment opportunities. Can suitable products be recommended?",
    "Assisting in choosing appropriate banking products, assuming a user earns "+salary+" RMB per month and holds a balance of rmb"+saving+".",
    "If "+saving+" yuan is deposited in the bank, and with a current annual income of around "+salary*12+" rmb, advice can be provided on available purchase choices.",
    "With a bank balance of "+saving+" ￥ and a monthly salary of "+salary+" yuan, someone may be eager to explore investment opportunities. Can suitable products be suggested?",
    "Considering savings of "+saving+" Yuan and a monthly income of "+salary+" yuan, a client may be interested in exploring investment chances. Can appropriate products be recommended?",
    "With "+saving+" yuan saved up and a monthly income of "+salary+" yuan, someone might be interested in exploring investment options.",
    "If "+saving+" yuan is accumulated in the bank account and "+salary+" Yuan is earned monthly, a user may be considering investing in bank products. What would you say?",
    "With "+saving+" yuan in savings and a monthly income of "+salary+", someone may be seeking guidance on suitable products in the bank. Can assistance be provided?",
    "If the monthly income is "+salary+" yuan and the bank balance is "+saving+" yuan, someone might be looking for advice on investing in bank products. Can recommendations be offered?",
    "If evaluating investment options with "+saving+" yuan in savings and a monthly salary of "+salary+" yuan, suitable bank products can be suggested. Is that ok?"
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_recommend_3rd_person_positive(productName, productType): 
    texts = [
    "Based on the information provided, it seems that "+productName+" would be a suitable option for him/her.",
    "By referring the details, a type of "+productType+" called "+productName+" can as a potential recommendation for his/her consideration.",
    "After thinking carefully, "+productName+" appears to be a fitting choice given his / her circumstances.",
    "Let's see... How about "+productName+"? It could be a good option for him / her, considering his/her needs.",
    "On evaluation, "+productName+" stands out as a potential recommendation for the client. It belongs to the "+productType+" category.",
    "Taking the information at hand, I think "+productName+" is a promising option for this client. This is a kind of "+productType+"."
    "Considering this user's situation, "+productName+" seems like a suitable answer.",
    "After analyzing the data, "+productName+" seems to be a potential solution for this individual's requirements.",
    "Via assessment, "+productName+" appears to align well with this client's requirements.",
    productName+" seems like a good choice for this user.",
    "In my opinion, "+productName+" (a type of "+productType+") is an ideal selection for this client."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_recommend_3rd_person_negative():
    texts = [
    "Apologies, but given his / her financial circumstances, recommendations are not feasible at this time.",
    "Considering the balance and earnings of this user, there are no suitable options available; all present too much risk for him / her.",
    "There aren't any products with enough safty aligning with the balance and income of this client at the moment.",
    "Regrettably, based on the financial status of the one in your prompt, product recommendations cannot be made because of risk.",
    "Taking into account balance and earnings of the client, there are no appropriate choices with risk low enough.",
    "Unfortunately, due to the current financial situation of this user, the currency stream is not enough, so product suggestions cannot be provided.",
    "Considering the balance and income level of the client, there are no products available.",
    "Regrettably, there are no products that match the balance and salary of this one.",
    "Given the financial position of him/her, recommendations cannot be offered at this time.",
    "Considering the account balance and earnings of this one, there are no suitable options to recommend."
    ]
    return texts[random.randint(0, len(texts)-1)]


# Evaluate: Evaluate whether the proposal of investment raised by client is feasible or not.

def generate_prompt_evaluate_1st_person_known(saving, salary, productName):
    # return a prompt of client in 1st person perspective, Evaluate, which could have a certain response (positive / negative)
    texts = [
    "Do you think I could buy "+productName+" based on my current financial ability? (saving: ￥"+saving+", salary: ￥"+salary+"/month)",
    "If I earn RMB"+salary+" per month, having "+saving+" yuan in your bank, is it wise to invest money on "+productName+"?",
    "What if I invest on "+productName+" since I obtain "+salary*12+" yuan every year and now I have balance in the bank about rmb "+saving+"? Will you recommend this?",
    "Considering my current salary ("+salary+" rmb), with a balance of ￥"+saving+" in the bank, do you think it's feasible for me to purchase "+productName+"?",
    "With an income of RMB"+salary+" monthly and "+saving+" Yuan saved in my bank account, I'm planning about investing in "+productName+". What are your thoughts? Any Opinion?",
    "Given that I earn approximately "+salary*12+" (RMB) annually and have a bank balance of about "+saving+" Yuan, would it be advisable for me to hold a "+productName+"?",
    "I wonder if it's a good idea for me to buy "+productName+" given my current salary ("+salary+"￥ per month) and savings (RMB "+saving+"). What do you think?",
    "With a monthly income of RMB "+salary+" and a balance of "+saving+" yuan under my management, I'm considering whether purchasing "+productName+" is a wise decision or not.",
    "If my monthly salary is "+salary+"yuan/month and my savings amount to "+saving+" yuan, do you think it's a good move for me to invest in "+productName+"?",
    "Considering my annual earnings of around "+salary*12+" rmb and a bank balance of "+saving+" yuan, should I focus on buying "+productName+"?"
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_evaluate_1st_person_positive(productName):
    texts = [
    "Yes, I think "+productName+" fits you well, according to your financial situation provided.",
    "According to evaluating, I think "+productName+" could be a good investment for you, because your financial condition could afford the risk of it, and the profit potentiality is expectable.",
    "This is a good choice in my view, the return value is appropriate, considering your bank account currency stream.",
    "Indeed, I believe "+productName+" suits you, based on the provided information about your financial situation.",
    "After evaluation, I am of the opinion that "+productName+" could be a promising selection for you. Your financial condition seems capable of managing the associated risks, and the profit potentially is considerable.",
    "From my perspective, this appears to be a reasonable choice. The expected return aligns well with your income level.",
    "Yes, I do think that "+productName+" is a good option for you, given the details of your financial circumstance.",
    "Based on my consideration, I believe that "+productName+" could be a suitable investment selection for you. Your financial position seems to support this choice, and the potential returns and risks.",
    "In my opinion, this is a wise choice for you. Considering your financial circumstances.",
    "I agree that "+productName+" could help. It fit with your ability to invest and take risk for returning.",
    "After viewing your financial details, I am willing to suggest "+productName+". It seems to be a good choice based on your financial situation.",
    "Considering the information provided, I believe that "+productName+" is a suitable product for you. It appears to offer a good balance between the risk and potential returns.",
    "Based on the information of your financial status, I am confident in recommending "+productName+". It is well-suited to your financial circumstances."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_evaluate_1st_person_negative(productName):
    texts = [
    "No, this is too much for you, the investment on this product may fail because the risk is too high considering about the profit as well.",
    "I do not prefer to recommend buying this, is a risky strategy to make this investment based on your financial situation.",
    "Considering your income and balance, I think this"+productName+"is too much risky for you. I suggest that you could try more conservative investment assets with lower risk for loss.",
    "This investment seems too dangerous for your currency situation. It carries a high level of risk relative to the potential profit.",
    "I suggest against purchasing this product. It has to much potential cost for loss given your financial circumstances.",
    "Based on your income and balance, I don't think "+productName+" is one of the suitable options for you. I recommend exploring safer investment opportunities with lower risk.",
    "This might be too much of a gamble for you. We couldn't take investment like bidding. The risk involved outweighs the potential gains.",
    "I'd oppose for going for this option. It's too unsafe given your current financial position.",
    "After thinking carefully of your financial situation, I don't believe "+productName+" is a good fit. It carries too much risk compared to potential returns.",
    "I suggest avoiding this investment. It's too risky given your current financial status. It could earn a lot for you, but also might cost you more probably.",
    "No, this seems too risky for you. Investing in this product might lead to failure due to the high level of risk, especially considering the potential profit.",
    "I wouldn't recommend holding this. It's too risky given your financial situation, I don't think it's a wise investment.",
    "Considering your income and balance, I don't think "+productName+" is a great choice for you. I suggest exploring another conservative plan with lower risk."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_prompt_evaluate_3rd_person_known(saving, salary, productName):
    texts = [
    "Should a user believe he / her could afford to buy "+productName+" based on the current salary? (saving: ￥"+saving+", salary: ￥"+salary+"/month)",
    "If earning RMB"+salary+" per month, with "+saving+" yuan in their bank, would it be wise for a client to invest money in "+productName+"?",
    "What if one buys "+productName+" since they earn "+salary*12+" Yuan every year and now have a balance in the bank of about "+saving+" yuan? Would you recommend this?",
    "Thinking for the current salary and savings balance: ("+salary+" per month, "+saving+" Yuan), should this user consider that could purchase "+productName+"?",
    "With an income of RMB"+salary+" per month and a balance of "+saving+" yuan in the bank, is it feasible for a user to invest in "+productName+"?",
    "Given an annual income of approximately "+salary*12+" rmb and a bank balance of about ￥ "+saving+" , should this user consider buying "+productName+"?",
    "If the monthly salary is RMB"+salary+" and the savings amount to "+saving+" yuan, what's your opinion on this user investing in "+productName+"?",
    "Considering an annual earning of about "+salary*12+" Yuan and a bank balance of rmb "+saving+", should the client go to purchase"+productName+"?",
    "With a income of RMB "+salary+"monthly and a balance of "+saving+" yuan in the bank account, would it be good for this user to buy "+productName+"?",
    "Does this individual have chance to invest in "+productName+" given the monthly salary of RMB "+salary+" and current savings of "+saving+" ￥?"
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_evaluate_3rd_person_positive(productName):
    texts = [
    "Yes, this "+productName+" fits him/her well, given the provided financial situation.",
    "According to evaluation, it is believed that "+productName+" could serve as a good investment for this user. The financial condition appears capable of managing the associated risks, and the potential for profit is promising.",
    "From the perspective, choosing "+productName+" seems to be a wise decision. The expected return value aligns well with the financial situation of this individual.",
    "Indeed, I suggests that "+productName+" is a suitable option for this client. The financial position seems to support this choice, and the potential returns are huge enough.",
    "After careful consideration of the financial details, it is concluded that "+productName+" is a reasonable choice. It shall be a fit option based on the financial situation of this user.",
    "Considering the information provided, it is believed that "+productName+" shall be suggested for this user. It seems to give a good balance between the risk and potential returns.",
    "Based on the financial status at present, it is suggested that "+productName+" is a wise option for the client.",
    "According to the evaluation, "+productName+" is to be a suitable option for this individual. The financial situation supports this choice. It takes low risk and high return comparatively.",
    "After reviewing the financial details, I conclude that "+productName+" is a suitable choice for this user. It matches well with their financial circumstances and goals.",
    "Analyzing the the financial situation let me believe that "+productName+" is a suitable investment option for this client. It seems to offer favorable returns given their current financial standing."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_evaluate_3rd_person_negative(productName):
    texts = [
    "I wouldn't recommend this investment. It's a too risky strategy for this user's financial situation, he might have not enough currency if potential hazard happens.",
    "Considering this user's income and balance, I don't think "+productName+" is a good choice. I suggest exploring more conservative investment assets with lower risk for loss.",
    "This investment appears too risky for the client. The potential for failure outweighs the potential gains, given their financial situation. Or he / she should have more earning or saving.",
    "He/she might need to reconsider this investment. The risk involved is too high for the current financial standing.",
    "Based on the client's income and balance, this might not be a reasonable option. There might exist safer investment opportunities for him/her with lower risk.",
    "This investment idea could be too risky for the client. The potential losses would let people worry a lot comparing with the potential gains.",
    "Considering the financial situation of this user, I don't recommend "+productName+". It's too risky given the income and balance. Instead he / she needs a more moderate plan.",
    "The client may want to avoid this investment selection. It's no safe for the financial position he / she has now.",
    "He/she should be cautious about this investment. The financial situation is fragile to the risk."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_prompt_evaluate_1st_person_unknown(productName):
    texts = [
    "Do you think I should consider purchasing "+productName+"?",
    "Considering  would it be wise to invest in "+productName+"?",
    "What's your opinion on me for buying "+productName+"?",
    "Should I think about acquiring "+productName+" for investment at this time?",
    "Is it a good idea in your view for me to invest in "+productName+"?",
    "Do you believe "+productName+" is a suitable choice for me?",
    "Would it be a smart way for me to buy "+productName+"?",
    "What do you recommend to me for purchasing "+productName+"?",
    "Is it worthy for me to consider investing on "+productName+"?",
    "Should I include "+productName+" in my investment portfolio?"
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_evaluate_1st_person_unknown():
    texts = [
    "I could have a look on your proposal, but firstly you need to give me your 2 kinds of financial information: salary and balance.",
    "Sorry, I cannot give you accurate judgement if I do not know how much you earn monthly and your saving in the bank.",
    "To let me help you, please let me be acknowledged on how much yuan you have in the bank, and what is your earning per month or yearly. Otherwise I cannot make wise choice for you.",
    "Please inform me your balance and income each month, so I will help you with reasonable answer.",
    "I can think about your proposal, but before that, you'll need to provide me with two pieces of financial information: how much (rmb) you earn and your balance.",
    "I'm sorry, but I can't provide you with good advice if I don't know your earnings per month and your savings in the bank.",
    "To assist you effectively, please inform me of your bank balance and monthly income in ￥. Without this information, I won't be able to make informed decisions for you.",
    "First thing, kindly share with me your monthly balance and income, please.",
    "Before proceeding, I'll need to know two key financial details from you: your monthly salary and your current saving.",
    "Apologies, but without knowledge of your monthly earnings and bank balance, I cannot provide you with an accurate assessment.",
    "To offer assistance, please provide details regarding your bank balance and monthly income in yuan. Without this information, I cannot offer suitable recommendations.",
    "Please give me your balance and income each month to let me assist you effectively.",
    "Before I can offer any advice, I'll need to know your current salary and bank balance.",
    "In order to give you the best advice, I'll need to know how much Yuan you earn each month and your current savings."
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_prompt_evaluate_3rd_person_unknown(productName):
    texts = [
    "Do you think purchasing "+productName+" would be a wise decision?",
    "Considering the options available, is "+productName+" a suitable choice?",
    "Would it be advisable to invest in "+productName+" at this time?",
    "What are your thoughts on acquiring "+productName+"?",
    "Should one consider purchasing "+productName+" given the current circumstances?",
    "Is "+productName+" a good investment opportunity?",
    "Does "+productName+" align well with one's financial goals?",
    "Is it worthy to buy "+productName+"?",
    "What is your opinion regarding "+productName+"?",
    "Does "+productName+" fit within the investment strategy?"
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_evaluate_3rd_person_unknown():
    texts = [
    "I could give advice to the users, but first, I need two financial pieces of information: salary and balance.",
    "Apologies, accurate judgment cannot be given without knowledge of how much one earns monthly and the saving in the bank.",
    "To facilitate assistance, the client needs to provide his/her bank balance and monthly earnings. Otherwise, wise decisions cannot be made for him/her.",
    "Please inform this one of the balance and income each month.",
    "Given knowledge of the monthly balance and income and I could make suggestions.",
    "Without knowing the monthly earnings and bank balance, accurate assessments cannot be provided for user.",
    "In order to offer assistance, the user needs to share the bank balance and monthly income.",
    "To provide informed recommendations, client must provide the balance and income per month.",
    "This user can receive advice for him/her once he / she has access to the monthly salary and bank balance.",
    "Accurate advice cannot be given without knowledge of the client's current salary and bank balance.",
    "This individual could get proposal, but only if provided the two key financial details: salary and balance.",
    "Without knowledge of how much one earns monthly and his / her savings in the bank, accurate judgment cannot be proposed.",
    "To facilitate assistance, it is necessary for the client to disclose the bank balance and monthly earnings. Without this information, informed decisions cannot be made by me.",
    "Please ensure that the necessary information regarding balance and monthly income could be found in what you type for accurate assistance.",
    "The one need assistance is required to let me know the monthly balance and income to proceed effectively.",
    "Without access to the monthly earnings and bank balance, accurate opinion cannot be provided for this individual.",
    "In order to offer informed recommendations, it is essential for the user to disclose his / her balance and monthly income.",
    "To provide advice with reasonable risk and return, it is important for the client to share his / her balance and income per month.",
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_prompt_ask():
    texts = [
    "I want to have some recommendation in bank products.", 
    "Would you like to give me some advice in products?",
    "I want to by some of the assets offered by your bank, any suggestions?",
    "I'm looking for guidance on bank products. Any recommendations?",
    "Could you offer some insights into the bank products available?",
    "I'm interested in exploring options for bank products.",
    "Can you tell me on which bank products to consider?",
    "I'm seeking recommendations for bank products. Could you assist me?",
    "Could you provide some suggestions for bank products?",
    "I'm in need of advice regarding bank products. Can you help?",
    "Would you mind offering some recommendations on bank products?",
    "I'm looking to invest in bank products.",
    "Can you offer some guidance on which bank products are suitable for me?",
    ]
    return texts[random.randint(0, len(texts)-1)]


def generate_response_ask():
    texts = [
    "Sure, firstly I need to know your saving and monthly salary.",
    "Ok, but first some information about your financial situation is required, like how much you earn and save.",
    "Sorry, I could not give you good opinion without knowing your salary and balance, please give me more details.",
    "Sure, but before I proceed, I'll need to gather some information about your financial situation. Could you please share details about your savings and monthly income?",
    "Okay, before I can provide any recommendations, I'll need to understand your financial status better. Can you tell me about your earnings and savings?",
    "Certainly, but in order to give you good advice, I need details your financial position. Like about your income and saving.",
    "I'm happy to help, with a bit more information first. Can you tell me your salary and saving?",
    "Absolutely, but before we proceed, let me gather some information about your financial health condition. Can you tell me about your income and savings?",
    "No problem. Can you provide details about your earnings and savings?",
    "For sure, I need some information about your finances first. Share details with me about your income and saving.",
    "Okay, before we continue, tell me more about your financial situation. Can you provide details about your income and savings?",
    "I'd like to help, but I need to know more about your financial position first. How much yuan you earn now and how much balance you have in the bank?",
    ]
    return texts[random.randint(0, len(texts)-1)]


'''---------- FILE PATHS -----------'''
# get the absolute path of this program
current_script_path = os.path.abspath(__file__)
# get the absolute path of this jupitor notebook without itself
current_directory = os.path.dirname(current_script_path)
# read raw CSV, JSON files
input_file_path = current_directory+'/Churn_Modelling.csv'
output_file_path_1 = current_directory+'./bank_products_and_clients.csv'
vue_public_path = os.path.join(current_directory, '..', '..', 'Vue', 'public')
output_file_path_1_X = os.path.join(vue_public_path, 'products_list.json')
output_file_path_2 = current_directory+'./texts.json'
output_file_path_train = current_directory+'./train_data.json'
output_file_path_validate = current_directory+'./validate_data.json'
output_file_path_test = current_directory+'./test_data.json'
output_file_path_test_huge = current_directory+'./test_data_huge.json'


'''---------- MAIN CODE -----------'''

# store information of all kinds of products into: products_list.json
with open(output_file_path_1_X, 'w+', encoding='utf-8') as output_file_1_X:
    json.dump([part_I, part_II, part_III, part_IV], output_file_1_X, ensure_ascii=False, indent=4)

with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file:
    # read Churn_Modelling.csv
    reader = csv.reader(input_file)
    # get the header
    header = next(reader)

    # there are too much raw data, we just keep 1/24 of them
    rows = list(reader)
    num_of_rows = len(rows)
    new_num_of_rows = num_of_rows // 6
    # randomly choose index of data
    indices_to_keep = random.sample(range(num_of_rows), new_num_of_rows)
    # reset reader
    reader = [rows[i] for i in indices_to_keep]
    
    '''
    sum = 0.0
    for row in reader:
        whole_income = float(row['EstimatedSalary']) * 12 / 10 + float(row['Balance'])
        sum += whole_income
        part_1 = whole_income*0.1   # Cash
        part_2 = whole_income*0.2   # Leverage
        part_3 = whole_income*0.3   # Invest
        part_4 = whole_income*0.4   # Long-term
        print(str(part_1) + "\t" + str(part_2) + "\t" + str(part_3) + "\t" + str(part_4))
    average = sum/10000
    print(average)
    '''

    # add new attr for header
    header.extend(["ProductName","ProductType","DownLimit"])

    # open a new CSV file (bank_products_and_clients.csv), add the header
    with open(output_file_path_1, 'w+', newline='', encoding='utf-8') as output_file_1:
        writer = csv.writer(output_file_1)
        writer.writerow(header)

        # traverse each row of Churn_Modelling.csv, add with new attr into bank_products_and_clients.csv
        for row in reader:
            ''' assume: 10% of salary will finally be stored into the bank account.
            whole income = EstimatedSalary * 12 / 10 + Balance
            Divide whole income into 4 parts of money, each with different usage, used to buy a kind of products. 
            '''
            whole_income = float("%.2f" % (float(row[6]) * 12 / 10 + float(row[5])))   # for decimal part, only keep 2 digits
            part_1 = whole_income*0.1   # Cash
            part_2 = whole_income*0.2   # Leverage
            part_3 = whole_income*0.3   # Invest
            part_4 = whole_income*0.4   # Long-term

            results = []    # record
            # find reasonable products according to respective amount of money
            results.append(filter_and_choose(part_1, part_I))
            results.append(filter_and_choose(part_2, part_II))
            results.append(filter_and_choose(part_3, part_III))
            results.append(filter_and_choose(part_4, part_IV))
            #print(row)

            # add values of new attr
            for result in results:
                #print(result)
                row_temp = row.copy()
                if result is not None:
                    row_temp.extend(result)
                    #print(row_temp)
                    writer.writerow(row_temp)

    print("bank_products_and_clients.csv created successfully.")    
    
    # use bank_products_and_clients.csv to create texts.json
    with open(output_file_path_1, newline='', encoding='utf-8') as output_file_1:
        reader_1 = csv.reader(output_file_1)
        
        with open(output_file_path_2, 'w+', newline='', encoding='utf-8') as output_file_2:
            #output_file_2.write('{\n\t')
            items = []
            ''' structure of items: [["prompt","response"], ["prompt","response"], ...] '''
            for index, row in enumerate(reader_1):
                if index == 0:
                    continue                        # pass the header
                saving = Decimal(row[5])
                salary = Decimal(row[6])
                saving = str(saving.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
                salary = str(salary.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
                productName = row[7]
                productType = row[8]
                downlimit = row[9]
                ''' Here for each data, I know the saving & salary, and the product can buy
                generate conversations about Recommend, with answer 'positive',
                generate conversations about Evaluate-known, with answer 'positive' '''
                # randomly choose person perspective: 1st or 3rd 
                random_number = random.randint(1,4)
                if random_number == 1:
                    prompt = generate_prompt_recommend_1st_person(saving=saving, salary=salary)
                    response = generate_response_recommend_1st_person_positive(productName=productName, productType=productType)
                    conversation_type = 'recommend'
                    attitude = 'positive'
                elif random_number == 2:
                    prompt = generate_prompt_recommend_3rd_person(saving=saving, salary=salary)
                    response = generate_response_recommend_3rd_person_positive(productName=productName, productType=productType)
                    conversation_type = 'recommend'
                    attitude = 'positive'
                elif random_number == 3:
                    prompt = generate_prompt_evaluate_1st_person_known(saving=saving, salary=salary, productName=productName)
                    response = generate_response_evaluate_1st_person_positive(productName=productName)
                    conversation_type = 'evaluate'
                    attitude = 'positive'
                else:
                    prompt = generate_prompt_evaluate_3rd_person_known(saving=saving, salary=salary, productName=productName)
                    response = generate_response_evaluate_3rd_person_positive(productName=productName)
                    conversation_type = 'evaluate'
                    attitude = 'positive'
                items.append([prompt, response, conversation_type, attitude])
            
            ''' generate conversations about Recommend, with answer 'negative',
            generate conversations about Evaluate-known, with answer 'negative' '''
            # generate some too low salary and saving
            for i in range(1, 2000):
                part_I_less = random.randint(500, 12000)    # each part of whole income < minimum product price for that part
                part_II_less = random.randint(500, 35000)
                part_III_less = random.randint(500, 59000)
                part_IV_less = random.randint(500, 80000)
                # split whole income into 2 parts randomly (salary and saving), but no matter how to split, the whole income has determined that it cannot buy anything
                whole_income_less = int(min(part_I_less/0.1, part_II_less/0.2, part_III_less/0.3, part_IV_less/0.4))  # make sure the whole income definitely cannot buy any products
                split_point = random.randint(1, whole_income_less)
                saving = split_point
                salary = Decimal((whole_income_less - split_point)*10/12)
                salary = salary.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                saving = str(saving)
                salary = str(salary)

                # randomly choose person perspective: 1st or 3rd
                random_number = random.randint(1,4)
                if random_number == 1:
                    prompt = generate_prompt_recommend_1st_person(saving=saving, salary=salary)
                    response = generate_response_recommend_1st_person_negative()
                    conversation_type = 'recommend'
                    attitude = 'negative'
                elif random_number == 2:
                    prompt = generate_prompt_recommend_3rd_person(saving=saving, salary=salary)
                    response = generate_response_recommend_3rd_person_negative()
                    conversation_type = 'recommend'
                    attitude = 'negative'
                elif random_number == 3:
                    prompt = generate_prompt_evaluate_1st_person_known(saving=saving, salary=salary, productName=productName)
                    response = generate_response_evaluate_1st_person_negative(productName=productName)
                    conversation_type = 'evaluate'
                    attitude = 'negative'
                else:
                    prompt = generate_prompt_evaluate_3rd_person_known(saving=saving, salary=salary, productName=productName)
                    response = generate_response_evaluate_3rd_person_negative(productName=productName)
                    conversation_type = 'evaluate'
                    attitude = 'negative'
                items.append([prompt, response, conversation_type, attitude])


            '''   ---   Here, we separately dump out a large test set for future test and visualize.   ---   '''
            with open(output_file_path_test_huge, 'w+', encoding='utf-8') as test_huge:
                json.dump(items, test_huge, ensure_ascii=False, indent=4)
                print("test_data_huge.json created successfully.")


            ''' generate conversations about Evaluate-unknown,
            generate conversations about Ask'''
            for i in range(1, 800):
                random_number = random.randint(1, 2)
                if random_number == 1:
                    # randomly choose a product
                    part = parts[random.randint(0, len(parts)-1)]
                    productName = part[random.randint(0, len(part)-1)][0]
                    random_number_2 = random.randint(1, 2)
                    if random_number_2 == 1:
                        prompt = generate_prompt_evaluate_1st_person_unknown(productName=productName)
                        response = generate_response_evaluate_1st_person_unknown()
                        conversation_type = 'evaluate'
                        attitude = 'unknown'
                    else:
                        prompt = generate_prompt_evaluate_3rd_person_unknown(productName=productName)
                        response = generate_response_evaluate_3rd_person_unknown()
                        conversation_type = 'evaluate'
                        attitude = 'unknown'
                else:
                    prompt = generate_prompt_ask()
                    response = generate_response_ask()
                items.append([prompt, response])


            random.shuffle(items)   # reset the order of elements in the list randomly
            
            # set size of train, validate and test part
            total_length = len(items)
            part1_length = math.ceil(total_length * 0.7)
            part2_length = math.ceil(total_length * 0.2)

            # divide data into 3 parts: train, validate, test
            part1_data = items[:part1_length]
            part2_data = items[part1_length:part1_length + part2_length]
            part3_data = items[part1_length + part2_length:]

            # write lists into 3 JSON files
            with open(output_file_path_train, 'w+', encoding='utf-8') as train:
                json.dump(part1_data, train, ensure_ascii=False, indent=4)

            with open(output_file_path_validate, 'w+', encoding='utf-8') as validate:
                json.dump(part2_data, validate, ensure_ascii=False, indent=4)

            with open(output_file_path_test, 'w+', encoding='utf-8') as test:
                json.dump(part3_data, test, ensure_ascii=False, indent=4)

        print("train_data.json, validate_data.json and test_data.json created successfully.")
        print('Num of train data:'+str(len(part1_data)))