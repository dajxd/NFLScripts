library(nflfastR)
library(tidyverse)
library(ggimage)
library(na.tools)
# Pull the week out of the first play too so I cann run this script whenever to update to the latest data
data <- readRDS(url('https://raw.githubusercontent.com/guga31bb/nflfastR-data/master/data/play_by_play_2020.rds'))
week <- data %>% summarize(week) %>% arrange(week)

weeknum <- toString(last(last(week)))
data <- data %>% filter(!is_na(air_yards), play_type == "pass") %>% group_by(posteam) %>% summarize(avg_airyards = mean(air_yards), week) %>% arrange(avg_airyards)
nfl_logos_df <- read_csv("https://raw.githubusercontent.com/statsbylopez/BlogPosts/master/nfl_teamlogos.csv")
chart <- data %>% left_join(nfl_logos_df, by = c("posteam" = "team_code"))
#ggplot(chart, aes(x=reorder(posteam, -avg_airyards), y=avg_airyards)) + labs(x = "Team", y="Average Air Yards", title="Average Air Yards Per Team", subtitle = "2020 Through Week 10") + theme_bw() + theme(axis.title = element_text(size=12), axis.text = element_text(size=10), plot.title = element_text(size = 16), plot.subtitle = element_text(size=14))
#ggsave ('airyards.png', dpi=500)
#print(chart)
chart %>%
ggplot(aes(x = reorder(posteam, avg_airyards), y = avg_airyards)) +
	geom_image(aes(image = url), size = 0.05) +
	labs(x = "Team",
	y = "Average Air Yards",
	caption = "Data from nflfastR",
	title = "Every NFL Team's Average Air Yards",
	subtitle = paste("2020 Through Week", weeknum, sep=" ")) +
	theme_bw() +
	theme(axis.title = element_text(size = 12),
	axis.text = element_text(size = 10),
	plot.title = element_text(size = 16),
	plot.subtitle = element_text(size = 14),
        plot.caption = element_text(size = 12))

ggsave('airyards2.png', dpi=1000)
