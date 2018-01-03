package SwapChain;

public class GenePlus extends Gene{
   public double [] f;
   public double crowd_dis;
   public int rank;
   public GenePlus(int length)//先进入默认构造函数，然后再进入子构造函数
   {
	   GeneSerial = new int[length];
   	   f = new double[2];
   	   f[0]=0;f[1]=0;
   	   
   }
}
