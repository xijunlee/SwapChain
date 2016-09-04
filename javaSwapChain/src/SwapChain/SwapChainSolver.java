package SwapChain;

//import java.math.*;

public class SwapChainSolver {
    private Provider P[];
    private Customer O[];
    private Match A[];
    //上述为声明数组的引用
    private int match_ctr;
    private final int max_size=10000;
    private final double max_num=21400000;
    
    
    public SwapChainSolver(Provider p[],Customer o[])
    {
    	P=p;O=o;
    	//声明了一个长度为max_size的Match类型数组的引用
    	A = new Match[max_size];
    	match_ctr=0;
    }
    
    public double Solver()
    {
       double mmd=0;
       initiallize_assignment();
       Match extreme_m = new Match();
       while(find_d_satisfiable(extreme_m))
       {
    	   String s= Double.toString(extreme_m.o) + " "
 				   + Double.toString(extreme_m.p) + " "
 				   + Double.toString(extreme_m.w) + " "
 				   + Double.toString(extreme_m.dis);
 				   
 		   System.out.println(s);
    	   swap(A,extreme_m);
       }
       qsort(0,match_ctr-1,A);
       
       //输出结果
       /*System.out.println();
       for (int i=0;i<match_ctr;i++)
 	   {
 		   String s= Double.toString(A[i].o) + " "
 				   + Double.toString(A[i].p) + " "
 				   + Double.toString(A[i].w) + " "
 				   + Double.toString(A[i].dis);
 				   
 		   System.out.println(s);
 	   }*/
       
       mmd=A[match_ctr-1].dis;
       return mmd;
    }
    
    private void initiallize_assignment()
    {
    	Dis_list list[] = new Dis_list[max_size];//声明了max_size个Dis_list类型的引用
    	
    	for (int i=0;i<O.length;i++)
    	{
    	   for (int j=0;j<list.length;j++)
    		   list[j]=new Dis_list();//每个都初始化，相当于C中的memset
    	   //引用类型都要初始化才能使用，数值类型不要初始化
    	   
    	   for (int j=0;j<P.length;j++)
    	   {
    	      list[j].p=j;
    	      list[j].dis=calc_dis(i,j);
    	   }
    	   //按照到o点距离的升序排序
    	   qsort(0,P.length-1,list);
    	   
    	   for (int j=0;j<P.length&&O[i].Demand>0;j++)
    	   {
    		   double tmp = Math.min(O[i].Demand, P[list[j].p].Capacity);
    		   if (tmp>0)
    		   {
    			   Match m=new Match();
    			   m.o=i;
    			   m.p=list[j].p;
    			   m.w=tmp;
    			   m.dis=list[j].dis;
    			   add_match(A, m);
    		   }
    	   }
    	}
       /*qsort(0,match_ctr-1,A);
       for (int i=0;i<match_ctr;i++)
 	   {
 		   String s= Double.toString(A[i].o) + " "
 				   + Double.toString(A[i].p) + " "
 				   + Double.toString(A[i].w) + " "
 				   + Double.toString(A[i].dis);
 				   
 		   System.out.println(s);
 	   }
       
       System.out.println();*/
    }
    
    private void add_match(Match []Matches,Match m)
    //向集合Matches中增添一个匹配m
    {
       boolean flag=false;
       
       for (int i=0;i<match_ctr;i++)
    	   if (m.o==Matches[i].o && m.p==Matches[i].p)
    	   {
    		   Matches[i].w+=m.w;
    		   flag=true;
    		   break;
    	   }
       
       if (flag==false)
       {
    	   Matches[match_ctr++]=m;
       }
       
       P[m.p].Capacity-=m.w;
       O[m.o].Demand-=m.w;
       
       return;
    }
    
    private void sub_match(Match []Matches,Match m)
    {
    	P[m.p].Capacity+=m.w;
    	O[m.o].Demand+=m.w;
    	
    	for (int i=0;i<match_ctr;i++)
    		if (m.o==Matches[i].o && m.p==Matches[i].p)
    		{
    			Matches[i].w-=m.w;
    			if (Matches[i].w==0)
    			{
    				Matches[i]=Matches[match_ctr-1];
    				match_ctr--;
    			}
    			break;
    		}
    	
    	return;
    }
    
    private double calc_dis(int o,int p)
    {
    	return Math.sqrt(Math.pow(O[o].x-P[p].x, 2)+Math.pow(O[o].y-P[p].y,2));
    }
    
    private void qsort(int st,int ed,Dis_list[] a)
    {
    	if (st>=ed)
    		return;
    	int i=st,j=ed;
    	Dis_list tmp=a[i];
    	while (i<j)
    	{
    		while (i<j && a[j].dis>=tmp.dis) j--;
    		if (i<j)
    			a[i]=a[j];
    		while (i<j && a[i].dis<tmp.dis) i++;
    		if (i<j)
    			a[j]=a[i];
    	}
    	a[i]=tmp;
    	qsort(st,i-1,a);
    	qsort(i+1,ed,a);
    	return;
    }
    
    private void qsort(int st,int ed,Match[] a)
    {
    	if (st>=ed)
    		return;
    	int i=st,j=ed;
    	Match tmp=a[i];
    	while (i<j)
    	{
    		while (i<j && a[j].dis>=tmp.dis) j--;
    		if (i<j)
    			a[i]=a[j];
    		while (i<j && a[i].dis<tmp.dis) i++;
    		if (i<j)
    			a[j]=a[i];
    	}
    	a[i]=tmp;
    	qsort(st,i-1,a);
    	qsort(i+1,ed,a);
    	return;
    }
    private void copy_match(Match a,Match b)
    {
    	a.dis=b.dis;
    	a.o=b.o;
    	a.p=b.p;
    	a.w=b.w;
    }
    
    private boolean find_d_satisfiable(Match em)
    //找到满足条件的一个极限匹配,若找到返回true
    {
    	qsort(0,match_ctr-1,A);
    	boolean flag=false;
    	double maxd=A[match_ctr-1].dis;
    	int k=match_ctr-1;
    	Queue Q[]=new Queue[max_size];
    	int hash[]=new  int[max_size];
    	for (int i=0;i<max_size;i++)
    	{	Q[i]=new Queue(); }
    	
    	while(!flag && A[k].dis==maxd &&k>=0)
    	{
    		for (int i=0;i<max_size;i++)
    			hash[i]=0;
    		int head=0,tail=0;
    		hash[A[k].o]=1;
    		Q[head].num=A[k].o;Q[head].parent=-1;
    		tail++;
    		//em=A[k];
    		copy_match(em,A[k]);
    		sub_match(A,em);
    		
    		
    		while(head!=tail && !flag)
    		{
    			int CurrentNode = Q[head].num;
    			if (CurrentNode<O.length)
    			//表示当前处理的是消费者节点
    			{
    				for (int i=0;i<P.length;i++)
    				{
    					double tmp=calc_dis(CurrentNode,i);
    					if (tmp<maxd && hash[i+O.length]==0)
    					{
    						Q[tail].num=i+O.length;
    						Q[tail].parent=head;
    						hash[i+O.length]=1;
    						tail=(tail+1)%max_size;
    					}
    				}
    				 
    			}
    			else
    			{
    				//表示当前处理的是provider节点
    				int pc=CurrentNode-O.length;
    				if (P[pc].Capacity==0)
    				{
    					for (int i=0;i<match_ctr;i++)
    						if (A[i].p==pc && hash[A[i].o]==0)
    						{
    							hash[A[i].o]=1;
    							Q[tail].num=A[i].o;
    							Q[tail].parent=head;
    							tail=(tail+1)%max_size;
    						}
    				}
    				else
    				{
    					flag=true;
    				}
    			
    			}
    			head=(head+1)%max_size;
    		}
    		add_match(A,em);
    		k--;
    	}
    	
    	return flag;
    }
    
    private void swap(Match[] Matches,Match m)
    //注意：java中所有类类型的对象都是引用传递
    {
        sub_match(Matches,m);
        
        int C[]=new int[max_size];//java基本类型的数组对象不需要初始化，只需要声明数组引用就好
        int cl=0;
        while((cl=find_chain(C,m))>0)
        {
        	//chain breaking
        	double ws=max_num;
        	ws=Math.min(P[C[0]-O.length].Capacity,ws);
    		ws=Math.min(O[C[cl-1]].Demand,ws);
    		
    		for (int i=1;i<cl-1;i+=2)
    		{
    			int tmpo=C[i];
    			int tmpp=C[i+1]-O.length;
    			for (int j=0;j<match_ctr;j++)
    				if (Matches[j].o==tmpo && Matches[j].p==tmpp)
    				{
    					ws=Math.min(ws, Matches[j].w);
    					break;
    				}
    		}
    		
    		for (int i=1;i<cl-1;i+=2)
    		{
    			int tmpo=C[i];
    			int tmpp=C[i+1]-O.length;
    			for (int j=0;j<match_ctr;j++)
    				if (Matches[j].o==tmpo && Matches[j].p==tmpp)
    				{
    					Match tmpm=new Match();
    					/*tmpm.dis=Matches[j].dis;
    					tmpm.o=Matches[j].o;
    					tmpm.p=Matches[j].p;
    					tmpm.w=Matches[j].w;*/
    					copy_match(tmpm,Matches[j]);
    					sub_match(Matches,Matches[j]);
    					if (tmpm.w!=ws)
    					{
    						tmpm.w=tmpm.w-ws;
    						add_match(Matches,tmpm);
    					}
    					break;
    				}
    		}
    		
    		//chain matching
    		for (int i=0;i<cl;i+=2)
    		{
    			int tmpo=C[i+1];
    			int tmpp=C[i]-O.length;
    			Match tmpm=new Match();
    			tmpm.o=tmpo;
    			tmpm.p=tmpp;
    			tmpm.w=ws;
    			tmpm.dis=calc_dis(tmpo,tmpp);
    			add_match(Matches,tmpm);
    		}
    		
    		if (O[m.o].Demand==0)
    			break;
        }
        
        //post matching
        if (O[m.o].Demand>0)
        {
        	Match tmpm= new Match();
        	tmpm.o=m.o;
 		    tmpm.p=m.p;
 		    tmpm.w=O[m.o].Demand;
 		    tmpm.dis=calc_dis(tmpm.o,tmpm.p);
 		    add_match(Matches,tmpm);
        }
            
    }
    
    private int find_chain(int[] c,Match m)
    {
    	int cl=0;
    	boolean flag=false;
    	double maxd=m.dis;
    	Queue Q[]=new Queue[max_size];
    	int hash[]=new  int[max_size];
    	for (int i=0;i<max_size;i++)
    	{	Q[i]=new Queue(); hash[i]=0; }
    	
    	int head=0,tail=0;
    	hash[m.o]=1;
    	Q[head].num=m.o;Q[head].parent=-1;
    	tail++;
    	//head遇到tail，表明最底层所有节点都扩展完了，即整棵树都搜索完了
    	
    	while(head!=tail && !flag)
		{
			int CurrentNode = Q[head].num;
			if (CurrentNode<O.length)
			{
				for (int i=0;i<P.length;i++)
				{
					double tmp=calc_dis(CurrentNode,i);
					if (tmp<maxd && hash[i+O.length]==0)
					{
						Q[tail].num=i+O.length;
						Q[tail].parent=head;
						hash[i+O.length]=1;
						tail=(tail+1)%max_size;
					}
				}
			}
			else
			{
				int pc=CurrentNode-O.length;
				if (P[pc].Capacity==0)
				{
					for (int i=0;i<match_ctr;i++)
						if (A[i].p==pc && hash[A[i].o]==0)
						{
							hash[A[i].o]=1;
							Q[tail].num=A[i].o;
							Q[tail].parent=head;
							tail=(tail+1)%max_size;
						}
				}
				else
				{
					flag=true;
					int tmp=head;
					while(tmp>=0)
					{
						c[cl++]=Q[tmp].num;
						tmp=Q[tmp].parent;
					}
				}
			}
			head=(head+1)%max_size;
		}
    	
    	return cl;
    }
}
