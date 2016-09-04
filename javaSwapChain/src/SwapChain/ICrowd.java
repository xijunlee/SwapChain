package SwapChain;

public class ICrowd {
    public int number;
    public double []f;
    public double dis;
    public int rank;
    public ICrowd(int m)
    {
    	f = new double[m];
    	number=0;
    	dis=0;
    	rank=0;
    	for (int i=0;i<m;i++)
    		f[i]=0;
    }
}
