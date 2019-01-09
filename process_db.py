import sqlite3
import json
import re



"""
def get_text(js):
    if not js['extended_tweet'] is None:
        if not js['extended_tweet']['full_text'] is None:
            return js['extended_tweet']['full_text']
    return(js['text'])
"""


def get_text(data):       
    # Try for extended text of original tweet, if RT'd (streamer)
    try: text = data['retweeted_status']['extended_tweet']['full_text']
    except: 
        # Try for extended text of an original tweet, if RT'd (REST API)
        try: text = data['retweeted_status']['full_text']
        except:
            # Try for extended text of an original tweet (streamer)
            try: text = data['extended_tweet']['full_text']
            except:
                # Try for extended text of an original tweet (REST API)
                try: text = data['full_text']
                except:
                    # Try for basic text of original tweet if RT'd 
                    try: text = data['retweeted_status']['text']
                    except:
                        # Try for basic text of an original tweet
                        try: text = data['text']
                        except: 
                            # Nothing left to check for
                            text = ''
    return text.replace('\n', ' ')

def get_lang(data):
    return data['lang']

t_dict = {'@AmazonHelp':'AtAmazonHelp', '@amazon':'AtAmazonHelp', '@PrimeVideoIn':'AtAmazonHelp', '@AmazonUK':'AtAmazonHelp', '@AmazonESP':'AtAmazonHelp', '@JeffBezos':'AtAmazonHelp', '@AmazonKindle':'AtAmazonHelp' }


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def process_t(t):
    t = replace_all(t, t_dict)
    return t

def process_r(r):
    r = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', 'AtCustomerName', r)
    r = re.sub(r'http\S+', 'AmazonHelpURL', r)
    return r


def open_files(filename):
        filename = 'data_files/'+filename
        i_f = open(filename + '.from',  'w+')
        o_f = open(filename + '.to', 'w+')
        return i_f, o_f

conn = sqlite3.connect('/home/rich/src/concretely/concretely_nmt/tweets.db')

cur = conn.cursor()
cur.execute("SELECT * FROM tweets")

rows = cur.fetchall()
row_count = len(rows)

i_f= open("data_files/input.txt","w+")
o_f= open("data_files/output.txt","w+")
i = 0

for row in rows:
    if i == 0:
        i_f, o_f = open_files('tst2012')
    if i == 100:
        i_f, o_f = open_files('tst2013')
    if i == 200:
        i_f, o_f = open_files('train')
    i += 1
    t = json.loads(row[0])
    #print(row[1])
    r = json.loads(row[1])
    lang=get_lang(r)
#    print("lang={}".format(lang))
    if lang=='en':
        t_text = process_t(get_text(t))
        r_text = process_r(get_text(r))
    #print('{} - {}'.format(get_text(r), get_text(t)))
        i_f.write('{}\n'.format(t_text))
        o_f.write('{}\n'.format(r_text))
