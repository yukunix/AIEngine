
csvsLoader<-function(path){
  
  temp=list.files(path=path,pattern="*.csv")
  obj=read.csv(paste(path,temp[1],sep="/"))
  obj<-obj[c("Date","Close")]
 
  colnames(obj)[2]<-temp[1]

  total=obj
  for(i in 2:length(temp)){
    obj=read.csv(paste(path,temp[i],sep="/"))
    obj<-obj[c("Date","Close")]

    colnames(obj)[2]<-temp[i]
    total=merge(total,obj)
  }

  return (total)
}
path="C:/Users/PWang/Documents/finance/snp500_top10"
total1<-csvsLoader(path)
show(total1)
total1$Date <-strptime(total1$date,format="%y-%m-%d")
