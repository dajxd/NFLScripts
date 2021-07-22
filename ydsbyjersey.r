library(nflfastR)
library(tidyverse)
library(ggimage)
data <- readRDS(url('https://raw.githubusercontent.com/guga31bb/nflfastR-data/master/data/play_by_play_2020.rds'))
num <- 1
vec <- c()
while (num < 99){
	fata <- list(data %>% filter(yards_gained == num) %>% filter(rusher_jersey_number == num | receiver_jersey_number == num)%>% summarize(yards_gained, posteam, defteam, rusher_player_name, receiver_player_name, rusher_jersey_number, receiver_jersey_number, jersey_number, game_date))
	vec <- append(vec, fata)
	num <- num + 1
}
c=1
for (i in vec) {
	if ( c < 10){
		cc <- paste("0", c, sep="")
	}
	else {
		cc <- c
	}
	filename <- paste(cc, "yards.csv", sep= '')
	write.table(i, file = filename, sep = "\t", row.names = F)
	c <- c+1
}
