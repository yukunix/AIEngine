myfunction<-function(){
  path="/Users/yukunix/git/AIEngine/R"
  temp=list.files(path=path,pattern="*.csv")
  obj=read.csv(paste(path,temp[1],sep="/"))
  obj<-obj[c("Date","Close")]
  colnames(obj)[2]<-paste("col",1,sep="")
  total=obj
  for(i in 2:length(temp)){
    obj=read.csv(paste(path,temp[i],sep="/"))
    obj<-obj[c("Date","Close")]
    colnames(obj)[2]<-paste("col",i,sep="")
    total=merge(total,obj)
  }
  return (total)
}

total<-myfunction()
show(total)