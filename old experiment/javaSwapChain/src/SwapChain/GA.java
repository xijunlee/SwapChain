package SwapChain;

import java.util.Random;

public class GA {
    private Gene[] Population;//��Ⱥ
    private int  PopulationSize;//��Ⱥ��С
    private double Pm;//�������
    private double Pc;//�������
    private double Ps;//ѡ�����
    private Providers P[];
    private Customer O[];
    private double D;
    private final double BigNum=21400000;
    private int IterMax;
    
    public GA(Providers p[],Customer o[],double d)
    //��Ⱥ��С,ѡ����ʣ�������ʣ�������ʣ�P����,O����
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
    	
    	//����ֻ����������Ⱥ��С������,����ʹ��ʱ����Ҫ��ÿ��������г�ʼ��
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
    		
    		//ͳһ���¼�����Ӧ��ֵ
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
//    	//ֻ������һ����ΪGA�����Ž�
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
    //�����ʼ����Ⱥ
    {
    	Random rd=new Random();
    	for (int i=0;i<PopulationSize;i++)
    	{
    		//ĳһ��Ⱦɫ��
    		Population[i]=new Gene(P.length);
    		for (int j=0;j<Gene.GeneLength;j++)
    			Population[i].GeneSerial[j]=rd.nextInt(P[j].CapacityCtr);
    		Population[i].fitness=calc_fitness(Population[i]);
    	}
    }
    
    private void replicate()
    {
    	Gene[] NextPopulation = new Gene[PopulationSize];//������һ����Ⱥ
        for (int i = 0; i < PopulationSize; i++)//����Ⱥ��ÿ�������������
            NextPopulation[i] = new Gene(Gene.GeneLength);

        double[] pi = new double[PopulationSize];
        double FitnessSum = 0;
        //����
        FitnessSum = 0;
        qsort(0, PopulationSize - 1,Population);
        //��ȡ��������Ѿ�Ӣ���ԡ��������Ÿ���ֱ�����������;
        //�����������л�����븴��
        NextPopulation[0] = Population[PopulationSize - 1];
        //�������̶�
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
        //����
        for (int i = 0; i < PopulationSize; i++)
            hash[i] = 0;
        hash[0] = 1;
        //��Ѹ��岻���뽻�����
        for (int i = 1; i < PopulationSize / 2; i++)
        {
            hash[i] = 1;
            int j = 0;//hash[0] = 1;
            while (hash[j] == 1)
            {
                j = PopulationSize/2 + rd.nextInt(PopulationSize/2);
                //�ҵ�һ��hash[j]==0�ģ�������
            }
            hash[j] = 1;
            //Xi,Xj���н���,�����ض���һ��Ⱦɫ��
            
            /*//���㽻��
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
            
            //���㽻��
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
        //����
        for (int k = 0; k < PopulationSize * Gene.GeneLength * Pm; k++)
        {
            //int i = rd.Next(0, PopulationSize);
            int i = rd.nextInt(PopulationSize);//�����ȡ����Xi
            //int ik = rd.Next(0, GENE.GeneLength);//
            int ik = rd.nextInt(Gene.GeneLength);//���ѡȡ��Ҫ����Ļ���λ
            int vk = rd.nextInt(P[ik].CapacityCtr);//��������ֵ
            
            Population[i].GeneSerial[ik] = vk;
        }
    
    }
    
    private double calc_fitness(Gene one)
    {
    	double alpha=5.0,beta=1.0;
    	//����Ϊ�ɵ�����������
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
			
			//�������
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
