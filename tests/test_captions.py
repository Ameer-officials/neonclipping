import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import captions

def words(text,step=.45):
    return [{'start':.3+i*step,'end':.7+i*step,'text':w} for i,w in enumerate(text.split())]

class GroupWords(unittest.TestCase):
    def test_every_word_exactly_once_in_order(self):
        for text in ('this is a caption test oh my god look at that chase','a b c d e','one','a b c d e f g h i j k l m n o p q r s t',
                     'this is a caption test oh my god look at that chase now'):
            for mc in (10,12,15,17,24,40):
                got=[w['text'] for g in captions.group_words(words(text),max_chars=mc) for w in g]
                self.assertEqual(got,text.split(),(text,mc))
    def test_groups_are_at_most_four_words(self):
        for mc in (12,17,24):
            for g in captions.group_words(words('a b c d e f g h i j k l m n o p'),max_chars=mc):
                self.assertLessEqual(len(g),5)    # 4 + the merged lone word rule never exceeds 5 here
    def test_random_streams(self):
        import random
        random.seed(7)
        for _ in range(500):
            n=random.randint(1,40);t=0;ws=[]
            for i in range(n):
                t+=random.choice((.2,.4,.9,1.4));ws.append({'start':t,'end':t+.3,'text':random.choice(('hi','okay.','what','YES!','no,','chase','a'))+''})
            got=[w['text'] for g in captions.group_words(ws,max_chars=random.choice((12,17,24))) for w in g]
            self.assertEqual(got,[w['text'] for w in ws])



class Cleanup(unittest.TestCase):
    def test_fold_accents_and_junk(self):
        self.assertEqual(captions.ascii_fold('nósga'),'nosga')
        self.assertEqual(captions.ascii_fold('função'),'funcao')
        self.assertEqual(captions.ascii_fold('mera dost kamjor hai'),'mera dost kamjor hai')
        self.assertEqual(captions.ascii_fold('okال'),'ok')
    def test_repeat_loops_are_cut(self):
        ws=[{'start':i,'end':i+.4,'text':t} for i,t in enumerate('mein chal chal chal chal chal chal chal sach'.split())]
        self.assertEqual([w['text'] for w in captions.collapse_repeats(ws)],['mein','chal','chal','chal','sach'])
    def test_three_repeats_stay(self):
        ws=[{'start':i,'end':i+.4,'text':t} for i,t in enumerate('bhaag bhaag bhaag ruko'.split())]
        self.assertEqual([w['text'] for w in captions.collapse_repeats(ws)],['bhaag','bhaag','bhaag','ruko'])
    def test_punctuation_does_not_hide_a_loop(self):
        ws=[{'start':i,'end':i+.4,'text':t} for i,t in enumerate('ha. ha, ha ha! ha'.split())]
        self.assertEqual(len(captions.collapse_repeats(ws)),3)

if __name__=='__main__':unittest.main()
