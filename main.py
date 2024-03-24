# global imports
import geopandas as gpd
import matplotlib as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import plotly.express as px
import plotly.io as py
import re
import seaborn as sns
from typing import Counter
from wordcloud import WordCloud


# local imports
from clean import raw_data_cleaner

df = pd.read_csv("ufo_sightings.csv", on_bad_lines="skip", low_memory=False)
df2 = raw_data_cleaner(df)

# filtered df
filt = (df2["shape"].isin(["unknown", "light", "flare", "nan"]) | (df2["duration (seconds)"] > 3600) | (df2["duration (seconds)"] < 5))
filt_df = df[~filt]

# plotting UFO sighting across the world
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create the plot
fig = px.scatter_geo(world, lat='Latitude', lon='Longitude',
                     projection='natural earth',
                     color='Count',
                     size='Count',
                     hover_name='city',
                     hover_data=['Count'],
                     color_continuous_scale='Viridis')

# Add the world map
fig.update_geos(showcountries=True, countrywidth=0.2)

# Layout
fig.update_layout(
    title_text='UFO Sightings',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    )
)
py.write_html(fig, "ufo_sightings.html")

fig.show()

# top cities with UFO sightings
top_cities = (df2[["city", "datetime"]]
.groupby("city")
.count()
.rename(columns={"datetime":"cnt"})
.sort_values("cnt", ascending=False)
).head(10)
print(top_cities)

top_cities.plot.bar(title="Top Cities")

# years of UFO sighting
year_group = (df2[["year", "datetime"]]
.groupby("year")
.count()
.rename(columns={"datetime":"cnt"})
).loc[:2013]

fig = px.line(year_group, x=year_group.index, y=year_group.cnt, title='Visibility of UFOs')
fig.show()
fig.write_html("output.html")

# weekdays of UFO sightings
df2.loc[:, "weekday"] = df2["datetime"].dt.day_name()
df2['weekday'] = pd.Categorical(df2['weekday'], categories=
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
    ordered=True)

weekday_group = (df2[["weekday", "datetime"]]
.groupby("weekday", sort=False)
.count()
.rename(columns={"datetime":"cnt"})
)

print(weekday_group)

fig = px.bar(weekday_group, x=weekday_group.index, y=weekday_group.cnt, labels={'x':'Weekday', 'cnt':'Count'}, title='Count of Sightings by Weekday')
plt.figure(figsize=(10,6))
fig.show()

# monthly UFO sighting pattern
month_group = (df2[["month", "datetime"]]
.groupby("month")
.count()
.rename(columns={"datetime":"cnt"})
)

sns.barplot(x=month_group.index, y=month_group.cnt, data=month_group, palette="mako")
plt.title("UFO observation peak months")

# hourly UFO sighting pattern
hour_group = (df2[["hour", "datetime"]]
.groupby("hour")
.count()
.rename(columns={"datetime":"cnt"})
)

print(hour_group)

plt.figure(figsize=(10,3))
sns.barplot(x=hour_group.index, y=hour_group.cnt, data=hour_group, palette="mako")
plt.title("UFO observation peak hours")

# Most common comments in UFO sighting
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

comments = filt_df['comments']
words = word_tokenize(' '.join(comments))


# Remove punctuation and convert to lower case
words = [word.lower() for word in words if word.isalpha()]
custom_stop_words = ["i", "we", "a", "&", "the", "to", "as", "i", "we", "or", "ISS"]

# Remove stopwords, and filter grammatical wordings
stop_words = set(stopwords.words('english') + custom_stop_words)
words = [word for word in words if word not in stop_words]

tagged = nltk.pos_tag(words)
filtered_words = [word for word, pos in tagged if pos not in ('IN', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')]

# Count the frequency of each word
word_counts = Counter(filtered_words)
print(word_counts.most_common(100))

# wordcloud
cmt = [item for item in filt_df.comments.dropna()]

cmt = " ".join(cmt)

plt.figure(figsize=(18,12))

wordcloud = WordCloud(background_color='whitesmoke', width=2000, height=1000,
                      stopwords=None).generate(cmt)
plt.imshow(wordcloud, interpolation="nearest", aspect='auto')
plt.axis('off')
plt.savefig('wordcloud.png')
plt.title("UFO Wordcloud", size=40)

plt.show()