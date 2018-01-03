package SwapChain;

import java.util.Random;

public class NSGAII {
	//private GenePlus[] Population;//��Ⱥ
	private GenePlus[] Pf;//������Ⱥ
	private GenePlus[] Qs;//�Ӵ���Ⱥ
	private GenePlus[] R;
	private Front[] F;
	private int FrontCount;
	private Dominate[] S;
    private int  PopulationSize;//��Ⱥ��С
    
    private int[] ni;
    private double Pm;//�������
    private double Pc;//�������
    private double Ps;//ѡ�����
    private Providers P[];
    private Customer O[];
    //private double D;
    private final double BigNum=21400000;
    private int IterMax;
    
    
    public NSGAII(Providers p[],Customer o[])
    //��Ⱥ��С,ѡ����ʣ�������ʣ�������ʣ�P����,O����
    {
    	PopulationSize=40;
    	Pm=0.001;
    	Pc=0.01;
    	Ps=0.01;
    	IterMax=50;
    	
    	//Population = new GenePlus[PopulationSize];
    	Pf = new GenePlus[PopulationSize];
    	Qs = new GenePlus[PopulationSize];
    	R = new GenePlus[2*PopulationSize];
//    	S = new Dominate[2*PopulationSize];
//    	F = new Front[2*PopulationSize];
    	//����ֻ�����������ã���û�жԶ����ʼ������ʵ��������
//    	ni = new int[2*PopulationSize];
    	P=p;
    	O=o;
    	//D=d;
    	GenePlus.GeneLength=P.length;
    	
    	//����ֻ����������Ⱥ��С������,����ʹ��ʱ����Ҫ��ÿ��������г�ʼ��
    }
    
    private void NonDominatedSort(GenePlus[] pop)
    //����Ⱥ�и���ֲ�
    {
    	F = new Front[pop.length+1];
    	S = new Dominate[pop.length];
    	ni = new int[pop.length];
    	
    	F[0] = new Front(pop.length);
    	for (int i=0;i<pop.length;i++)
    	{
    		S[i]=new Dominate(pop.length);
    		ni[i]=0;
    		for (int j=0;j<pop.length;j++)
    		{
    			if (i!=j)
    			{
    				if (IsDominated(pop[i],pop[j]))
    				{	
    					//i֧��j
    					S[i].add(j);
    				}
    				else if (IsDominated(pop[j],pop[i]))
    				{
    					//j֧��i
    					ni[i]+=1;
    				}
    			}
    		}
    		if (ni[i]==0)
    		{	
    			pop[i].rank=0;
    		    F[0].add(i);
    		}
    	}
    	FrontCount=0;
    	while(F[FrontCount].length!=0)
    	{
    		Front H = new Front(pop.length);
    		for (int k=0;k<F[FrontCount].length;k++)
    		{
    			int i=F[FrontCount].set[k];
    			for (int l=0;l<S[i].length;l++)
    			{
    				int j=S[i].set[l];
    				ni[j]-=1;
    				if (ni[j]==0)
    				{
    					pop[j].rank=FrontCount+1;
    					H.add(j);
    				}
    			}
    		}
    		FrontCount++;
    		F[FrontCount]=H;
    	}
    }
    
    private void SortInFrontWithOperator(Front f,GenePlus[] pop)
    {
        ICrowd[] I = new ICrowd[f.length];//��������ô�������
    	
    	for (int i=0;i<f.length;i++)
    	{
    		I[i] = new ICrowd(2);//ֻ�������Ż�Ŀ��
    		int num=f.set[i];
    		I[i].number=num;
    		I[i].rank=pop[num].rank;
    		I[i].dis=pop[num].crowd_dis;
    	}
    	
    	sort_with_operator(0,f.length-1,I);
    	
    	for (int i=0;i<f.length;i++)
    	f.set[i]=I[i].number;
    	
    }
    
    private void sort_with_operator(int st,int ed,ICrowd[] a)
    {
    	if (st>=ed)
    		return;
    	int i=st,j=ed;
    	ICrowd tmp = a[i];
    	while (i<j)
    	{
    		//while (i<j && a[j].f[m]>tmp.f[m]) j--;
    		while (i<j && CrowdCmp(tmp,a[j])) j--;
    		if (i<j) a[i]=a[j];
    		//while (i<j && a[i].f[m]<=tmp.f[m]) i++;
    		while (i<j && CrowdCmp(a[i],tmp)) i++;
    		if (i<j) a[j]=a[i];
    	}
    	a[i]=tmp;
    	sort_with_operator(st,i-1,a);
    	sort_with_operator(i+1,ed,a);
    }
    
    private void CalcCrowdingDistance(Front f,GenePlus[] pop)
    {
    	ICrowd[] I = new ICrowd[f.length];//��������ô�������
    	
    	for (int i=0;i<f.length;i++)
    	{
    		I[i] = new ICrowd(2);//ֻ�������Ż�Ŀ��
    		int num=f.set[i];
    		I[i].number=num;
    		I[i].f[0]=pop[num].f[0];
    		I[i].f[1]=pop[num].f[1];
    	}
    	
        for (int m=0;m<2;m++)
        {
        	sort_for_different_objective(0,f.length-1,I,m);
        	I[0].dis=BigNum;
        	I[f.length-1].dis=BigNum;
        	for (int i=1;i<f.length-1;i++)
        		I[i].dis=I[i].dis+(I[i+1].f[m]-I[i-1].f[m])/(I[f.length-1].f[m]-I[0].f[m]);
        }
        
        for (int i=0;i<f.length;i++)
        {
        	int num=I[i].number;
        	pop[num].crowd_dis=I[i].dis;
        }
    }
    
    private boolean CrowdCmp(ICrowd a,ICrowd b)
    //ӵ���ȱȽ����ӣ��ж�a<b?true:false
    {
    	if (a.rank<b.rank)
    		return true;
    	else if (a.rank==b.rank)
    	{
    		if (a.dis>=b.dis)
    			return true;
    	}
    	return false;
    }
    
    private void sort_for_different_objective(int st,int ed,ICrowd[] a,int m)
    {
    	if (st>=ed)
    		return;
    	int i=st,j=ed;
    	ICrowd tmp = a[i];
    	while (i<j)
    	{
    		while (i<j && a[j].f[m]>tmp.f[m]) j--;
    		if (i<j) a[i]=a[j];
    		while (i<j && a[i].f[m]<=tmp.f[m]) i++;
    		if (i<j) a[j]=a[i];
    	}
    	a[i]=tmp;
    	sort_for_different_objective(st,i-1,a,m);
    	sort_for_different_objective(i+1,ed,a,m);
    }
     
    public void Solver()
    {
    	Initialize(Pf);
    	MakeNewPop(Pf,Qs);
    	
    	int iter=0;
    	while(iter<IterMax)
    	{
    		mergePQ(R,Pf,Qs);
    		NonDominatedSort(R);
    		Pf = new GenePlus[PopulationSize];//��ո���
    		int i=0;
    		for (i=0;(count_length(Pf)+F[i].length<=PopulationSize);i++)
    		{
    			CalcCrowdingDistance(F[i],R);
    			mergePR(F[i],R,Pf);
    		}
    		
    		if (i<FrontCount)
    		{
    			CalcCrowdingDistance(F[i],R);

    		    SortInFrontWithOperator(F[i],R);
    		
    		    mergePR(F[i],R,Pf,PopulationSize-count_length(Pf));
    		}
    		
    		MakeNewPop(Pf,Qs);

    		System.out.println("��"+Integer.toString(iter)+"�ε������:");
    		PrintToScreen(Pf);
 
    		iter++;
    	}
    	
    	System.out.println("the final:");
    	PrintToScreen(Pf);
    }
  
    private void PrintToScreen(GenePlus[] pop)
    {
    	String out;
    	for (int i=0;i<PopulationSize;i++)
    	{
    		out="";
    		out+="mmd="+Double.toString(Pf[i].f[0])
    				+"  cost="+Double.toString(Pf[i].f[1])+"  Serial: ";
          for (int j=0;j<GenePlus.GeneLength;j++)
        	out+=Integer.toString(Pf[i].GeneSerial[j])+" ";  
          System.out.println(out);
    	}
    	System.out.println();
    }
    
    private void mergePQ(GenePlus[] r,GenePlus[] p,GenePlus[] q)
    {
    	for (int i=0;i<p.length;i++)
    		r[i]=p[i];
    	for (int i=0;i<q.length;i++)
    		r[i+p.length]=q[i];
    	return;
    }
    
    private void mergePR(Front f,GenePlus[] r,GenePlus[] p)
    {
    	int j=count_length(p);
    	for (int i=0;i<f.length;i++)
    	{
    		int num=f.set[i];
    		p[j] = new GenePlus(P.length);
    		copy_A_to_B(r[num],p[j]);
    		j++;
    	}
    }
    
    private void mergePR(Front f,GenePlus[] r,GenePlus[] p,int length)
    {
    	int j=count_length(p);
    	for (int i=0;i<length;i++)
    	{
    		int num=f.set[i];
    		p[j] = new GenePlus(P.length);
    		copy_A_to_B(r[num],p[j]);
    		j++;
    	}
    }
    
    private int count_length(Object[] x)
    {
    	int length=0;
    	while(length<PopulationSize && x[length]!=null)
    		length++;
    	return length;
    }
    
    private boolean IsDominated(GenePlus a,GenePlus b)
    {
    	boolean flag=false;
    	if ((a.f[0]<=b.f[0])&&(a.f[1]<=b.f[1]))
    	{
    		if ((a.f[0]<b.f[0])||(a.f[1]<b.f[1]))
    			flag=true;
    	}
    	
    	return flag;
    }
    
    private void Initialize(GenePlus[] pop)
    //�����ʼ����Ⱥ
    {
    	Random rd=new Random();
    	for (int i=0;i<pop.length;i++)
    	{
    		//ĳһ��Ⱦɫ��
    		pop[i]=new GenePlus(P.length);
    		for (int j=0;j<GenePlus.GeneLength;j++)
    			pop[i].GeneSerial[j]=rd.nextInt(P[j].CapacityCtr);
    		pop[i].f[0]=calc_mmd(pop[i]);
    		pop[i].f[1]=calc_cost(pop[i]);
    	}
    	NonDominatedSort(pop);
    	for (int i=0;i<pop.length;i++)
    		pop[i].fitness=calc_fitness_according_to_rank(pop[i]);
    }
    
    private void qsort(int st,int ed,GenePlus[] a)
    {
    	if (st>=ed)
    		return;
    	int i=st,j=ed;
    	GenePlus tmp=a[i];
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
    
    private void MakeNewPop(GenePlus[] Pop,GenePlus[] NewPop)
    {
    	Replicate(Pop,NewPop);
    	Cross(NewPop);
    	Mutation(NewPop);
    	NonDominatedSort(NewPop);
    	for (int i=0;i<NewPop.length;i++)
    		NewPop[i].fitness=calc_fitness_according_to_rank(NewPop[i]);
    }
    
    private void Replicate(GenePlus[] pop,GenePlus[] NextPopulation)
    {
        for (int i = 0; i < PopulationSize; i++)//����Ⱥ��ÿ�������������
            NextPopulation[i] = new GenePlus(GenePlus.GeneLength);

        double[] pi = new double[PopulationSize];
        double FitnessSum = 0;
        //����
        FitnessSum = 0;
        qsort(0, PopulationSize - 1,pop);
        //��ȡ��������Ѿ�Ӣ���ԡ��������Ÿ���ֱ�����������;
        //�����������л�����븴��
        copy_A_to_B(pop[PopulationSize - 1],NextPopulation[0] );
        //�������̶�
        for (int i = 0; i < PopulationSize; i++)
            FitnessSum += pop[i].fitness;

        pi[0] = pop[0].fitness / FitnessSum;
        for (int i = 1; i < PopulationSize; i++)
            pi[i] = pop[i].fitness / FitnessSum + pi[i - 1];

        Random rd = new Random();
        for (int i = 1; i < PopulationSize; i++)
        {
            double tmp = rd.nextDouble();
            int copy = 0;
            for (int j = 0; j < PopulationSize; j++)
                if (tmp <= pi[j])
                { copy = j; break; }
            //NextPopulation[i] = pop[copy];
            copy_A_to_B(pop[copy],NextPopulation[i]);
        }

    }
    
    private void copy_A_to_B(GenePlus A,GenePlus B)
    {
    	
    	B.crowd_dis=A.crowd_dis;
    	B.fitness=A.fitness;
    	B.f[0]=A.f[0];B.f[1]=A.f[1];
    	B.rank=A.rank;
    	for (int i=0;i<Gene.GeneLength;i++)
    		B.GeneSerial[i]=A.GeneSerial[i];
    }
    
    private void Cross(GenePlus[] pop)
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
            int cross_point = rd.nextInt(GenePlus.GeneLength);
            if (i != 0 && j != 0)
            {
               int tmp;
               for (int k=cross_point;k<GenePlus.GeneLength;k++)
               {
            	   tmp=Population[i].GeneSerial[k];
            	   Population[i].GeneSerial[k]=Population[j].GeneSerial[k];
            	   Population[j].GeneSerial[k]=tmp;
               }
            }*/
            
            //���㽻��
            int cross_point1 = rd.nextInt(GenePlus.GeneLength);
            int cross_point2 = rd.nextInt(GenePlus.GeneLength);
            if (i != 0 && j != 0)
            {
               int tmp;
               for (int k=cross_point1;k<=cross_point2;k++)
               {
            	   tmp=pop[i].GeneSerial[k];
            	   pop[i].GeneSerial[k]=pop[j].GeneSerial[k];
            	   pop[j].GeneSerial[k]=tmp;
               }
            }
        }
    }
    
    private void Mutation(GenePlus[] pop)
    {
    	Random rd = new Random();
        //����
        for (int k = 0; k < PopulationSize * GenePlus.GeneLength * Pm; k++)
        {
            //int i = rd.Next(0, PopulationSize);
            int i = rd.nextInt(PopulationSize);//�����ȡ����Xi
            //int ik = rd.Next(0, GENE.GeneLength);//
            int ik = rd.nextInt(GenePlus.GeneLength);//���ѡȡ��Ҫ����Ļ���λ
            int vk = rd.nextInt(P[ik].CapacityCtr);//��������ֵ
            
            pop[i].GeneSerial[ik] = vk;
        }
    
    }
    
    private double calc_mmd(GenePlus one)
    {
    	double mmd=BigNum;
    	Provider tmpP[]=new Provider[P.length];
    	double SigmaCapacity=0,SigmaDemand=0;
		for (int i=0;i<P.length;i++)
		{
			tmpP[i]=new Provider();
			tmpP[i].x=P[i].x;
			tmpP[i].y=P[i].y;
			tmpP[i].Capacity=P[i].capacity[one.GeneSerial[i]];
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
		
		if (SigmaCapacity>=SigmaDemand)
		{
			SwapChainSolver scs = new SwapChainSolver(tmpP, tmpO);
			mmd = scs.Solver();
		}
		
		return mmd;
    }
    
    private double calc_fitness_according_to_rank(GenePlus one)
    {
    	return 1000.0/(one.rank+1.0);
    }
    
    private double calc_cost(GenePlus one)
    {
    	
		double SigmaCost=0;
		for (int i=0;i<P.length;i++)
		  SigmaCost+=P[i].cost[one.GeneSerial[i]];

		return SigmaCost;
    }
}
