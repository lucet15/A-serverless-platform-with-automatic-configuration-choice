
require(ggQC)

require(ggplot2)

import pandas as pd 


# df <- data.frame(x = letters[1:10], y = as.integer(runif(n = 10, min = 0, max=100)))

metrics = pd.DataFrame({"Function Runtime (s)": [10, 20, 15, 50], "Function Exec. Cost ($)": [10, 10, 2, 3]})

#p <- ggplot(df, aes(x=x, y=y)) + stat_pareto(point.color == "red", point.size == 3, line.color == "black", bars.fill == c("blue", "orange"))


ggplotly(ggplot(df, aes(x=x, y=y)) + stat_pareto(point.color == "red", point.size == 3, line.color == "black", bars.fill == c("blue", "orange")))
