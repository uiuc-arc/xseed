inp="projectdata.csv"
import pandas as pd
df = pd.read_csv(inp)
topic_dict=dict()
#print(df['Topics'])
groups=[
    ['machine-learning', 'ml', 'machine-learning-algorithms', 'machine-learning-library'],
    ['natural-language-processing', 'nlp'],
    ['artificial-intelligence', 'ai', ],
    ['deep-learning', 'deep-neural-networks', 'deeplearning', 'deep-learning-tutorial'],
    ['neural-networks', 'neural-network'],
    [ 'bayesian-inference', 'bayesian', 'bayesian-statistics', 'bayesian-networks'],
    ['probabilistic-programming', 'probabilistic']

    ]
def get_topics():
    for t in list(df['Topics']):
        if isinstance(t, str) and len(t) > 0:
            for g in t.strip().split("::"):
                gr = [k for k in groups if g in k]
                if len(gr) > 0:
                    gr=gr[0]
                    topic_dict[gr[0]] = topic_dict.get(gr[0], 0) + 1
                else:
                    topic_dict[g] = topic_dict.get(g,0)+1
    other=0
    for topic in sorted(topic_dict.keys(), key=lambda x:topic_dict[x], reverse=True):
        if topic_dict[topic]>=4:
            print("{}, {}".format(topic, topic_dict[topic]))
        else:
            other+=topic_dict[topic]
    print("other, {}".format(other))


def get_stats():
    import numpy as np
    for k in ["Stars", "Releases", "Contributors", "Commits"]:
        print("{}, {}".format(k, np.median(df[k])))
print("Stats:")
get_stats()
print("Topics:")
get_topics()
