import math
def main ():
    list=[1,8,10]
    print (binarysearch(list,8,0,len(list)-1))

def binarysearch(list,candidate,firstindex,lastindex):
    if(firstindex == lastindex):
        if (list[firstindex]==candidate): return True
        else :return False
    else: mid=round((firstindex+lastindex)/2)
    if(list[mid]==candidate): return True
    if(list[mid]>candidate):
        binarysearch(list,candidate,firstindex,mid-1)
    else: binarysearch(list,candidate,mid+1,lastindex)

if(__name__ == '__main__'): main()
        
        
