package SwapChain;

import java.util.Random;

public class GA {
    private Gene[] Population;//种群
    private int  PopulationSize;//种群大小
    private double Pm;//变异概率
    private double Pc;//交叉概率
    private double Ps;//选择概率
    private Providers P[];
    private Customer O[];
    private double D;
    private final double BigNum=21400000;
    private int IterMax;
    
    public GA(Providers p[],Customer o[],double d)
    //种群大小,选择概率，交叉概率，变异概率，P集合,O集合
    {
    	PopulationSize=100;
    	Pm=0.00001;
    	Pc=0.01;
    	Ps=0.01;
    	IterMax=50;
    	
    	Population = new Gene[PopulationSize];
    	P=p;
    	O=o;
    	D=d;
    	Gene.GeneLength=P.length;
    	
    	//这里只是声明了种群大小的引用,真正使用时，还要对每个对象进行初始化
    }
    
    public void Solver()
    {
    	initialize();
    	/*for (int i=0;i<PopulationSize;i++)
    	{
            String s;
            s=Double.toString(Population[i].fitness);
            
            System.out.println(s);
    	}*/
    	
    	int iter=0;
    	double theBestFitness=-2*BigNum;
    	int theBestSerial[]=new int[P.length];
    	while(iter < IterMax)
    	{
    		
    		replicate();
    		
    		cross();
    		
    		mutation();
    		
    		//统一重新计算适应度值
    		for (int i=0;i<PopulationSize;i++)
        		Population[i].fitness=calc_fitness(Population[i]);
    		
    		iter++;
    		
    		for (int i=0;i<PopulationSize;i++)
        	{
                String s;
                s=Double.toString(Population[i].fitness);
                if (Population[i].fitness>=theBestFitness)
                {
                	theBestFitness=Population[i].fitness;
                	for (int j=0;j<P.length;j++)
    					theBestSerial[j]=Population[i].GeneSerial[j];
                }
                
                double SigmaCost=0;
				for (int j=0;j<P.length;j++)
					SigmaCost+=P[j].cost[Population[i].GeneSerial[j]];
                s+=" "+ SigmaCost;
                System.out.println(s);
        	}
        	
        	System.out.println();
    	}
    	
    	System.out.println();
    	
//    	qsort(0,PopulationSize-1,Population);
//    	//只输出最后一个作为GA的最优解
//    	for (int i=PopulationSize-1;i<PopulationSize;i++)
//    	{
//            String s;
//            s=Double.toString(Population[i].fitness);
//            double SigmaCost=0;
//			for (int j=0;j<P.length;j++)
//				SigmaCost+=P[j].cost[Population[i].GeneSerial[j]];
//            s+=" "+ SigmaCost+" ";
//            for (int j=0;j<P.length;j++)
//			{
//			   s+=Integer.toString(Population[i].GeneSerial[j])+ " ";
//			}
//            System.out.println(s);
//    	}
    	String s;
      s=Double.toString(theBestFitness);
      double SigmaCost=0;
		for (int j=0;j<P.length;j++)
			SigmaCost+=P[j].cost[theBestSerial[j]];
      s+=" "+ SigmaCost+" ";
      for (int j=0;j<P.length;j++)
		{
		   s+=Integer.toString(theBestSerial[j])+ " ";
		}
      System.out.println(s);
    	System.out.println();
    }
    
    private void qsort(int st,int ed,Gene[] a)
    {
    	if (st>=ed)
    		return;
    	int i=st,j=ed;
    	Gene tmp=a[i];
    	while (i<j)
    	{
    		while (i<j && a[j].fitness>=tmp.fitness) j--;
    		if (i<j)
    			a[i]=a[j];
    		while (i<j && a[i].fitness<tmp.fitness) i++;
    		if (i<j)
    			a[j]=a[i];
    	}
    	a[i]=tmp;
    	qsort(st,i-1,a);
    	qsort(i+1,ed,a);
    	return;
    }
    
    private void initialize()
    //随机初始化种群
    {
    	Random rd=new Random();
    	for (int i=0;i<PopulationSize;i++)
    	{
    		//某一条染色体
    		Population[i]=new Gene(P.length);
    		for (int j=0;j<Gene.GeneLength;j++)
    			Population[i].GeneSerial[j]=rd.nextInt(P[j].CapacityCtr);
    		Population[i].fitness=calc_fitness(Population[i]);
    	}
    }
    
    private void replicate()
    {
    	Gene[] NextPopulation = new Gene[PopulationSize];//声明下一代种群
        for (int i = 0; i < PopulationSize; i++)//对种群中每个个体进行声明
            NextPopulation[i] = new Gene(Gene.GeneLength);

        double[] pi = new double[PopulationSize];
        double FitnessSum = 0;
        //复制
        FitnessSum = 0;
        qsort(0, PopulationSize - 1,Population);
        //采取“保留最佳精英策略”，将最优个体直接替代最差个体;
        //但最差个体仍有机会参与复制
        NextPopulation[0] = Population[PopulationSize - 1];
        //构造轮盘赌
        for (int i = 0; i < PopulationSize; i++)
            FitnessSum += Population[i].fitness;

        pi[0] = Population[0].fitness / FitnessSum;
        for (int i = 1; i < PopulationSize; i++)
            pi[i] = Population[i].fitness / FitnessSum + pi[i - 1];

        Random rd = new Random();
        for (int i = 1; i < PopulationSize; i++)
        {
            double tmp = rd.nextDouble();
            int copy = 0;
            for (int j = 0; j < PopulationSize; j++)
                if (tmp <= pi[j])
                { copy = j; break; }
            NextPopulation[i] = Population[copy];
        }

        for (int i = 0; i < PopulationSize; i++)
            Population[i] = NextPopulation[i];
    }
    
    private void cross()
    {
    	int[] hash = new int[PopulationSize];
        Random rd = new Random();
        //交叉
        for (int i = 0; i < PopulationSize; i++)
            hash[i] = 0;
        hash[0] = 1;
        //最佳个体不参与交叉操作
        for (int i = 1; i < PopulationSize / 2; i++)
        {
            hash[i] = 1;
            int j = 0;//hash[0] = 1;
            while (hash[j] == 1)
            {
                j = PopulationSize/2 + rd.nextInt(PopulationSize/2);
                //找到一个hash[j]==0的，就跳出
            }
            hash[j] = 1;
            //Xi,Xj进行交叉,交换特定的一段染色体
            
            /*//单点交叉
            int cross_point = rd.nextInt(Gene.GeneLength);
            if (i != 0 && j != 0)
            {
               int tmp;
               for (int k=cross_point;k<Gene.GeneLength;k++)
               {
            	   tmp=Population[i].GeneSerial[k];
            	   Population[i].GeneSerial[k]=Population[j].GeneSerial[k];
            	   Population[j].GeneSerial[k]=tmp;
               }
            }*/
            
            //两点交叉
            int cross_point1 = rd.nextInt(Gene.GeneLength);
            int cross_point2 = rd.nextInt(Gene.GeneLength);
            if (i != 0 && j != 0)
            {
               int tmp;
               for (int k=cross_point1;k<=cross_point2;k++)
               {
            	   tmp=Population[i].GeneSerial[k];
            	   Population[i].GeneSerial[k]=Population[j].GeneSerial[k];
            	   Population[j].GeneSerial[k]=tmp;
               }
            }
        }
    }
    
    private void mutation()
    {
    	Random rd = new Random();
        //变异
        for (int k = 0; k < PopulationSize * Gene.GeneLength * Pm; k++)
        {
            //int i = rd.Next(0, PopulationSize);
            int i = rd.nextInt(PopulationSize);//随机抽取个体Xi
            //int ik = rd.Next(0, GENE.GeneLength);//
            int ik = rd.nextInt(Gene.GeneLength);//随机选取需要变异的基因位
            int vk = rd.nextInt(P[ik].CapacityCtr);//产生变异值
            
            Population[i].GeneSerial[ik] = vk;
        }
    
    }
    
    private double calc_fitness(Gene one)
    {
    	double alpha=5.0,beta=1.0;
    	//以上为可调的两个因子
    	double fitness=0;
    	Provider tmpP[]=new Provider[P.length];
    	double SigmaCapacity=0,SigmaDemand=0;
		for (int i=0;i<P.length;i++)
		{
			tmpP[i]=new Provider();
			tmpP[i].x=P[i].x;
			tmpP[i].y=P[i].y;
			tmpP[i].Capacity=P[i].capacity[one.GeneSerial[i]];
			SigmaCapacity+=tmpP[i].Capacity;
			/*String s = Double.toString(tmpP[i].x) + " " +
					   Double.toString(tmpP[i].y) + " " +"1 "+
					   Double.toString(tmpP[i].Capacity);
			System.out.println(s);*/
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
			fitness=-2*BigNum;
		else
		{
			SwapChainSolver scs = new SwapChainSolver(tmpP, tmpO);
			double mmd = scs.Solver();
			
			//调试输出
			/*System.out.printlUn(mmd);*/
			/*String s= new String();
			for (int i=0;i<P.length;i++)
			{
			   s+=Integer.toString(one.GeneSerial[i])+ " ";
			}
			System.out.println(s);*/
			
			if (mmd>D)
				fitness=-BigNum;
			else
			{
				double SigmaCost=0;
				for (int i=0;i<P.length;i++)
					SigmaCost+=P[i].cost[one.GeneSerial[i]];
				fitness=-alpha*SigmaCost+beta*(D-mmd);
			}
		}
		 
        return fitness;
    }
    
}
