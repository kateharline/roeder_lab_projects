### Beginner ###
# where you at homey
getwd()
setwd("~/Documents/class_sp19/quant_gen")
# start activity
df <- data.frame(a = c(1,2,3), b = c(4,5,6), c=c(7,8,9))
# create a vector
v = df$b
v
# create a vector of two
v_2 = df$a[2]
v_2
# multiply first row by second column
mult = as.numeric(df[1,])*as.numeric(df[,2])
mult
# append answer as new column
df$d= mult
head(df)
# row 1 mult first by 2 second by 3 third by 2 fourth by 3
row_mult = c(2, 3, 2, 3)
df_as_matrix <- as.matrix(df[,])
df_as_matrix[1,] = df_as_matrix[1,]*row_mult
df = as.data.frame(df_as_matrix)
head(df)
# save data to file
write.table(df, "Lab1.txt", sep="\t")

### Advanced ###