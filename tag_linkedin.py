import glob
import pickle

# Read files
files = glob.glob("./scraping/programming/*.txt")

prog_sent = []
for f in files:
    sent = pickle.load(open(f, "rb"))
    prog_sent.append(sent)

posts_flatten = [y for x in prog_sent for y in x]
set_posts_flatten = list(set(posts_flatten))

print('Length posts: ', len(posts_flatten))
print('Set length posts: ', len(set_posts_flatten))

print('\nExample 1: ')
print(set_posts_flatten[20])
print('\n\n' + set_posts_flatten[-345])