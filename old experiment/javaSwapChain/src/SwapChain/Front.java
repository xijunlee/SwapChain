package SwapChain;

public class Front {
    public int[] set;
    public int length;
	public Front(int size){//¹¹Ôìº¯Êý
    	set=new int[size];
    	length=0;
    }
	public void add(int x)
	{
		set[length++]=x;
	}
}
