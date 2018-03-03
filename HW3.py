import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.atomic.*;
 
class SearcherThread<T> extends Thread
{
    private T needle;
    private T[] haystack;
    private int start, end, result;
    private AtomicBoolean isFound; //Not using a volatile boolean guarantees the result
    //http://stackoverflow.com/questions/4501223/when-do-i-need-to-use-atomicboolean-in-java
    public SearcherThread(T needle, T[] haystack, int start, int end, AtomicBoolean isFound)
    {
        this.needle = needle;
        this.haystack = haystack;
        this.start = start;
        this.end = end;
        this.isFound = isFound;
        this.result = -1; //not found 
    }
 
    public int getResults()
    {
        return result;
    }
 
    // @override
    public void run() 
    {
        for (int i=start; i<end && !isFound.get() && !Thread.currentThread().isInterrupted(); ++i)
            if (haystack[i].equals(needle)) {
            	result = i;
            	isFound.set(true);
            }
    }   
}
 
public class Searcher
{
    public static <T> int search(T needle, T[] haystack, int numThreads ) throws InterruptedException
    {
        
        ArrayList<SearcherThread<T>> searchers = new ArrayList<>();
        int numItemsPerThread = haystack.length / numThreads;
        int extraItems = haystack.length - numItemsPerThread*numThreads;
        int result = -1;
        AtomicBoolean isFound = new AtomicBoolean(false);
        
        for (int i=0, start=0; i<numThreads; ++i) {
            int numItems = (i<extraItems) ? (numItemsPerThread+1) : numItemsPerThread;
            searchers.add(new SearcherThread<T>(needle, haystack, start, start+numItems, isFound));
            start += numItems;
        }
        for (SearcherThread<T> searcher : searchers) 
            searcher.start();
        for (SearcherThread<T> searcher : searchers) 
            searcher.join();
        for (SearcherThread<T> searcher : searchers) {
            result = searcher.getResults();
            if (result > -1) //if found in any threads , return
            	return result;
        }
        return result; //if not found in any threads, return the initial value
    }
     
    public static void main(String[] args) throws InterruptedException
    {
        int numItems = 10000;
        Integer[] haystack = new Integer[numItems];
        int domainSize = 1000;
        for (int i=0; i<numItems; ++i) 
            haystack[i] = (int)(Math.random() * domainSize);
        int needle = 10;
        List<Integer> indices = Searcher.search(needle, haystack);
        for (int index : indices)
            System.out.println("index: "+index+", value: "+haystack[index]);
    }
}
