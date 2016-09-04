package SwapChain;

public class Gene {
    public int GeneSerial[];
    public static int GeneLength;
    public double fitness;
    public Gene(int length)
    {
    	GeneSerial = new int[length];
    	fitness = 0;
    }
    public Gene()
    {
    	fitness=0;
    }
}
