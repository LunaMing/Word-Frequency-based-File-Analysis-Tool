import wordcloud


def get_cloud(s):
    w = wordcloud.WordCloud(background_color='white')
    w.generate(s)
    w.to_file('../output/cloud.png')
