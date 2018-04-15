#input data
data(iris)
data(cars)
# display the structure
str(iris)
# Take a peek
head(iris)
tail(iris)
# overall view of data
attributes(iris)
names(iris)
# Check distribution of every variable
summary(iris)
# Check mean
mean(iris$Sepal.Length)
# Check median
median(iris$Sepal.Length)
# Check range
range(iris$Sepal.Length)
# Check quartile
quantile(iris$Sepal.Length)
# Check variance
var(iris$Sepal.Length)
# check five-numbers: min, lower hinge, median, upper hinge, max
fivenum(iris$Sepal.Length)
# To display: 
# stats - five-numbers
# n - number of data
# conf - the lower and uppper extremes of notches
# out - number of potential outliers
boxplot.stats(iris$Sepal.Length) 
# find frequencies
table(iris$Sepal.Length)
# Pictorial representation
hist(iris$Sepal.Length)
boxplot(iris$Sepal.Length)
plot(iris$Sepal.Length)
barplot(iris$Sepal.Length[1:10])
pie(iris$Sepal.Length[1:10])
?scatterplot()

curve(dnorm(x, mean = mean(iris$Sepal.Length), sd = sd(iris$Sepal.Length)), add = TRUE)
hist(iris$Petal.Width)
curve(dnorm(x, mean = mean(iris$Petal.Width), sd = sd(iris$Petal.Width)), add = TRUE)
lines(density(iris$Petal.Width), col = "blue", lwd = 3)








