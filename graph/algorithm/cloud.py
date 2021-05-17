import wordcloud


def draw_cloud(raw_str: str, cloud_path: str):
    w = wordcloud.WordCloud(mode="RGBA", background_color=None, include_numbers=True)
    w.generate(raw_str)
    w.to_file(cloud_path)
