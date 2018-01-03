package SwapChain;

public class SearchOptimal {
	private Providers P[];
    private Customer O[];
    private double D;
    private int s[];//基本类型只需要申明引用即可
    private double answer=21400000;
    private int answerSerial[];
    public SearchOptimal(Providers p[],Customer o[],double d)
    {
    	P=p;
    	O=o;
    	D=d;
    	s=new int[P.length];//有多少个基站，则解的序列就有多长
    	answerSerial=new int[P.length];
    }
    public void GetTheOptimal()
    {
    	for (int i=0;i<P[0].CapacityCtr;i++){
    		s[0]=i;
    		search(1);
    		s[0]=0;
    	}
    	System.out.println();
    	String str;
    	str=Double.toString(answer);
    	for (int i=0;i<P.length;i++)
    		str+=" "+answerSerial[i];
    	System.out.println(str);
    	
    }
    private void search(int step)
    {
    	if (step>=P.length)
    	{
    		Provider tmpP[]=new Provider[P.length];
    		double SigmaCapacity=0,SigmaDemand=0;
    		double SigmaCost=0;
    		for (int i=0;i<P.length;i++)
    		{
    			tmpP[i]=new Provider();
    			tmpP[i].x=P[i].x;
    			tmpP[i].y=P[i].y;
    			tmpP[i].Capacity=P[i].capacity[s[i]];
				SigmaCost+=P[i].cost[s[i]];
    			SigmaCapacity+=tmpP[i].Capacity;
    			
    		}
    		Customer tmpO[]=new Customer[O.length];
    		for (int i=0;i<O.length;i++)
    		{
    			tmpO[i]=new Customer();
    			tmpO[i].x=O[i].x;
    			tmpO[i].y=O[i].y;
    			tmpO[i].Demand=O[i].Demand;
    			SigmaDemand+=tmpO[i].Demand;
    		}
    		
    		
    		if (SigmaCapacity<SigmaDemand)
    			return;
    		else
    		{
    			SwapChainSolver scs = new SwapChainSolver(tmpP, tmpO);
    			double mmd = scs.Solver();
    			String str;
            	str="cost:"+Double.toString(SigmaCost);
            	str+=" serial:";
            	for (int i=0;i<P.length;i++)
            		str+=" "+s[i];
            	str+=" mmd:"+mmd;
            	System.out.println(str);
    			if (mmd>D)
    				return;
    			else
    			{
    				
    				if (SigmaCost<=answer)
    				{
    					answer=SigmaCost;
    					for (int i=0;i<P.length;i++)
    						answerSerial[i]=s[i];
    					return;
    				}
    			}
    		}
    	}
    	else
    	{
    		for (int i=0;i<P[step].CapacityCtr;i++){
        		s[step]=i;
        		search(step+1);
        		s[step]=0;
    		}
    	}
    	
    }
}
