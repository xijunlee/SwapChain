package SwapChain;

import java.io.*;

public class IOData {
	public static void read_data(Providers P[],Customer O[],String FilePath)
	{
		try {
		       FileReader fr = new FileReader(FilePath);   //创建一个FileReader对象   从磁盘读
		       BufferedReader br = new BufferedReader(fr);    //创建一个BufferedReader对象

		       String line = "";                   //定义一个String变量line用来接每次读一行的结果
		       String[][] a = new String[2000][];
		       int lineCount=0;
		       while(br.ready()){                             //如果文件准备好，就继续读
		         line=br.readLine();//读一行
		         a[lineCount] = new String[line.split("\t").length];
		         a[lineCount] = line.split("\t");
		         lineCount++;
		       }
		       br.close();                                   //关闭流
		       fr.close();                                   //关闭流
		       
		       //初始化providers,customers
		       Providers[] p = new Providers[Integer.parseInt(a[0][0])];
		       //这里只是初始化了引用，并没有真正初始化的对象
		       Customer[] o = new Customer[Integer.parseInt(a[p.length+1][0])];
		       //按照数据特征，处理读入provider的数据
		       for (int i=1;i<=p.length;i++)
		       {
		    	  p[i-1]=new Providers();//对于每个引用，还要初始化实例对象，将其赋给引用
		    	  p[i-1].x=Double.parseDouble(a[i][0]);
		    	  p[i-1].y=Double.parseDouble(a[i][1]);
		    	  p[i-1].CapacityCtr=Integer.parseInt(a[i][2]);
		    	  p[i-1].capacity = new double[p[i-1].CapacityCtr];
		    	  for (int j=0;j<p[i-1].CapacityCtr;j++)
		    		  p[i-1].capacity[j]=Double.parseDouble(a[i][j+3]);
		       }
		       //按照数据特征，处理读入customer的数据
		       for (int i=p.length+2,k=0;i<lineCount;i++)
		       {
		          o[k]=new Customer();
		    	  o[k].x=Double.parseDouble(a[i][0]);
		          o[k].y=Double.parseDouble(a[i][1]);
		          o[k].Demand=Double.parseDouble(a[i][2]);
		          k++;
		       }
		       
		       /*for (int i=0;i<o.length;i++)
		       {
		    	   System.out.print(o[i].x+" ");
		    	   System.out.print(o[i].y+" ");
		    	   System.out.println(o[i].Demand+" ");
		       }*/
		       
		       P=p;O=o;
		     }
		     catch (IOException ex) {
		       ex.printStackTrace();
		     }
		
	}
	
}
