package SwapChain;

public class Dominate {
	public int[] set;
    public int length;
	public Dominate(int size){//���캯��
    	set=new int[size];
    	length=0;
    }
	public void add(int x)
	{
		set[length++]=x;
	}
}
