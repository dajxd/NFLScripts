### NFL 4 Which Teams Run The Most On 3rd and Long
library(nflfastR)
library(tidyverse)
library(ggimage)
library(na.tools)
data <- readRDS(url('https://raw.githubusercontent.com/guga31bb/nflfastR-data/master/data/play_by_play_2020.rds'))

week <- data %>% summarize(week) %>% arrange(week)

weeknum <- toString(last(last(week)))
fileConn<-file("names.txt")
writeLines(c(names(data)), fileConn)
close(fileConn)
data <- data %>% filter(down == 3, pass == 1 | rush == 1, ydstogo > 5) %>% group_by(posteam) %>% summarize(posteam, play_type, ydstogo, mean_run=mean(rush), mean_pass=mean(pass)) %>% arrange(desc(mean_run))
print(data)



nfl_logos_df <- read_csv("https://raw.githubusercontent.com/statsbylopez/BlogPosts/master/nfl_teamlogos.csv")
chart <- data %>% left_join(nfl_logos_df, by = c("posteam" = "team_code"))
chart %>%
ggplot(aes(x = reorder(posteam, mean_run), y = mean_run)) +
	geom_image(aes(image = url), size = 0.03) +
	labs(x = "Team",
	y = "Rushing percentage",
	caption = "Data from nflfastR",
	title = "Rushing Percentage on 3rd and > 5 by Team",
	subtitle = paste("2020 Through Week", weeknum, sep=" ")) +
	theme_bw() +
	theme(axis.title = element_text(size = 12),
	axis.text = element_text(size = 10),
	plot.title = element_text(size = 16),
	plot.subtitle = element_text(size = 14),
        plot.caption = element_text(size = 12),
	axis.text.x=element_blank()
	)


ggsave('dumbrush.png', dpi=500)
