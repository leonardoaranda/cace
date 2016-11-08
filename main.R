library(ggplot2)
library(kohonen)
library(cluster)
library(RColorBrewer)
library(rgl)
library(corrplot)
library(arules)
library(GGally)

set.seed(15485863)

sites <- read.csv("cace_metrics.csv",row.names=18)
categories <- read.csv("cace_metrics_v2.csv")

# Exploro algunos datos
str(sites)
head(sites,n=3)
summary(sites)

table(categories$category_l2)

sites$visit_time <- as.numeric(sites$visit_time)
sites$category_l2 <- categories$category_l2
sites <- subset(sites,complete.cases(sites))
sites <- subset(sites,visits>50000)

sites <- subset(sites,category_l2 == "marketplace" | category_l2 == "retail" | category_l2 == "travel")

sites$country_rank_bucket <- discretize(sites$country_rank,method="frequency",categories=4,labels=c(1,2,3,4))

table(sites$country_rank_bucket)

# Genero dataframes con numéricos
sites.num <- sites[c(1,8,10:17)]
sites.num.st <- scale(sites.num)
sites.num.st.dist <- dist(sites.num.st)


col <- brewer.pal(n=4, name="Spectral")


pairs(sites.num,col=col[sites$country_rank_bucket],upper.panel = NULL,pch=19,cex=1.5)
pairs(sites.num,col=sites$category_l2,pch=19,cex=1.5)


hclust.methods <- c("ward.D","single","complete","average")

for(method in hclust.methods){
  h <- hclust(sites.num.st.dist,method=method)
  cop <- cophenetic(h)
  corr <- cor(sites.num.st.dist,cop)
  print(paste(corr,"-----",method))
}

rs <- array()
ss <- array()

for(k in 2:40){
  km <- kmeans(sites.num.st,centers=k)
  rs[k] <- km$tot.withinss
  s <- silhouette(km$cluster,sites.num.st.dist)
  ss[k] <- mean(s[,3])
  print(ss[k])
}

qplot(1:40,rs) + geom_line() + labs(x="Tamaño Cluster",y="SSE",title="SSE según K")



sites.kmeans <- kmeans(sites.num.st,centers=8)
sil <- silhouette(sites.kmeans$cluster,sites.num.st.dist)
sites$cluster <- sites.kmeans$cluster

plot(sil,main="Silhouette k-means para K=6")

sites.hclust <- hclust(dist(sites.num.st),method='average')

plot(sites.hclust)

# Analisis por cluster
table(sites$cluster,sites$category_l2)
t(aggregate(sites[,c(1,7,8,10:17)],list(sites$cluster),mean))

table(sites$cluster,sites$category_l2)

sites.pca <- prcomp(sites.num.st)

sites.pca.pc1 <- sites.pca$x[,1]
sites.pca.pc2 <- sites.pca$x[,2]
sites.pca.pc3 <- sites.pca$x[,3]

plot3d(sites.pca.pc1,sites.pca.pc2,sites.pca.pc3,col=sites$cluster,size=10)

sites.corr <- cor(sites.num)

corrplot(sites.corr,method="color",col=brewer.pal(n=10, name="Spectral"),tl.col="black",main="Correlación entre variables",line=-2,type="lower")


subset(sites,cluster==7)
