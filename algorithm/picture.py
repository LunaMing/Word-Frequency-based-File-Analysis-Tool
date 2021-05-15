import matplotlib.pyplot as plt
import wordcloud


def cloud(raw_str: str, cloud_name: str):
    w = wordcloud.WordCloud(background_color='white')
    w.generate(raw_str)
    w.to_file('output/' + cloud_name)


def plotdata(data):
    plt.plot(data)
    plt.show()
