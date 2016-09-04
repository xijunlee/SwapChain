package SwapChain;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class Main {
    public static Providers P[];
    public static Provider Ps[];
    public static Customer O[];
    public static final int max_size=10000;
	public static void main(String[] args) throws Exception {
        //要双斜杠，否则单斜杠+字母会被编译器识别成转义字符
		//ReadData("C:\\Users\\XIJUN\\Desktop\\swapchain\\PCProblem\\alldata.txt");
	    /*GA ga = new GA(P,O,100);//第三个参数是准许的最大距离D
	    ga.Solver();*/
//	    NSGAII nsga = new NSGAII(P,O);
//	    nsga.Solver();
		ReadDataForSwapChain("C:\\Users\\XIJUN\\Desktop\\swapchain\\PCProblem\\pydata.txt");
		SwapChainSolver sc = new SwapChainSolver(Ps,O);
		double mmd=sc.Solver();
        System.out.println(mmd);
	
       /* ReadData("C:\\Users\\XIJUN\\Desktop\\swapchain\\PCProblem\\alldata.txt");
		SearchOptimal so=new SearchOptimal(P,O,10);//第三个参数是准许匹配的最大距离D
		so.GetTheOptimal();*/
	}
	
	public static void ReadDataForSwapChain(String FilePath)
	{
		try {
		       FileReader fr = new FileReader(FilePath);   //创建一个FileReader对象   从磁盘读
		       BufferedReader br = new BufferedReader(fr);    //创建一个BufferedReader对象

		       String line = "";                   //定义一个String变量line用来接每次读一行的结果
		       String[][] a = new String[2000][];
		       int lineCount=0;
		       while(br.ready()){                             //如果文件准备好，就继续读
		         line=br.readLine();//读一行
		         a[lineCount] = new String[line.split(" ").length];
		         a[lineCount] = line.split(" ");
		         lineCount++;
		       }
		       br.close();                                   //关闭流
		       fr.close();                                   //关闭流
		       
		       //初始化providers,customers
		       Ps = new Provider[Integer.parseInt(a[0][0])];
		       //这里只是声明了数组引用，并没有实例化对象
		       O = new Customer[Integer.parseInt(a[Ps.length+1][0])];
		       //按照数据特征，处理读入provider的数据
		       for (int i=1;i<=Ps.length;i++)
		       {
		    	  Ps[i-1]=new Provider();//实例化对象，并将对象传给相应引用
		    	  Ps[i-1].x=Double.parseDouble(a[i][0]);
		    	  Ps[i-1].y=Double.parseDouble(a[i][1]);
                  Ps[i-1].Capacity=Double.parseDouble(a[i][2]);
		       }
		       //按照数据特征，处理读入customer的数据
		       for (int i=Ps.length+2,k=0;i<lineCount;i++)
		       {
		          O[k]=new Customer();
		    	  O[k].x=Double.parseDouble(a[i][0]);
		          O[k].y=Double.parseDouble(a[i][1]);
		          O[k].Demand=Double.parseDouble(a[i][2]);
		          k++;
		       }
		     }
		     catch (IOException ex) {
		       ex.printStackTrace();
		     }
	}
	
	public static void ReadData(String FilePath)
	{
		try {
		       FileReader fr = new FileReader(FilePath);   //创建一个FileReader对象   从磁盘读
		       BufferedReader br = new BufferedReader(fr);    //创建一个BufferedReader对象

		       String line = "";                   //定义一个String变量line用来接每次读一行的结果
		       String[][] a = new String[2000][];
		       int lineCount=0;
		       while(br.ready()){                             //如果文件准备好，就继续读
		         line=br.readLine();//读一行
		         a[lineCount] = new String[line.split(" ").length];
		         a[lineCount] = line.split(" ");
		         lineCount++;
		       }
		       br.close();                                   //关闭流
		       fr.close();                                   //关闭流
		       
		       //初始化providers,customers
		       P = new Providers[Integer.parseInt(a[0][0])];
		       //这里只是声明了数组引用，并没有实例化对象
		       O = new Customer[Integer.parseInt(a[P.length+1][0])];
		       //按照数据特征，处理读入provider的数据
		       for (int i=1;i<=P.length;i++)
		       {
		    	  P[i-1]=new Providers();//实例化对象，并将对象传给相应引用
		    	  P[i-1].x=Double.parseDouble(a[i][0]);
		    	  P[i-1].y=Double.parseDouble(a[i][1]);
		    	  P[i-1].CapacityCtr=Integer.parseInt(a[i][2]);
		    	  P[i-1].capacity = new double[P[i-1].CapacityCtr];
		    	  P[i-1].cost = new double[P[i-1].CapacityCtr];
		    	  for (int j=0;j<P[i-1].CapacityCtr;j++)
		    	  {
		    		  P[i-1].capacity[j]=Double.parseDouble(a[i][j+3]);
		    		  P[i-1].cost[j]=Double.parseDouble(a[i][j+3+P[i-1].CapacityCtr]);
		    	  }
		    	  
		       }
		       //按照数据特征，处理读入customer的数据
		       for (int i=P.length+2,k=0;i<lineCount;i++)
		       {
		          O[k]=new Customer();
		    	  O[k].x=Double.parseDouble(a[i][0]);
		          O[k].y=Double.parseDouble(a[i][1]);
		          O[k].Demand=Double.parseDouble(a[i][2]);
		          k++;
		       }
		     }
		     catch (IOException ex) {
		       ex.printStackTrace();
		     }
	}
}
